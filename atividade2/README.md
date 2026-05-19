# Atividade 2 — Problema dos Leitores e Escritores

## Tema

Concorrência e sincronização em threads no problema clássico de leitores e escritores.

## Objetivo

Implementar, no mesmo arquivo `atividade2.py`, duas abordagens:

1. versão **sem sincronismo** (para evidenciar condição de corrida);
2. versão **com sincronismo** (Readers-Writers Lock).

## Ambiente de validação

- Python 3.10.12
- Ubuntu 22.04 LTS
- VirtualBox
- 4 GB RAM
- 2 núcleos

## Implementação

- somente biblioteca padrão do Python;
- módulos: `threading`, `time`, `random`;
- sem bibliotecas externas.

## Parte 1 — Sem sincronismo

Cenário com acessos concorrentes descontrolados à região crítica, permitindo:

- condição de corrida;
- leituras inconsistentes;
- possibilidade de perda de escrita.

## Parte 2 — Com sincronismo

Aplicação de Readers-Writers Lock com:

- `mutex` para controle do contador de leitores;
- `escrita_lock` para exclusão da escrita;
- política de prioridade para leitores;
- regra do primeiro/último leitor.

## Conceitos de SO evidenciados

- condição de corrida;
- região crítica;
- exclusão mútua;
- sincronização;
- acesso concorrente;
- paralelismo entre leitores;
- escrita exclusiva;
- escalonamento não determinístico de threads.

## Procedimento de execução

```bash
mkdir -p ~/atividade_psb
cd ~/atividade_psb
python3 --version
python3 atividade2.py | tee log_atividade2.txt
```

## Observação

Diferentemente da Atividade 1, esta atividade é **portável** por usar apenas biblioteca padrão do Python. A validação principal foi realizada em Ubuntu.
