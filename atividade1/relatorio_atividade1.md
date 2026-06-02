# Relatório - Atividade 1

**Disciplina:** Princípios de Software Básico  
**Professor:** Lidiano Oliveira  
**Semestre:** 2026.1  
**Atividade:** 1ª Atividade  
**Data:** 11/05/2026  

## 1. Objetivo

Modificar o arquivo `atividade1.py` para que uma carga computacional intensiva conclua sua execução em aproximadamente 60 segundos, utilizando `time.time()` para medição e `os.setpriority()` para ajuste dinâmico de prioridade.

O comportamento deve ser validado em Linux com concorrência forçada no mesmo núcleo de CPU, usando `taskset -c 0`.

## 2. Ambiente de Teste

- Sistema operacional: Ubuntu em máquina virtual VirtualBox
- Memória RAM: 4 GB
- Processadores virtuais: 2 núcleos
- Linguagem: Python 3
- Fixação de núcleo: `taskset -c 0`
- Execução com privilégio: `sudo`, quando for necessário reduzir `nice` para valores negativos

## 3. Estratégia

A função pesada foi mantida sem `if`, `break`, `print` ou `sleep` no laço principal. Isso reduz interferências no custo da carga e preserva melhor a quantidade de processamento útil executado.

Para não inserir controle dentro da carga, o trabalho foi isolado em um processo separado com `multiprocessing.Process`. O processo principal atua como monitor externo, lendo o tempo de CPU do trabalhador em `/proc/<pid>/stat` e ajustando sua prioridade por PID.

A cada ciclo de monitoramento, o programa estima quanto tempo de CPU ainda precisa ser recebido para que a execução se aproxime da meta de 60 segundos. Essa necessidade é convertida em um valor de `nice` usando os pesos reais do CFS do Linux. Assim, quando o processo está atrasado, o `nice` tende a diminuir; quando está adiantado, o `nice` tende a aumentar.

## 4. Calibração

A carga foi dividida em blocos para permitir medição externa de progresso. Os parâmetros principais são:

- `--duracao-alvo`: tempo de parede desejado, com padrão de 60 segundos;
- `--blocos`: quantidade de blocos da carga;
- `--iteracoes-por-bloco`: quantidade de iterações por bloco;
- `--intervalo-monitor`: intervalo entre leituras do monitor.

Como o desempenho depende da máquina, a calibração deve ser feita ajustando `--iteracoes-por-bloco`. Se o tempo final ficar muito abaixo ou acima de 60 segundos, esse parâmetro deve ser aumentado ou reduzido proporcionalmente.

## 5. Código Principal

O arquivo `atividade1.py` possui três partes principais:

1. carga computacional em `carga_intensiva`;
2. leitura externa de CPU em `/proc/<pid>/stat`;
3. cálculo e aplicação de prioridade com base nos pesos do CFS.

Trecho central da carga:

```python
def carga_intensiva(total_blocos: int, iteracoes_por_bloco: int, fila: mp.Queue) -> None:
    acumulador = 0x12345678
    mascara = 0xFFFFFFFF

    for bloco in range(1, total_blocos + 1):
        for i in range(iteracoes_por_bloco):
            acumulador = (acumulador * 1664525 + 1013904223 + i) & mascara
        fila.put(bloco)

    fila.put((total_blocos, acumulador))
```

O laço interno não possui condicionais, interrupções artificiais, impressão ou espera. O envio para a fila ocorre apenas ao final de cada bloco.

## 6. Controle por CFS

O código usa a tabela de pesos do CFS para valores de `nice` de `-20` a `19`. O monitor calcula um peso alvo conforme a proporção de CPU necessária para terminar próximo da meta e escolhe o `nice` cujo peso fica mais próximo:

```python
def nice_por_peso(peso: float) -> int:
    return min(range(-20, 20), key=lambda nice: abs(peso_cfs(nice) - peso))
```

Esse método evita uma sequência extensa de `if/elif` e aproxima o controle do comportamento real do escalonador Linux.

## 7. Comandos de Execução

Execução básica:

```bash
sudo taskset -c 0 python3 atividade1/atividade1.py
```

Execução com parâmetros explícitos:

```bash
sudo taskset -c 0 python3 atividade1/atividade1.py --duracao-alvo 60 --blocos 120 --iteracoes-por-bloco 450000
```

Validação com concorrência no mesmo núcleo:

```bash
sudo taskset -c 0 python3 concorrente.py &
sudo taskset -c 0 python3 atividade1/atividade1.py
```

O arquivo `concorrente.py` é apenas um apoio de teste e não faz parte da entrega do repositório.

## 8. Resultado Esperado

A execução deve terminar próxima de 60 segundos, sem encerrar artificialmente a carga ao atingir esse tempo. O trabalhador completa todos os blocos definidos, enquanto o monitor apenas ajusta sua prioridade.

Durante a validação, o comportamento esperado é:

- `nice` menor quando o processo precisa receber mais CPU;
- `nice` maior quando o processo está adiantado;
- tempo de parede final próximo da meta;
- carga principal preservada sem instrumentação interna pesada.

## 9. Conclusão

A solução mantém a carga computacional separada do controle de tempo. O ajuste ocorre externamente, por prioridade de processo, usando `os.setpriority()` e medições de CPU obtidas pelo `/proc`.

Com `multiprocessing`, o monitor consegue atuar sobre o PID correto do trabalhador. Com `taskset -c 0`, a disputa por CPU fica concentrada em um único núcleo, permitindo observar o efeito do CFS e dos valores de `nice` sobre a distribuição de tempo de processador.
