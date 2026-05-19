# Princípios de Software Básico (PSB) — UFRPE

Repositório acadêmico da disciplina **Princípios de Software Básico (PSB)** do curso de **Bacharelado em Sistemas de Informação** da **Universidade Federal Rural de Pernambuco (UFRPE)**.

- **Professor:** Lidiano Oliveira  
- **Aluno:** Gabriel Sabino Pinho Leite  
- **Semestre:** 2026.1

## Descrição da disciplina

A disciplina PSB aborda fundamentos de software em interação direta com o sistema operacional, com ênfase em observação prática do comportamento de programas em execução.

## Objetivos do repositório

Este repositório organiza experimentos e relatórios para demonstrar, de forma aplicada, conceitos clássicos de Sistemas Operacionais, incluindo:

- execução de programas no Linux;
- processos e threads;
- escalonamento e prioridade de execução;
- concorrência e sincronização;
- região crítica e exclusão mútua;
- análise de comportamento em ambiente controlado.

O foco não é apenas “fazer o código funcionar”, mas **compreender como o SO influencia a execução**.

## Estrutura de pastas

```text
psb/
├── README.md
├── .gitignore
├── LICENSE
├── atividade1/
│   ├── README.md
│   ├── atividade1.py
│   ├── relatorio_atividade1.pdf
│   └── exemplos/
│       └── log_exemplo.txt
├── atividade2/
│   ├── README.md
│   ├── atividade2.py
│   ├── relatorio_atividade2.md
│   └── log_atividade2.txt
└── docs/
    └── resumo_disciplina.md
```

## Resumo breve da disciplina

A disciplina investiga fundamentos de software em nível de sistema por meio de atividades experimentais. A Atividade 1 concentra-se no escalonamento de processos no Linux (prioridade, afinidade e tempo de execução). A Atividade 2 aborda concorrência entre threads e sincronização usando o problema dos leitores e escritores.

## Atividades

| Atividade | Tema | Objetivo principal | Tecnologias |
|---|---|---|---|
| [Atividade 1](./atividade1/README.md) | Gerenciamento de processos no Linux | Relacionar prioridade/afinidade com tempo de execução de carga computacional | Python + recursos do Linux (`taskset`, `/proc`, `nice`) |
| [Atividade 2](./atividade2/README.md) | Leitores e escritores | Comparar execução sem sincronismo e com sincronismo | Python (biblioteca padrão: `threading`, `time`, `random`) |

## Ambiente utilizado

- Ubuntu 22.04 LTS (validação principal)
- Python 3.10.12
- VirtualBox
- 4 GB RAM
- 2 núcleos de CPU

## Como executar cada atividade

### Atividade 1 (dependente de Linux)

```bash
sudo taskset -c 0 python3 atividade1/atividade1.py
```

Para gerar concorrência no mesmo núcleo:

```bash
sudo taskset -c 0 python3 concorrente.py &
sudo taskset -c 0 python3 atividade1/atividade1.py
```

### Atividade 2 (portável)

```bash
mkdir -p ~/atividade_psb
cd ~/atividade_psb
python3 --version
python3 atividade2.py | tee log_atividade2.txt
```

> Observação: a Atividade 2 usa somente biblioteca padrão do Python e é portável. A validação principal foi feita em Ubuntu.

## Principais conceitos aprendidos

- escalonamento de processos no Linux e CFS;
- prioridade `nice` e impacto na partilha de CPU;
- tempo de CPU versus tempo de parede;
- afinidade de CPU e contenção em núcleo único;
- monitoramento de processos via `/proc`;
- condição de corrida em threads;
- região crítica, exclusão mútua e sincronização;
- política de leitores e escrita exclusiva no problema leitores-escritores.

## Sugestão de descrição curta (GitHub)

Repositório acadêmico da disciplina PSB (UFRPE) com experimentos de escalonamento de processos no Linux e sincronização de threads em Python.

## Sugestão de tópicos/tags (GitHub)

`ufrpe`, `sistemas-operacionais`, `psb`, `python`, `linux`, `processos`, `threads`, `concorrencia`, `sincronizacao`, `cfs`

## Sugestões de commits iniciais

1. `docs: estrutura inicial do repositório da disciplina PSB`
2. `docs: adiciona README principal com objetivos e instruções de execução`
3. `docs(atividade1): descreve experimento de escalonamento no Linux`
4. `docs(atividade2): documenta versão sem e com sincronização`
5. `chore: adiciona .gitignore Python e licença MIT`

## Observações finais

- O projeto utiliza **apenas a biblioteca padrão do Python**.
- A Atividade 1 é fortemente vinculada ao ambiente Linux (Ubuntu) por usar recursos específicos do SO.
- A Atividade 2 foi validada em Ubuntu, mas não depende de funcionalidades exclusivas de Linux.

## O que colocar no repositório

- [x] `README.md` principal com contexto acadêmico da disciplina
- [x] `atividade1/README.md` com foco em escalonamento, prioridade e afinidade no Linux
- [x] `atividade2/README.md` com comparação sem/com sincronização
- [x] `docs/resumo_disciplina.md`
- [x] Estrutura de pastas conforme proposta
- [x] `.gitignore` para Python
- [x] `LICENSE` (MIT)
- [x] Sugestões de descrição curta, tópicos e commits iniciais
- [ ] Arquivos de implementação e relatórios finais da disciplina (`atividade1.py`, `atividade2.py`, relatórios e logs reais)
