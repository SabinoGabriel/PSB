# Resumo da Disciplina — Princípios de Software Básico (PSB)

## Intuito da disciplina

A disciplina PSB estuda fundamentos de software com foco em sua execução sob controle do sistema operacional. A proposta central é observar, de forma prática, como escalonamento, concorrência e sincronização afetam o comportamento de programas.

## Conexão com Sistemas Operacionais

Os experimentos da disciplina abordam processos e threads como entidades de execução concorrente, destacando políticas de escalonamento, prioridades, região crítica e mecanismos de exclusão mútua.

## Contribuição da Atividade 1

A Atividade 1 conecta prioridade (`nice`), afinidade de CPU e partilha de tempo de processador no Linux. O uso de `taskset`, `/proc/<pid>/stat` e controle de carga computacional permite avaliar relação entre tempo de CPU e tempo de parede em cenário controlado.

## Contribuição da Atividade 2

A Atividade 2 compara comportamento sem sincronização e com sincronização no problema dos leitores e escritores. A análise evidencia condição de corrida na ausência de proteção e consistência de acesso quando há lock de leitura/escrita.

## Síntese

Em conjunto, as atividades consolidam uma visão experimental dos conceitos clássicos de SO, mostrando que decisões de escalonamento e sincronização influenciam diretamente correção e desempenho de software.
