# Capacidades do agente — KA Allocation AI

O agente responde em linguagem natural sobre alocação de supply por Key Account, WOI, Score, Deal e KPIs de Health Check.

## Arquitetura simples

| Camada | Responsabilidade |
|--------|-----------------|
| `analise_alocacao` | **Única skill de análise** — toda pergunta de dados usa SQL direto no SQLite de alocação |

## Como o agente responde perguntas de dados

```
Usuário faz uma pergunta
      ↓
Orquestrador → consultar_analista()
      ↓
Sub-agente lê analise_alocacao.md
      ↓
Escreve e executa SQL no SQLite de alocação
      ↓
Processa resultado com pandas
      ↓
Responde com tabela ou gráfico
```

## Tipos de análise suportados

**Por tempo:** quarter atual, próximo quarter, por mês (`month_seq`/`month_status`)

**Por Key Account:** ranking de alocação, WOI por KA, deals completos por KA

**Por produto:** alocação por produto/deal_group, por origem (JAG/MAN)

**Por risco de estoque:** KAs com WOI crítico, WOI projetado, distribuição por faixa de risco

**Por regra de negócio:** Score de priorização, rollover/rollback aplicados, elegibilidade (allocation_allowed)

**Comparativo:** Request de entrada vs. alocação resultante (join `ka_input_data` × `ka_deal_allocation`)

**Cruzamentos:** qualquer combinação das dimensões acima via JOIN

## Formatos de saída

- Tabela markdown
- Gráfico (barra, linha, pizza, dispersão)
- PDF com análise e gráficos
- Planilha Excel para download

## Períodos aceitos em linguagem natural

Como a granularidade é por quarter/mês (não por data de calendário), períodos costumam ser expressos como "este quarter", "próximo quarter", "quarter atual" — o agente também aceita "hoje", "esta semana", "este mês" para rotular o período do relatório, mesmo quando o filtro real de dados usa `quarter`/`month_status`.

## Tarefas agendadas

O agente pode criar tarefas que rodam automaticamente.

**Relatórios periódicos:**
- "Toda segunda às 8h me manda o resumo de WOI crítico por Key Account"
- "Todo dia às 7h gera um PDF com a alocação do quarter atual"
- "Todo primeiro do mês exporta os dados de alocação para Excel"

**Monitores com alertas:**
- "Me avise se mais de 10 Key Accounts ficarem com WOI crítico"
- "Alerta quando houver rollback aplicado no quarter atual"

Frequências: `once`, `daily`, `weekly`, `monthly`, `every_Xm`, `every_Xh`, `every_Xd`

**Gerenciamento:** "Liste as tarefas", "Pause a tarefa 003", "Delete a tarefa 001"
