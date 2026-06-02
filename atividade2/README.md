# Atividade 2 - Problema dos Leitores e Escritores

## Objetivo

Comparar duas versões do problema leitores-escritores:

1. execução sem sincronismo, sujeita a condição de corrida;
2. execução com sincronismo usando Readers-Writers Lock.

## Implementação

O código usa apenas a biblioteca padrão do Python:

- `threading` para concorrência;
- `time` para criar janelas de interleaving;
- `random` para variar a ordem observada de execução.

Na primeira parte, leitores e escritores acessam os mesmos dados sem proteger a região crítica. Na segunda, leitores podem executar em paralelo, mas escritores entram com acesso exclusivo.

Os `sleep()` curtos são intencionais: eles aumentam a chance de trocas de contexto entre threads e tornam a condição de corrida mais visível na versão sem sincronismo.

O lock implementado usa prioridade para leitores. Isso preserva paralelismo de leitura, mas pode atrasar escritores se novos leitores chegarem continuamente.

## Execução

```bash
python3 atividade2/atividade2.py
```

## Conceitos Trabalhados

- threads;
- condição de corrida;
- região crítica;
- exclusão mútua;
- sincronização;
- escrita exclusiva;
- paralelismo entre leitores;
- possível starvation de escritores em política com prioridade para leitores.
