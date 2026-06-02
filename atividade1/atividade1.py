#!/usr/bin/env python3
"""Atividade 1: controle de prioridade de processo no Linux."""

from __future__ import annotations

import argparse
import multiprocessing as mp
import os
import queue
import time
from dataclasses import dataclass


CFS_WEIGHTS = [
    88761, 71755, 56483, 46273, 36291, 29154, 23254, 18705, 14949, 11916,
    9548, 7620, 6100, 4904, 3906, 3121, 2501, 1991, 1586, 1277,
    1024, 820, 655, 526, 423, 335, 272, 215, 172, 137,
    110, 87, 70, 56, 45, 36, 29, 23, 18, 15,
]


@dataclass
class Resultado:
    blocos: int
    checksum: int | None
    tempo: float
    cpu: float
    nice: int


def peso_cfs(nice: int) -> int:
    return CFS_WEIGHTS[max(-20, min(19, nice)) + 20]


def nice_por_peso(peso: float) -> int:
    return min(range(-20, 20), key=lambda nice: abs(peso_cfs(nice) - peso))


def ler_cpu_processo(pid: int, tick_hz: int) -> float:
    with open(f"/proc/{pid}/stat", "r", encoding="utf-8") as arquivo:
        campos = arquivo.read().split()
    return (int(campos[13]) + int(campos[14])) / tick_hz


def carga_intensiva(total_blocos: int, iteracoes_por_bloco: int, fila: mp.Queue) -> None:
    acumulador = 0x12345678
    mascara = 0xFFFFFFFF

    for bloco in range(1, total_blocos + 1):
        for i in range(iteracoes_por_bloco):
            acumulador = (acumulador * 1664525 + 1013904223 + i) & mascara
        fila.put(bloco)

    fila.put((total_blocos, acumulador))


def drenar_fila(fila: mp.Queue, blocos: int, checksum: int | None) -> tuple[int, int | None]:
    while True:
        try:
            item = fila.get_nowait()
        except queue.Empty:
            return blocos, checksum

        if isinstance(item, tuple):
            blocos, checksum = item
        else:
            blocos = item


def calcular_nice(
    nice_atual: int,
    total_blocos: int,
    blocos: int,
    tempo: float,
    cpu: float,
    alvo: float,
) -> int:
    restante_tempo = alvo - tempo

    if blocos < 1 or blocos >= total_blocos or tempo <= 0 or cpu <= 0 or restante_tempo <= 0:
        return nice_atual

    cpu_por_bloco = cpu / blocos
    cpu_restante = cpu_por_bloco * (total_blocos - blocos)
    cota_atual = cpu / tempo
    cota_necessaria = cpu_restante / restante_tempo
    peso_alvo = peso_cfs(nice_atual) * cota_necessaria / cota_atual

    return nice_por_peso(peso_alvo)


def ajustar_prioridade(pid: int, nice_atual: int, novo_nice: int) -> int:
    if novo_nice == nice_atual:
        return nice_atual

    try:
        os.setpriority(os.PRIO_PROCESS, pid, novo_nice)
    except PermissionError:
        return nice_atual

    return novo_nice


def executar_experimento(alvo: float, total_blocos: int, iteracoes_por_bloco: int, intervalo: float) -> Resultado:
    fila: mp.Queue = mp.Queue()
    processo = mp.Process(target=carga_intensiva, args=(total_blocos, iteracoes_por_bloco, fila))

    inicio = time.time()
    processo.start()

    if processo.pid is None:
        raise RuntimeError("processo trabalhador não foi iniciado")

    pid = processo.pid
    tick_hz = os.sysconf(os.sysconf_names["SC_CLK_TCK"])
    nice_atual = os.getpriority(os.PRIO_PROCESS, pid)
    blocos = 0
    checksum = None
    cpu = 0.0

    while processo.is_alive():
        blocos, checksum = drenar_fila(fila, blocos, checksum)
        tempo = time.time() - inicio
        try:
            cpu = ler_cpu_processo(pid, tick_hz)
        except FileNotFoundError:
            break
        novo_nice = calcular_nice(nice_atual, total_blocos, blocos, tempo, cpu, alvo)
        nice_atual = ajustar_prioridade(pid, nice_atual, novo_nice)
        time.sleep(intervalo)

    processo.join()
    blocos, checksum = drenar_fila(fila, blocos, checksum)

    return Resultado(
        blocos=blocos,
        checksum=checksum,
        tempo=time.time() - inicio,
        cpu=cpu,
        nice=nice_atual,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Experimento de prioridade e CFS no Linux.")
    parser.add_argument("--duracao-alvo", type=float, default=60.0)
    parser.add_argument("--blocos", type=int, default=120)
    parser.add_argument("--iteracoes-por-bloco", type=int, default=450000)
    parser.add_argument("--intervalo-monitor", type=float, default=1.0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    executar_experimento(
        alvo=args.duracao_alvo,
        total_blocos=args.blocos,
        iteracoes_por_bloco=args.iteracoes_por_bloco,
        intervalo=args.intervalo_monitor,
    )


if __name__ == "__main__":
    main()
