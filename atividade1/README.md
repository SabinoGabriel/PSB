# Atividade 1 - Gerenciamento de Processos no Linux

## Objetivo

Modificar `atividade1.py` para que uma carga computacional intensiva termine em aproximadamente 60 segundos, observando o efeito de prioridade e escalonamento no Linux.

## Estratégia

A carga principal fica isolada em um `multiprocessing.Process`. O processo principal atua como monitor externo: mede o tempo com `time.time()`, lê o consumo de CPU em `/proc/<pid>/stat` e ajusta a prioridade com `os.setpriority()`.

O ajuste usa os pesos do CFS associados aos valores de `nice`, evitando uma sequência grande de decisões manuais. A carga não é encerrada artificialmente ao chegar em 60 segundos; ela executa até completar todos os blocos.

## Características da carga

A função `carga_intensiva` mantém o laço interno sem `if`, `break`, `print` ou `sleep`.

O envio `fila.put(bloco)` ocorre somente ao final de cada bloco, fora do laço interno, para que o monitor conheça o progresso real da carga. O envio final `fila.put((total_blocos, acumulador))` transporta o checksum após o último bloco.

O monitor externo não segue essa restrição: ele pode usar condicionais, espera curta e impressão de log porque não faz parte da carga computacional principal.

## Parâmetros

- `--duracao-alvo`: tempo de parede desejado, por padrão 60 segundos;
- `--blocos`: número de blocos da carga;
- `--iteracoes-por-bloco`: quantidade de iterações em cada bloco;
- `--intervalo-monitor`: intervalo entre leituras do monitor.

O monitor drena a fila a cada ciclo e mantém o estado mais recente observado. Assim, `blocos` representa o último progresso recebido, não uma soma feita pelo monitor.

## Execução

Do diretório raiz do repositório:

```bash
sudo taskset -c 0 python3 atividade1/atividade1.py
```

Parâmetros opcionais:

```bash
sudo taskset -c 0 python3 atividade1/atividade1.py --duracao-alvo 60 --blocos 120 --iteracoes-por-bloco 450000
```

## Observações

- A atividade depende de Linux por usar `/proc`, `taskset` e política de prioridade do kernel.
- Reduzir `nice` para valores negativos normalmente exige `sudo`.
- A validação com concorrência deve ser feita com outro processo disputando o mesmo núcleo.
