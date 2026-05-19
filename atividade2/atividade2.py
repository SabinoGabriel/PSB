#!/usr/bin/env python3
"""Atividade 2 (PSB/UFRPE): problema leitores-escritores sem e com sincronização."""

from __future__ import annotations

import random
import threading
import time
from dataclasses import dataclass


@dataclass
class ResultadoExecucao:
    inconsistencias: int
    leituras: int
    escritas: int
    duracao: float


class ReadersWritersLock:
    """Lock com prioridade para leitores (primeiro/último leitor)."""

    def __init__(self) -> None:
        self.mutex = threading.Lock()
        self.escrita_lock = threading.Lock()
        self.leitores_ativos = 0

    def acquire_read(self) -> None:
        with self.mutex:
            self.leitores_ativos += 1
            if self.leitores_ativos == 1:
                self.escrita_lock.acquire()

    def release_read(self) -> None:
        with self.mutex:
            self.leitores_ativos -= 1
            if self.leitores_ativos == 0:
                self.escrita_lock.release()

    def acquire_write(self) -> None:
        self.escrita_lock.acquire()

    def release_write(self) -> None:
        self.escrita_lock.release()


def executar_sem_sincronismo(leitores: int, escritores: int, iteracoes: int) -> ResultadoExecucao:
    estado = {"valor": 0, "versao": 0}
    contadores = {"inconsistencias": 0, "leituras": 0, "escritas": 0}
    lock_contadores = threading.Lock()

    def leitor(_: int) -> None:
        local_inconsistencias = 0
        for _ in range(iteracoes):
            valor = estado["valor"]
            time.sleep(random.uniform(0.0008, 0.0020))
            versao = estado["versao"]
            if valor != versao:
                local_inconsistencias += 1
            with lock_contadores:
                contadores["leituras"] += 1
            time.sleep(random.uniform(0.0004, 0.0013))
        with lock_contadores:
            contadores["inconsistencias"] += local_inconsistencias

    def escritor(identificador: int) -> None:
        for passo in range(iteracoes):
            novo_valor = identificador * 100000 + passo
            estado["valor"] = novo_valor
            time.sleep(random.uniform(0.0008, 0.0022))
            estado["versao"] = novo_valor
            with lock_contadores:
                contadores["escritas"] += 1
            time.sleep(random.uniform(0.0004, 0.0012))

    inicio = time.time()
    threads = [threading.Thread(target=leitor, args=(i,), daemon=False) for i in range(leitores)]
    threads += [threading.Thread(target=escritor, args=(i,), daemon=False) for i in range(escritores)]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    return ResultadoExecucao(
        inconsistencias=contadores["inconsistencias"],
        leituras=contadores["leituras"],
        escritas=contadores["escritas"],
        duracao=time.time() - inicio,
    )


def executar_com_sincronismo(leitores: int, escritores: int, iteracoes: int) -> ResultadoExecucao:
    lock = ReadersWritersLock()
    estado = {"valor": 0, "versao": 0}
    contadores = {"inconsistencias": 0, "leituras": 0, "escritas": 0}
    lock_contadores = threading.Lock()

    def leitor(_: int) -> None:
        local_inconsistencias = 0
        for _ in range(iteracoes):
            lock.acquire_read()
            try:
                valor = estado["valor"]
                time.sleep(random.uniform(0.0005, 0.0016))
                versao = estado["versao"]
                if valor != versao:
                    local_inconsistencias += 1
                with lock_contadores:
                    contadores["leituras"] += 1
            finally:
                lock.release_read()
            time.sleep(random.uniform(0.0004, 0.0013))
        with lock_contadores:
            contadores["inconsistencias"] += local_inconsistencias

    def escritor(identificador: int) -> None:
        for passo in range(iteracoes):
            novo_valor = identificador * 100000 + passo
            lock.acquire_write()
            try:
                estado["valor"] = novo_valor
                time.sleep(random.uniform(0.0008, 0.0022))
                estado["versao"] = novo_valor
            finally:
                lock.release_write()
            with lock_contadores:
                contadores["escritas"] += 1
            time.sleep(random.uniform(0.0004, 0.0012))

    inicio = time.time()
    threads = [threading.Thread(target=leitor, args=(i,), daemon=False) for i in range(leitores)]
    threads += [threading.Thread(target=escritor, args=(i,), daemon=False) for i in range(escritores)]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    return ResultadoExecucao(
        inconsistencias=contadores["inconsistencias"],
        leituras=contadores["leituras"],
        escritas=contadores["escritas"],
        duracao=time.time() - inicio,
    )


def main() -> None:
    random.seed(42)
    leitores = 6
    escritores = 2
    iteracoes = 60

    print("=== PARTE 1: sem sincronismo ===")
    r1 = executar_sem_sincronismo(leitores=leitores, escritores=escritores, iteracoes=iteracoes)
    print(f"leituras={r1.leituras} escritas={r1.escritas} inconsistencias={r1.inconsistencias} tempo={r1.duracao:.3f}s")

    print("\n=== PARTE 2: com sincronismo (Readers-Writers Lock) ===")
    r2 = executar_com_sincronismo(leitores=leitores, escritores=escritores, iteracoes=iteracoes)
    print(f"leituras={r2.leituras} escritas={r2.escritas} inconsistencias={r2.inconsistencias} tempo={r2.duracao:.3f}s")

    print("\n=== COMPARATIVO ===")
    print(f"inconsistencias evitadas = {max(0, r1.inconsistencias - r2.inconsistencias)}")
    print("esperado: inconsistências > 0 sem sincronismo e ~0 com sincronismo")


if __name__ == "__main__":
    main()
