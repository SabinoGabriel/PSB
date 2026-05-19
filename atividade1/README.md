# Atividade 1 — Gerenciamento de Processos no Linux

## Tema

Manipulação de prioridade de processo e afinidade de CPU no Linux.

## Objetivo

Modificar `atividade1.py` para que uma carga computacional intensiva conclua em aproximadamente **60 segundos**, analisando o efeito de parâmetros do escalonador.

## Contexto técnico

Esta atividade é um **experimento de Sistemas Operacionais em ambiente Linux (Ubuntu)**. O comportamento observado depende de mecanismos específicos do kernel Linux.

## Técnicas empregadas

- medição de tempo com `time.time()`;
- ajuste de prioridade com `os.nice()` e/ou `os.setpriority()`;
- contenção no mesmo núcleo com `taskset -c 0`;
- leitura de `/proc/<pid>/stat` para monitorar uso de CPU;
- isolamento da carga em `multiprocessing.Process`;
- processo principal como monitor.

## Estratégia experimental

- A carga computacional foi mantida sem condicionais internas para preservar estabilidade do custo por iteração.
- Um processo trabalhador executa a rotina intensiva.
- O processo principal observa progresso, tempo de execução e consumo de CPU.
- O controle de partilha de CPU considera pesos reais associados a valores de `nice` no **CFS (Completely Fair Scheduler)**.
- A validação principal foi feita com disputa real no mesmo núcleo usando `taskset -c 0`.

## Conceitos de SO evidenciados

- escalonamento do Linux;
- CFS;
- prioridade `nice`;
- tempo de CPU vs. tempo de parede;
- concorrência entre processos;
- afinidade de CPU;
- monitoramento por `/proc`;
- calibração de carga computacional.

## Comandos de execução

Do diretório raiz do repositório:

```bash
sudo taskset -c 0 python3 atividade1/atividade1.py
```

Validação opcional com concorrência no mesmo núcleo:

```bash
sudo taskset -c 0 python3 concorrente.py &
sudo taskset -c 0 python3 atividade1/atividade1.py
```

## Observações

- Para reduzir `nice` para valores negativos (maior prioridade), normalmente é necessário executar com `sudo`.
- O script `concorrente.py` foi usado como apoio de validação experimental e **não é parte obrigatória da entrega** deste repositório.
- A reprodução dos resultados depende de Linux, especialmente pelo uso de `taskset`, `/proc` e política de escalonamento do kernel.
