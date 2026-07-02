# Schema e semântica do banco — KA Allocation

## Banco de dados

SQLite local (`allocation.db`). A ferramenta `executar_sql_alocacao` conecta diretamente a esse
arquivo — use os nomes das tabelas sem prefixo/schema. Não há endpoints REST para este domínio;
todo acesso a dado é via SQL direto.

**Regra crítica:** não há tipos enum nem casts (`::text`) neste banco — é SQLite puro.

---

## Entidades e o que cada uma representa

### `ka_input_data` — dado de ENTRADA do algoritmo de alocação

Cada linha é uma combinação (produto, KA, quarter, mês) com a demanda e capacidade consideradas
pela IA antes de calcular a alocação.

| Coluna | Tipo | O que significa no negócio |
|--------|------|---------------------------|
| material_id | integer | Identificador do material/produto |
| family | text | Família comercial do produto |
| product_group | text | Grupo de produto |
| deal_group | text | Grupo de acordo comercial (Deal) ao qual o produto pertence |
| product | text | Nome/descrição completa do produto |
| sales_model | text | Modelo de vendas (código comercial) |
| origin | text | Site de origem do produto — JAG ou MAN |
| key_account_id | integer | Identificador numérico da Key Account |
| key_account_code | text | Código da Key Account (ex: CLARO_BR, MMICOM_BR) |
| current_quarter | integer | 1 se este registro pertence ao quarter atual, 0 caso contrário |
| current_month | text | Mês de referência atual do sistema |
| current_week | integer | Semana corrente dentro do mês/quarter |
| quarter | text | Identificador do quarter (ex: FQ1, FQ2) |
| year_month | text | Mês/ano do registro — **confiável nesta tabela** |
| month_status | text | `done` (mês fechado do quarter atual), `ongoing` (mês corrente) ou `next` (quarter seguinte) |
| entered_quarter | integer | Volume "Entered" (intenção de pedido) do quarter |
| booked_quarter | integer | Volume "Booked" (reservado/confirmado) do quarter |
| user_allocation1..5 | integer | Alocação manual definida pelo usuário, por semana (1 a 5) do mês |
| sell_in1..5 | integer | Volume faturado por semana |
| one_plan_week1..5 | integer | Capacidade semanal definida no One Plan |
| req_qty | integer | Request final considerado pela IA (Initial Request + Rollover − Rollback) |
| init_req_qty | integer | Request inicial, antes de ajustes |
| deal | integer | Valor do acordo comercial (Deal Value) aplicável ao registro |
| sell_in_lifetime | integer | Total acumulado de unidades faturadas (usado no cálculo do WOI) |
| activations_lifetime | integer | Total acumulado de unidades ativadas (usado no cálculo do WOI) |
| avg_activations | integer | Média de ativações por semana (usado no cálculo do WOI) |
| woi | real | Weeks of Inventory |
| month_seq | integer | Posição do mês (1/2/3) dentro do grupo (quarter, material_id, key_account_id) |

---

### `ka_deal_allocation` — RESULTADO computado pela IA

Mesma granularidade da tabela acima, com os valores efetivamente calculados pelo algoritmo.

| Coluna | Tipo | O que significa no negócio |
|--------|------|---------------------------|
| quarter, material_id, key_account_id, key_account_code, deal_group, product, origin, current_week, month_status | — | Mesmo significado de `ka_input_data` |
| year_month | text | Mês/ano do registro — confiável (o arquivo de origem vinha corrompido; corrigido no momento da carga a partir de `ka_input_data`) |
| booked_quarter, entered_quarter | integer | Mesmo significado de `ka_input_data` |
| initial_req_qty | integer | Request inicial informado, antes de ajustes |
| req_qty | integer | Request final considerado no cálculo (após Rollover/Rollback) |
| rollover | integer | Demanda não atendida em períodos anteriores, transferida para este período |
| rollback | integer | Ajuste negativo aplicado ao Request |
| deal | integer | Deal Value aplicável ao registro |
| sell_in1..5 | integer | Volume faturado por semana |
| one_plan_week1..5 | integer | Capacidade semanal (One Plan) |
| **allocation_W1..W5** | integer | **Volume final alocado pela IA, por semana do mês — saída principal do algoritmo** |
| allocation_alone_W1..W5 | integer | Alocação isolada por semana (sem efeito de compensações) |
| sell_in_comp_w1..5 | integer | Compensação de Sell-in (ajuste técnico de faturamento) |
| sell_in_lifetime, activations_lifetime, avg_activations | integer | Usados no cálculo do WOI |
| woi | real | WOI no momento da alocação |
| allocation_allowed | integer | 1 se o registro foi elegível para o cálculo da IA (0/1, não texto) |
| proj_woi_w1..w5 | real | WOI projetado, semana a semana, após aplicar a alocação |
| month_seq | integer | Posição do mês (1/2/3) dentro do grupo (quarter, material_id, key_account_id) |

---

## Grafo de relacionamentos

```
ka_input_data (1) ──────────────────── (1) ka_deal_allocation
    via: quarter = quarter AND material_id = material_id
         AND key_account_id = key_account_id AND month_seq = month_seq
    para que serve: comparar a demanda/capacidade de ENTRADA com o resultado computado pela IA
```

---

## Dimensões de análise disponíveis

**Tempo:** `quarter`, `year_month`, `month_seq` (1/2/3), `month_status` (`done`/`ongoing`/`next`)

**Key Account:** `key_account_code`, `key_account_id`

**Produto:** `material_id`, `product`, `product_group` (só em `ka_input_data`), `deal_group`, `origin`

**Risco de estoque:** `woi`, `proj_woi_w1..w5` (só em `ka_deal_allocation`)

**Volume:** `req_qty`, `deal`, `allocation_W1..W5`, `rollover`, `rollback`, `sell_in1..5`

**Elegibilidade:** `allocation_allowed` (1/0)

---

## Acesso a dados

Não há API REST para este domínio — todo acesso é via `executar_sql_alocacao` com SQL direto
sobre `ka_input_data` e `ka_deal_allocation`.
