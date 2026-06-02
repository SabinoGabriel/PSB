# Atividade 1 - Gerenciamento de Processos no Linux

## Objetivo

Modificar `atividade1.py` para que uma carga computacional intensiva termine em aproximadamente 60 segundos, observando o efeito de prioridade e escalonamento no Linux.

## Estratégia

A carga principal fica isolada em um `multiprocessing.Process`. O processo principal atua como monitor externo: mede o tempo com `time.time()`, lê o consumo de CPU em `/proc/<pid>/stat` e ajusta a prioridade com `os.setpriority()`.

O ajuste usa os pesos do CFS associados aos valores de `nice`, evitando uma sequência grande de decisões manuais. A carga não é encerrada artificialmente ao chegar em 60 segundos; ela executa até completar todos os blocos.

## Características da carga

- sem `if` no laço principal;
- sem `break`;
- sem `print`;
- sem `sleep`;
- envio de progresso apenas ao final de cada bloco.

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
