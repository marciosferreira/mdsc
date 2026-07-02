# skill: analise_alocacao
# descricao: Skill de análise de alocação de supply por Key Account (KA Allocation) — Request/Deal/Retail, Score de priorização, WOI, rollover/rollback, KPIs de Health Check. Executa SQL no SQLite de alocação (ka_input_data, ka_deal_allocation).
# palavras-chave: alocação, allocation, key account, KA, WOI, score, deal, request, retail, rollover, rollback, supply, site supply, health check, week supply, woi crítico, sell-in, booked, entered, one plan week

---

## ⚠️ COLUNAS PERIGOSAS — leia antes de escrever qualquer SQL

| Coluna | Tabela | Problema |
| --- | --- | --- |
| `year_month` | ambas | Confiável em ambas as tabelas. O arquivo de origem de `ka_deal_allocation` vinha com essa coluna corrompida (bug de exportação, colapsava para ~1969-12-31) — o valor foi corrigido no momento da carga (`load_ka_allocation.py`), usando o `year_month` de `ka_input_data` via join em `(quarter, material_id, key_account_id, month_seq)`. |
| `month_seq` | ambas | Posição do mês (1/2/3) dentro do grupo `(quarter, material_id, key_account_id)`, na ordem original do arquivo — útil para ordenar sem depender de `year_month`. |
| `month_status` | ambas | `done`/`ongoing` = meses do quarter atual (sempre nessa ordem: 2× `done`, depois `ongoing`); `next` = os 3 meses do próximo quarter. |
| `allocation_allowed` | `ka_deal_allocation` | Armazenada como INTEGER (1/0), não texto `"true"/"false"`. |

---

## ⏰ Granularidade temporal — NÃO existe dado por dia de calendário

`year_month` é sempre o **dia 1 do mês** (`2026-04-01`, `2026-05-01`, ...) — representa o mês
inteiro, não um dia específico. O detalhamento real dentro do mês é por **semana**
(`allocation_W1`..`allocation_W5`, `sell_in1`..`sell_in5`, `one_plan_week1`..`5`), não por data.

**Se o usuário pedir "alocação de hoje" (ou qualquer data que não seja o dia 1 de um mês):**
- NÃO filtre por `year_month = '<data de hoje>'` nem por um `LIKE` que capture o mês inteiro
  fingindo que é o dia exato — isso "encontra" dados do mês e responde como se existisse
  alocação para aquele dia específico, o que é falso.
- Responda explicando que a alocação é granular por **mês** (linhas sempre no dia 1) e por
  **semana** dentro do mês (W1 a W5) — não existe registro por dia de calendário. Ofereça a
  alocação do mês corrente (via `month_status = 'ongoing'`) ou peça pra especificar mês/semana.

---

## 📸 Os dados são um SNAPSHOT estático

As tabelas vêm de uma exportação pontual do algoritmo de alocação. O "agora" dos dados é
definido **dentro deles** (o mês com `month_status = 'ongoing'` e a coluna `current_month`),
e pode não coincidir com a data de hoje. Consequências práticas:

- O prefixo `[PERÍODO: from=...&to=...]` recebido na mensagem é um **rótulo** para o
  título/texto — o filtro SQL real deve usar `quarter`, `month_status` e `year_month`.
- `FQ1`, `FQ2` são valores **literais** da coluna `quarter` — filtre por eles diretamente
  (`WHERE quarter = 'FQ1'`), nunca converta para datas de calendário.
- Antes de concluir "não há dados para o período", verifique o range real:
  `SELECT quarter, month_status, MIN(year_month), MAX(year_month) FROM ka_deal_allocation GROUP BY quarter, month_status`.
  Se o período pedido não intersectar os dados, informe qual range existe e responda com o
  quarter em andamento, explicitando o ajuste.

---

## 📅 Período padrão quando o usuário não especifica

O WOI (e outras métricas) **muda entre quarters** — a mesma combinação produto+KA pode ter um
WOI em `FQ1` (atual) e outro bem diferente em `FQ2` (próximo). Dentro do mesmo quarter, o WOI é
constante nos 3 meses (`month_seq` 1/2/3) — varia só de quarter pra quarter.

**Se o usuário perguntar algo como "quais KAs estão com WOI crítico" (ou qualquer métrica) sem
mencionar período**, assuma o **quarter em andamento** por padrão — filtre por
`month_status IN ('done', 'ongoing')` — e deixe explícito na resposta que o resultado é do
quarter atual (cite o valor de `quarter`, ex: "FQ1"). Como o WOI se repete nos 3 meses do
quarter, agrupe/deduplique por KA (ex: `SELECT DISTINCT key_account_code, woi` ou `GROUP BY`)
para não listar a mesma KA três vezes.

Se o usuário quiser o próximo quarter ou uma comparação entre os dois, ele precisa pedir
explicitamente ("no próximo quarter", "compare os dois quarters") — nesse caso use
`month_status = 'next'` ou traga os dois lados rotulados por `quarter`.

---

## Esta é a skill de análise de KA Allocation

Use para qualquer pergunta sobre alocação de produto por Key Account: quanto foi alocado, por que uma conta recebeu mais/menos que outra, WOI crítico, rollover/rollback, deals atendidos, violação de capacidade semanal, etc. Esta é a única skill de análise deste agente.

---

## Fluxo obrigatório

```
1. read_skill('analise_alocacao.md')                    ← você já está aqui
2. executar_sql_alocacao(query=<SELECT...>, chave=<nome>) ← executa SQL e injeta DataFrame
3. analisar_dataframe(script)                            ← processa com pandas e gera resultado
```

Todo acesso a dado é via `executar_sql_alocacao` — não há API REST para este domínio.

---

## SQLite — regras críticas

| Regra | Como aplicar |
|-------|-------------|
| Apenas SELECT | Qualquer outro comando será rejeitado |
| Sem SELECT * | Liste sempre as colunas necessárias |
| Tabelas | `ka_input_data` (entrada do algoritmo) e `ka_deal_allocation` (resultado computado pela IA) |
| Ordenar/filtrar por mês | `year_month` já é confiável em ambas as tabelas; `month_seq` (1/2/3) + `month_status` também servem para ordenar sem depender de data |
| Booleanos | `allocation_allowed`, `current_quarter` são INTEGER 0/1 |

---

## Modelo de dados — o que cada tabela representa

### `ka_input_data` — dado de ENTRADA do algoritmo de alocação

Cada linha é uma combinação (produto, KA, quarter, mês) com a demanda e capacidade consideradas pela IA antes de calcular a alocação.

| Coluna | Significado |
|--------|-------------|
| material_id | Identificador do material/produto |
| family | Família comercial do produto |
| product_group | Grupo de produto |
| deal_group | Grupo de acordo comercial (Deal) ao qual o produto pertence |
| product | Nome/descrição completa do produto |
| sales_model | Modelo de vendas (código comercial) |
| origin | Site de origem do produto — JAG ou MAN |
| key_account_id | Identificador numérico da Key Account |
| key_account_code | Código da Key Account (ex: CLARO_BR, MMICOM_BR) |
| current_quarter | 1 se este registro pertence ao quarter atual, 0 caso contrário |
| current_month | Mês de referência atual do sistema (data) |
| current_week | Semana corrente dentro do mês/quarter |
| quarter | Identificador do quarter (ex: FQ1, FQ2) |
| year_month | Mês/ano do registro — **confiável nesta tabela** |
| month_status | `done` (mês fechado do quarter atual), `ongoing` (mês corrente) ou `next` (quarter seguinte) |
| entered_quarter | Volume "Entered" (intenção de pedido) do quarter — ver RN_013/Score |
| booked_quarter | Volume "Booked" (reservado/confirmado) do quarter — ver RN_013/Score |
| user_allocation1..5 | Alocação manual definida pelo usuário, por semana (1 a 5) do mês |
| sell_in1..5 | Volume faturado por semana |
| one_plan_week1..5 | Capacidade semanal definida no One Plan (limite de supply da semana) |
| req_qty | Request final considerado pela IA (Initial Request + Rollover − Rollback) |
| init_req_qty | Request inicial, antes de ajustes de Rollover/Rollback |
| deal | Valor do acordo comercial (Deal Value) aplicável ao registro |
| sell_in_lifetime | Total acumulado de unidades faturadas (usado no cálculo do WOI) |
| activations_lifetime | Total acumulado de unidades ativadas (usado no cálculo do WOI) |
| avg_activations | Média de ativações por semana (usado no cálculo do WOI) |
| woi | Weeks of Inventory — ver fórmula abaixo |
| month_seq | **Derivada no load** — posição do mês (1/2/3) dentro do grupo (quarter, material_id, key_account_id) |

### `ka_deal_allocation` — RESULTADO computado pela IA

Mesma granularidade da tabela acima, mas com os valores efetivamente calculados pelo algoritmo de alocação.

| Coluna | Significado |
|--------|-------------|
| quarter, material_id, key_account_id, key_account_code, deal_group, product, origin, current_week, month_status | Mesmo significado de `ka_input_data` |
| year_month | Mês/ano do registro — confiável (corrigida a partir de `ka_input_data` no momento da carga) |
| booked_quarter, entered_quarter | Mesmo significado de `ka_input_data` |
| initial_req_qty | Request inicial informado, antes de ajustes |
| req_qty | Request final considerado no cálculo (após Rollover/Rollback) |
| rollover | Volume de demanda não atendida em períodos anteriores, transferido para este período (aumenta o Request) |
| rollback | Ajuste negativo aplicado ao Request (reduz a demanda) |
| deal | Deal Value aplicável ao registro |
| sell_in1..5 | Volume faturado por semana |
| one_plan_week1..5 | Capacidade semanal (One Plan) |
| allocation_W1..W5 | **Volume final alocado pela IA**, por semana do mês — é a saída principal do algoritmo |
| allocation_alone_W1..W5 | Alocação isolada por semana (sem efeito de compensações), útil para comparar com `allocation_W1..5` |
| sell_in_comp_w1..5 | Compensação de Sell-in (ajuste técnico de faturamento, não é regra de validação) |
| sell_in_lifetime, activations_lifetime, avg_activations | Usados no cálculo do WOI |
| woi | WOI no momento da alocação |
| allocation_allowed | 1 se o registro (KA/produto/período) foi elegível para participar do cálculo da IA, 0 se foi ignorado (equivalente ao "Enable Allocation" da especificação) |
| proj_woi_w1..w5 | WOI projetado, semana a semana, após aplicar a alocação calculada |
| month_seq | **Derivada no load** — posição do mês (1/2/3) dentro do grupo (quarter, material_id, key_account_id) |

---

## Grafo de relacionamentos

```
ka_input_data (1) ──→ (1) ka_deal_allocation
  JOIN: quarter = quarter AND material_id = material_id
        AND key_account_id = key_account_id AND month_seq = month_seq
  Para: comparar a demanda/capacidade de ENTRADA com o resultado computado pela IA
```

---

## Glossário (ver especificação completa em "[GCA] RF xxx - AI KA Allocation Distribution Explainability v1.md")

| Termo | Significado |
| --- | --- |
| KA | Key Account, cliente estratégico |
| WOI | Weeks of Inventory — semanas de cobertura de estoque |
| Rollover | Demanda não atendida em períodos anteriores, transferida para o período atual (aumenta o Request) |
| Rollback | Ajuste negativo aplicado ao Request (reduz a demanda) |
| Allocation | Volume distribuído para o KA |
| Deal | Acordo comercial, definido por quarter |
| Supply | Volume em estoque disponível para alocação |
| Booked | Volume já reservado/confirmado comercialmente no quarter |
| Entered | Volume em intenção de reserva/pedido em andamento |
| Request | Volume de demanda considerado pela IA |
| Sell-in | Volume efetivamente faturado |

## WOI — fórmula e faixas de risco

```
woi = (sell_in_lifetime - activations_lifetime) / avg_activations
```

| Faixa | Classificação | Prioridade de alocação |
| --- | --- | --- |
| WOI = 0 | Ruptura grave (estoque esgotado) | Máxima |
| WOI < 10 | Crítico | Alta |
| 10 ≤ WOI < 15 | Risco médio | Moderada |
| WOI ≥ 15 | Fora de risco (saudável) | Menor |

Exceção: WOI não se aplica a MMICOM (segue só Request) nem a Retail (segue só Booked/Entered).

## Score de priorização (0 a 7) — RN_013

A IA processa o Request respeitando esta ordem (Score 0 primeiro, consome supply até acabar):

| Score | Condição | Peso |
| --- | --- | --- |
| 0 | MMICOM (sempre) | Ignora WOI/Booked/Entered — 100% do Request |
| 1 | WOI < 10 | 100% WOI |
| 2 | 10 ≤ WOI < 15 e Booked > 0 | 50% WOI / 50% Booked |
| 3 | 10 ≤ WOI < 15, Booked = 0, Entered > 0 | 75% WOI / 25% Entered |
| 4 | 10 ≤ WOI < 15, sem Booked/Entered | 100% WOI |
| 5 | WOI ≥ 15 e Booked > 0 | 100% Booked |
| 6 | WOI ≥ 15, Booked = 0, Entered > 0 | 100% Entered |
| 7 | Demais casos | Menor prioridade |

Em cenário de escassez, apenas Score 0 e 1 tendem a ser atendidos completamente — scores maiores só recebem se ainda sobrar supply. O Score não é uma coluna armazenada nas tabelas; para estimá-lo numa análise, combine `woi`, `booked_quarter` e `entered_quarter` conforme a tabela acima.

## KPIs do Health Check — tradução para SQL

| KPI | Padrão SQL (sobre `ka_deal_allocation`) |
| --- | --- |
| Critical WOI | `COUNT(*) WHERE woi < 10` |
| Input Data Inconsistencies | `COUNT(*) WHERE allocation_W1 < 0 OR ... OR allocation_W5 < 0` |
| Rounded Allocations (blocos de 10) | `COUNT(*) WHERE allocation_W1 % 10 = 0` (repetir por semana ou considerar o total mensal) |
| Complete Request | `COUNT(*) WHERE (allocation_W1+allocation_W2+allocation_W3+allocation_W4+allocation_W5) >= req_qty` |
| Rollover / Rollback | `COUNT(*) WHERE rollover > 0` / `COUNT(*) WHERE rollback > 0` |
| Completed Deals | `COUNT(*) WHERE deal > 0 AND (soma das allocation_W1..5) >= deal` |

⚠️ **Ressalva**: "Week Supply Violation" (capacidade semanal excedida) e "Site Supply Occurrences" (redistribuição entre JAG/MAN) exigiriam comparar a soma de todas as KAs numa mesma semana contra `one_plan_week*`, ou dados de site não presentes nestas duas tabelas — trate essas duas métricas como aproximações e deixe explícito na resposta que a precisão total do KPI original (tela Health Check) depende de dados agregados que essas tabelas planas não guardam sozinhas.

## Waterfall de processamento (contexto de leitura, RN_002)

A alocação final (`allocation_W1..5`) é o resultado de 3 etapas sequenciais que consomem o supply em cascata: **Request → Deal → Retail**. MMICOM não passa pela etapa de Deal (só Request/Score); Retail não usa WOI (só Booked/Entered). As tabelas armazenam apenas o resultado final de cada etapa — não há colunas separadas por etapa.

---

## Exemplos de queries

```sql
-- WOI crítico por Key Account, quarter atual
SELECT key_account_code, product, month_status, woi
FROM ka_deal_allocation
WHERE woi < 10 AND month_status IN ('done', 'ongoing')
ORDER BY woi ASC;
```

```sql
-- Alocação total por mês (month_seq) para uma Key Account
SELECT month_seq, month_status,
       SUM(allocation_W1 + allocation_W2 + allocation_W3 + allocation_W4 + allocation_W5) AS alocacao_mensal
FROM ka_deal_allocation
WHERE key_account_code = 'CLARO_BR'
GROUP BY month_seq, month_status
ORDER BY month_seq;
```

```sql
-- Comparar Request de entrada vs. alocação resultante (join input x output)
SELECT i.key_account_code, i.product, i.month_seq, i.req_qty,
       (o.allocation_W1+o.allocation_W2+o.allocation_W3+o.allocation_W4+o.allocation_W5) AS alocado
FROM ka_input_data i
JOIN ka_deal_allocation o
  ON i.quarter = o.quarter AND i.material_id = o.material_id
 AND i.key_account_id = o.key_account_id AND i.month_seq = o.month_seq
WHERE i.key_account_code = 'CLARO_BR';
```

---

## Ambiente Python (analisar_dataframe)

| Variável | Biblioteca |
|----------|-----------|
| `pd` | pandas |
| `np` | numpy |
| `plt` | matplotlib.pyplot |
| `stats` | scipy.stats |

Atribua `result = fig` para gráfico ou `result = df` para tabela.

Cores padrão do sistema: aprovado `#34d399` · crítico/inconsistência `#f87171` · atenção/pendente `#fbbf24` · neutro `#94a3b8` · volume `#60a5fa` · valor `#a78bfa`
