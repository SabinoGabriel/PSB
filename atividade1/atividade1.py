#!/usr/bin/env python3
"""Atividade 1 (PSB/UFRPE): prioridade, afinidade e monitoramento de processo no Linux."""

from __future__ import annotations

import argparse
import multiprocessing as mp
import os
import queue
import time
from dataclasses import dataclass

# Pesos do CFS para nice -20..19 (kernel Linux).
CFS_WEIGHTS = [
    88761, 71755, 56483, 46273, 36291, 29154, 23254, 18705, 14949, 11916,
    9548, 7620, 6100, 4904, 3906, 3121, 2501, 1991, 1586, 1277,
    1024, 820, 655, 526, 423, 335, 272, 215, 172, 137,
    110, 87, 70, 56, 45, 36, 29, 23, 18, 15,
]


@dataclass
class Progresso:
    blocos_concluidos: int
    total_blocos: int
    checksum: int | None = None


def peso_cfs(nice: int) -> int:
    """Retorna o peso do CFS para um valor de nice no intervalo [-20, 19]."""
    nice_limitado = max(-20, min(19, nice))
    return CFS_WEIGHTS[nice_limitado + 20]


def ler_jiffies_processo(pid: int) -> int:
    """Lê utime+stime de /proc/<pid>/stat (em jiffies)."""
    with open(f"/proc/{pid}/stat", "r", encoding="utf-8") as arquivo:
        campos = arquivo.read().split()
    utime = int(campos[13])
    stime = int(campos[14])
    return utime + stime


def carga_intensiva(total_blocos: int, iteracoes_por_bloco: int, fila: mp.Queue) -> None:
    """Executa carga CPU-bound com custo estável por bloco."""
    acumulador = 0x12345678
    mascara = 0xFFFFFFFF

    for bloco in range(1, total_blocos + 1):
        for i in range(iteracoes_por_bloco):
            acumulador = (acumulador * 1664525 + 1013904223 + i) & mascara
        fila.put(Progresso(blocos_concluidos=bloco, total_blocos=total_blocos))

    fila.put(Progresso(blocos_concluidos=total_blocos, total_blocos=total_blocos, checksum=acumulador))


def ajustar_prioridade(pid: int, nice_atual: int, total_blocos: int, concluidos: int, decorrido: float, alvo: float) -> int:
    """Ajusta nice dinamicamente para aproximar o tempo de parede ao alvo."""
    if concluidos < 1 or decorrido <= 0:
        return nice_atual

    fracao_esperada = min(1.0, decorrido / alvo)
    blocos_esperados = max(1, int(total_blocos * fracao_esperada))

    novo_nice = nice_atual
    tolerancia = 0.06
    progresso_relativo = concluidos / blocos_esperados

    if progresso_relativo > 1.0 + tolerancia:
        novo_nice = min(19, nice_atual + 1)
    elif progresso_relativo < 1.0 - tolerancia:
        novo_nice = max(-20, nice_atual - 1)

    if novo_nice == nice_atual:
        return nice_atual

    try:
        os.setpriority(os.PRIO_PROCESS, pid, novo_nice)
        return novo_nice
    except PermissionError:
        return nice_atual


def executar_experimento(alvo_segundos: float, total_blocos: int, iteracoes_por_bloco: int, intervalo_monitor: float) -> None:
    """Executa experimento de monitoramento e controle de prioridade."""
    fila: mp.Queue = mp.Queue()
    trabalhador = mp.Process(target=carga_intensiva, args=(total_blocos, iteracoes_por_bloco, fila), daemon=False)

    inicio = time.time()
    trabalhador.start()

    pid = trabalhador.pid
    if pid is None:
        raise RuntimeError("Falha ao iniciar processo trabalhador.")

    tick_hz = os.sysconf(os.sysconf_names["SC_CLK_TCK"])
    nice_atual = os.getpriority(os.PRIO_PROCESS, pid)

    print("[monitor] experimento iniciado")
    print(f"[monitor] pid={pid} nice_inicial={nice_atual} peso_cfs={peso_cfs(nice_atual)}")

    concluidos = 0
    checksum = None

    ultimo_cpu_segundos = 0.0

    while trabalhador.is_alive() or not fila.empty():
        try:
            while True:
                progresso = fila.get_nowait()
                concluidos = progresso.blocos_concluidos
                if progresso.checksum is not None:
                    checksum = progresso.checksum
        except queue.Empty:
            pass

        decorrido = time.time() - inicio
        if trabalhador.is_alive():
            jiffies = ler_jiffies_processo(pid)
            ultimo_cpu_segundos = jiffies / tick_hz
        cpu_segundos = ultimo_cpu_segundos

        novo_nice = ajustar_prioridade(pid, nice_atual, total_blocos, concluidos, decorrido, alvo_segundos) if trabalhador.is_alive() else nice_atual
        if novo_nice != nice_atual:
            nice_atual = novo_nice
            print(f"[monitor] ajuste nice -> {nice_atual} (peso_cfs={peso_cfs(nice_atual)})")

        progresso_pct = (concluidos / total_blocos) * 100.0
        print(
            f"[monitor] t={decorrido:6.2f}s progresso={progresso_pct:6.2f}% "
            f"cpu={cpu_segundos:6.2f}s nice={nice_atual:>3d}"
        )

        if not trabalhador.is_alive() and concluidos >= total_blocos:
            break

        time.sleep(intervalo_monitor)

    trabalhador.join()
    tempo_total = time.time() - inicio
    print(f"[resultado] alvo={alvo_segundos:.2f}s real={tempo_total:.2f}s desvio={tempo_total - alvo_segundos:+.2f}s")
    print(f"[resultado] blocos={concluidos}/{total_blocos} checksum={checksum}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Experimento de prioridade e monitoramento de processo no Linux.")
    parser.add_argument("--duracao-alvo", type=float, default=60.0, help="Tempo de parede alvo em segundos (padrão: 60).")
    parser.add_argument("--blocos", type=int, default=120, help="Quantidade de blocos computacionais da carga.")
    parser.add_argument("--iteracoes-por-bloco", type=int, default=450000, help="Iterações por bloco da carga CPU-bound.")
    parser.add_argument("--intervalo-monitor", type=float, default=1.0, help="Intervalo de monitoramento em segundos.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    executar_experimento(
        alvo_segundos=args.duracao_alvo,
        total_blocos=args.blocos,
        iteracoes_por_bloco=args.iteracoes_por_bloco,
        intervalo_monitor=args.intervalo_monitor,
    )


if __name__ == "__main__":
    main()
