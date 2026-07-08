# Pack de configuração — KA Allocation

Esta pasta define **qual banco** o chat IA analisa e **como ele entende o domínio**.
Trocar `settings.yml` + `dominio.md` re-aponta o sistema inteiro (chat, widgets do
dashboard, tarefas agendadas, monitores) para outro banco. **Requer restart do app.**

## Arquivos

| Arquivo | Papel |
| --- | --- |
| `settings.yml` | Nome/descrição do app + URL SQLAlchemy do banco (segredos via `${VAR}` do ambiente; env `DATABASE_URL` tem precedência) |
| `dominio.md` | Todo o conhecimento de domínio, em seções canônicas `## ` (ver abaixo) |
| `README.md` | Este arquivo — não é lido pelo engine |

## Seções canônicas de `dominio.md`

- `## Regras do agente` — injetada no prompt do sub-agente analista
- `## Regras do orquestrador` — injetada no prompt do orquestrador
- `## Períodos` — machine-parsable: `### frases | separadas` ou `### re:<regex>` + bloco ```sql
  que retorna 1 linha com (from, to); ordem importa, primeira que casa vence
- `## Modelo de dados` — schema/joins/exemplos; servida por `rag_dados` e `read_skill('dominio.md')`
- `## Domínio de negócio` — regras de negócio/glossário; servida por `rag_dominio`
- `## Exemplos task_code` — anexada às regras do sandbox de tarefas agendadas
- `## Dica para condition_sql` — tabelas/colunas para criação de monitores

Headings internos das seções devem ser `###` (nunca `##`, que delimita seções).

## Este pack (KA Allocation)

- **Carga de dados**: `python load_ka_allocation.py` (raiz) — lê os dois xlsx de alocação
  e recria `allocation.db` (tabelas `ka_input_data` e `ka_deal_allocation`).
- **Widgets iniciais**: `python seed_widgets_allocation.py` (raiz) cria os 2 painéis
  padrão no dashboard (alocação por KA no quarter atual; faixas de WOI). Equivalente via
  chat: "adiciona ao dashboard um painel de alocação por Key Account no quarter atual" e
  "adiciona ao dashboard um painel com a distribuição de WOI por faixa de risco".
