# Princípios de Software Básico (PSB) - UFRPE

Repositório acadêmico da disciplina **Princípios de Software Básico (PSB)**, do curso de **Bacharelado em Sistemas de Informação** da **UFRPE**.

- **Professor:** Lidiano Oliveira
- **Aluno:** Gabriel Sabino Pinho Leite
- **Semestre:** 2026.1

## Objetivo

Organizar atividades práticas sobre interação entre programas e sistema operacional, com foco em processos, escalonamento, concorrência e sincronização.

## Estrutura

```text
psb/
├── README.md
├── LICENSE
├── atividade1/
│   ├── README.md
│   ├── atividade1.py
│   └── relatorio_atividade1.pdf
├── atividade2/
│   ├── README.md
│   ├── atividade2.py
│   └── relatorio_atividade2.md
└── docs/
    └── resumo_disciplina.md
```

## Atividades

| Atividade | Tema | Objetivo |
|---|---|---|
| [Atividade 1](./atividade1/README.md) | Processos no Linux | Controlar tempo de execução por prioridade, afinidade e CFS |
| [Atividade 2](./atividade2/README.md) | Leitores e escritores | Comparar execução sem sincronismo e com sincronismo |

## Ambiente

- Ubuntu 22.04 LTS
- Python 3.10.12
- Biblioteca padrão do Python

## Execução

Atividade 1:

```bash
sudo taskset -c 0 python3 atividade1/atividade1.py
```

Atividade 2:

```bash
python3 atividade2/atividade2.py
```

## Conceitos Trabalhados

- processos e threads;
- prioridade `nice` e CFS;
- tempo de CPU e tempo de parede;
- afinidade de CPU com `taskset`;
- monitoramento via `/proc`;
- condição de corrida;
- região crítica e exclusão mútua.
