# Relatório — Atividade 2 (Leitores e Escritores)

## 1. Contexto

Esta atividade da disciplina Princípios de Software Básico (PSB) investigou o problema clássico de leitores e escritores, com foco em concorrência, sincronização e exclusão mútua.

## 2. Objetivo

Implementar e comparar, no mesmo programa Python:

1. uma versão **sem sincronismo**, sujeita a condição de corrida;
2. uma versão **com sincronismo**, usando Readers-Writers Lock com prioridade para leitores.

## 3. Ambiente

- Python 3.10.12
- Ubuntu 22.04 LTS
- VirtualBox
- 4 GB RAM
- 2 núcleos de CPU

## 4. Implementação

Foram usadas apenas bibliotecas da distribuição padrão do Python:

- `threading` para concorrência;
- `time` para temporizações curtas;
- `random` para variação no escalonamento observado.

Não foram utilizadas dependências externas.

As pausas curtas com `sleep()` foram incluídas de forma proposital para aumentar a chance de interleavings entre threads. Sem essa janela, a condição de corrida poderia ficar menos evidente em algumas execuções.

## 5. Parte 1 — Sem sincronismo

A versão sem sincronismo acessa e atualiza a região crítica sem proteção. Escritores atualizam os campos compartilhados (`valor` e `versao`) em dois passos, abrindo janela para que leitores observem estado intermediário. O resultado esperado é a ocorrência de leituras inconsistentes.

## 6. Parte 2 — Com sincronismo

A versão sincronizada utiliza Readers-Writers Lock composto por:

- `mutex`: proteção do contador de leitores;
- `escrita_lock`: exclusão mútua de escrita.

Regras aplicadas:

- primeiro leitor adquire `escrita_lock`;
- último leitor libera `escrita_lock`;
- escritor entra em região crítica com acesso exclusivo.

Essa política dá prioridade aos leitores. Em um fluxo contínuo de leitores, escritores podem ficar esperando por mais tempo, caracterizando risco de starvation. Para a atividade, esse comportamento é aceitável porque o objetivo principal é demonstrar leitura paralela e escrita exclusiva.

## 7. Resultados observados

A execução típica registra inconsistências na versão sem sincronismo e zero inconsistências na versão sincronizada, evidenciando a correção lógica ao proteger a região crítica.

Exemplo de saída representativa:

```text
=== PARTE 1: sem sincronismo ===
leituras=360 escritas=120 inconsistencias=87 tempo=0.212s

=== PARTE 2: com sincronismo (Readers-Writers Lock) ===
leituras=360 escritas=120 inconsistencias=0 tempo=0.311s

=== COMPARATIVO ===
inconsistencias evitadas = 87
esperado: inconsistências > 0 sem sincronismo e 0 com sincronismo
```

## 8. Conclusão

A atividade confirmou, de forma experimental, que ausência de sincronização em acesso concorrente leva a condição de corrida e resultados incorretos. Com lock apropriado, mantém-se paralelismo entre leitores e escrita exclusiva, preservando consistência dos dados.
