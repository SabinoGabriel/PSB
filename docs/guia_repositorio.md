# Guia do Repositório PSB

## Descrição curta para o GitHub

> Atividades práticas da disciplina Princípios de Software Básico (PSB) — UFRPE 2026.1. Experimentos em Python sobre gerenciamento de processos no Linux (CFS, `nice`, `/proc`) e sincronização de threads (problema dos leitores e escritores).

---

## Tópicos/Tags sugeridos para o GitHub

```
python  sistemas-operacionais  linux  processos  threads  concorrencia
sincronizacao  cfs  escalonamento  ufrpe  disciplina  academico
leitores-escritores  multiprocessing  threading
```

---

## Sugestão de commits iniciais

```
feat: estrutura inicial do repositório PSB

docs: adiciona README principal com visão geral da disciplina

feat(atividade1): adiciona código de gerenciamento de processos com CFS

docs(atividade1): documenta estratégia de controle por prioridade nice

feat(atividade1): adiciona log de execução representativo

docs(atividade1): adiciona relatório da atividade 1

feat(atividade2): adiciona implementação do problema dos leitores e escritores

docs(atividade2): documenta comparação entre versão sem e com sincronismo

docs(atividade2): adiciona relatório e log de execução

docs: adiciona resumo conceitual da disciplina em docs/resumo_disciplina.md

chore: adiciona .gitignore para Python e LICENSE MIT
```

---

## Checklist — O que colocar no repositório

### Raiz do projeto

- [ ] `README.md` — visão geral completa da disciplina e das atividades
- [ ] `.gitignore` — ignora `__pycache__`, `.pyc`, ambientes virtuais etc.
- [ ] `LICENSE` — MIT com nome do aluno e ano 2026

### atividade1/

- [ ] `README.md` — objetivo, estratégia, conceitos, comandos e log de execução
- [ ] `atividade1.py` — código principal (monitor + trabalhador)
- [ ] `relatorio_atividade1.pdf` — relatório entregue ao professor
- [ ] `exemplos/log_exemplo.txt` — saída representativa anotada com legenda das colunas

> **Não incluir:** `concorrente.py` (usado apenas na validação; documentado no relatório)

### atividade2/

- [ ] `README.md` — objetivo, implementação, conceitos e procedimento de execução
- [ ] `atividade2.py` — código com as duas partes (sem e com sincronismo)
- [ ] `relatorio_atividade2.md` — relatório completo em Markdown
- [ ] `log_atividade2.txt` — saída capturada durante a execução de validação

### docs/

- [ ] `resumo_disciplina.md` — visão conceitual da disciplina e conexão com as atividades
- [ ] `guia_repositorio.md` — este arquivo (opcional; pode ser removido antes de publicar)

---

## O que NÃO incluir

| Item | Motivo |
|---|---|
| `concorrente.py` | Script de validação, não faz parte da solução entregue |
| `requirements.txt` | Sem dependências externas; declarar ausência no README é suficiente |
| Ambientes virtuais (`.venv/`, `venv/`) | Cobertos pelo `.gitignore` |
| Arquivos `*.pyc` / `__pycache__/` | Cobertos pelo `.gitignore` |
| PDFs de slides ou material do professor | Direitos autorais do professor |
| Dados pessoais ou credenciais | Nunca versionar |

---

## Verificação antes de publicar

- [ ] O `README.md` principal descreve corretamente o que cada atividade demonstra?
- [ ] Os READMEs das atividades mencionam os requisitos de ambiente (Linux para atividade 1)?
- [ ] O `.gitignore` está funcionando (`git status` não mostra arquivos indesejados)?
- [ ] O `relatorio_atividade1.pdf` está incluído e abre corretamente?
- [ ] O `log_atividade2.txt` foi gerado a partir de uma execução real?
- [ ] Nenhum arquivo contém caminhos absolutos locais (ex.: `/home/gabriel/...`)?
