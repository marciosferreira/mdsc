# skill: dominio
# descricao: Análise de alocação de supply por Key Account (KA Allocation) — Request/Deal/Retail, Score de priorização, WOI, rollover/rollback, KPIs de Health Check. Executa SQL no banco de alocação (ka_input_data, ka_deal_allocation).
# palavras-chave: alocação, allocation, key account, KA, WOI, score, deal, request, retail, rollover, rollback, supply, site supply, health check, week supply, woi crítico, sell-in, booked, entered, one plan week

---

## Regras do agente

### Granularidade temporal — invariante crítico

`year_month` é SEMPRE o dia 1 do mês (ex: '2026-06-01') — representa o mês inteiro,
não um dia específico. Não existe dado por dia de calendário; o detalhamento dentro
do mês é por SEMANA (allocation_W1..W5, sell_in1..5, one_plan_week1..5).
Se o usuário pedir 'alocação de hoje' (ou qualquer data que não seja dia 1 de um mês),
NUNCA filtre por essa data específica nem responda como se existisse alocação para
aquele dia exato — isso é impossível dado o schema. Em vez disso, explique que a
granularidade é mensal (linhas sempre no dia 1) e semanal (W1-W5) dentro do mês,
e ofereça a alocação do mês corrente (month_status='ongoing') como alternativa.

### Período padrão sem especificação

WOI e outras métricas MUDAM entre quarters (mesmo produto+KA pode ter WOI bem
diferente em FQ1 vs FQ2), mas são constantes nos 3 meses de um mesmo quarter.
Se o usuário perguntar algo (ex: 'quais KAs têm WOI crítico') SEM especificar período,
assuma o quarter em andamento (`month_status IN ('done','ongoing')`), deixe explícito
na resposta qual quarter foi usado, e deduplique por KA (o valor se repete nos 3
meses). Só considere o próximo quarter ou compare os dois se o usuário pedir
explicitamente.
Ao citar o rótulo do quarter na resposta, NUNCA deduza — leia dos dados:
inclua `quarter` no SELECT (ou rode `SELECT DISTINCT quarter FROM ka_deal_allocation
WHERE month_status='ongoing'`) e use o valor retornado.

### Snapshot estático — o [PERÍODO] é uma DICA, não um filtro literal

Os dados são uma exportação estática: o 'agora' deles é o mês com
month_status='ongoing', que pode NÃO coincidir com a data de hoje. O prefixo
[PERÍODO: from=...&to=...] serve para rotular o período no texto/título — o filtro
SQL real deve usar as colunas dos dados (`quarter`, `month_status`, `year_month`).
ANTES de responder 'não há dados para o período', execute um
`SELECT quarter, month_status, MIN(year_month), MAX(year_month) FROM ka_deal_allocation
GROUP BY quarter, month_status` para ver o range real. Se o período pedido não
intersectar os dados, diga qual range existe e responda com o quarter em andamento,
deixando claro o ajuste. 'FQ1', 'FQ2' são valores LITERAIS da coluna `quarter`.

## Regras do orquestrador

Este NÃO é um sistema de chão-de-fábrica — não há OEE, FPY, produção ou linhas de
montagem, e NÃO é um sistema de pedidos de compra.

Períodos e quarters — regras deste domínio:
- Os dados são um SNAPSHOT estático: o 'agora' deles é o mês em andamento nos dados,
  que pode não coincidir com a data de hoje.
- 'FQ1', 'FQ2' etc. são RÓTULOS LITERAIS de quarter que existem nos dados —
  NUNCA peça ao usuário para converter em datas; passe direto para calcular_periodo
  (ex: calcular_periodo('FQ1')) e inclua o rótulo em `detalhes` de consultar_analista.
- Se o usuário NÃO mencionar período nenhum, use calcular_periodo('este quarter')
  como padrão — nunca invente um mês específico.

## Períodos

### re:\bfq\s*(\d)\b

```sql
SELECT MIN(year_month), date(MAX(year_month), '+1 month', '-1 day')
FROM ka_deal_allocation WHERE quarter = 'FQ' || :g1
```

### este mes | esse mes | este mês | esse mês | this month | mes corrente | mês corrente

```sql
SELECT MIN(year_month), date(MAX(year_month), '+1 month', '-1 day')
FROM ka_deal_allocation WHERE month_status = 'ongoing'
```

### re:(pr[oó]xim|seguinte|que vem|vindouro|next).*(quarter|trimestre)|(quarter|trimestre).*(seguinte|que vem|vindouro)

```sql
SELECT MIN(year_month), date(MAX(year_month), '+1 month', '-1 day')
FROM ka_deal_allocation WHERE month_status = 'next'
```

### re:quarter|trimestre

```sql
SELECT MIN(year_month), date(MAX(year_month), '+1 month', '-1 day')
FROM ka_deal_allocation WHERE month_status IN ('done', 'ongoing')
```

## Modelo de dados

### ⚠️ Colunas com semântica especial — leia antes de escrever qualquer SQL

| Coluna | Tabela | Observação |
| --- | --- | --- |
| `year_month` | ambas | Confiável em ambas as tabelas. O arquivo de origem de `ka_deal_allocation` vinha com essa coluna corrompida (bug de exportação, colapsava para ~1969-12-31) — o valor foi corrigido no momento da carga (`load_ka_allocation.py`), usando o `year_month` de `ka_input_data` via join em `(quarter, material_id, key_account_id, month_seq)`. |
| `month_seq` | ambas | Posição do mês (1/2/3) dentro do grupo `(quarter, material_id, key_account_id)`, na ordem original do arquivo — útil para ordenar sem depender de `year_month`. |
| `month_status` | ambas | `done`/`ongoing` = meses do quarter atual (sempre nessa ordem: 2× `done`, depois `ongoing`); `next` = os 3 meses do próximo quarter. |
| `allocation_allowed` | `ka_deal_allocation` | Armazenada como INTEGER (1/0), não texto `"true"/"false"`. |

### Regras críticas de SQL

| Regra | Como aplicar |
|-------|-------------|
| Apenas SELECT | Qualquer outro comando será rejeitado |
| Sem SELECT * | Liste sempre as colunas necessárias |
| Tabelas | `ka_input_data` (entrada do algoritmo) e `ka_deal_allocation` (resultado computado pela IA) |
| Ordenar/filtrar por mês | `year_month` é confiável em ambas as tabelas; `month_seq` (1/2/3) + `month_status` também servem para ordenar sem depender de data |
| Booleanos | `allocation_allowed`, `current_quarter` são INTEGER 0/1 |

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
| year_month | Mês/ano do registro |
| month_status | `done` (mês fechado do quarter atual), `ongoing` (mês corrente) ou `next` (quarter seguinte) |
| entered_quarter | Volume "Entered" (intenção de pedido) do quarter — ver Score |
| booked_quarter | Volume "Booked" (reservado/confirmado) do quarter — ver Score |
| user_allocation1..5 | Alocação manual definida pelo usuário, por semana (1 a 5) do mês |
| sell_in1..5 | Volume faturado por semana |
| one_plan_week1..5 | Capacidade semanal definida no One Plan (limite de supply da semana) |
| req_qty | Request final considerado pela IA (Initial Request + Rollover − Rollback) |
| init_req_qty | Request inicial, antes de ajustes de Rollover/Rollback |
| deal | Valor do acordo comercial (Deal Value) aplicável ao registro |
| sell_in_lifetime | Total acumulado de unidades faturadas (usado no cálculo do WOI) |
| activations_lifetime | Total acumulado de unidades ativadas (usado no cálculo do WOI) |
| avg_activations | Média de ativações por semana (usado no cálculo do WOI) |
| woi | Weeks of Inventory — ver fórmula no domínio de negócio |
| month_seq | Derivada no load — posição do mês (1/2/3) dentro do grupo (quarter, material_id, key_account_id) |

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
| month_seq | Derivada no load — posição do mês (1/2/3) dentro do grupo (quarter, material_id, key_account_id) |

### Grafo de relacionamentos

```
ka_input_data (1) ──→ (1) ka_deal_allocation
  JOIN: quarter = quarter AND material_id = material_id
        AND key_account_id = key_account_id AND month_seq = month_seq
  Para: comparar a demanda/capacidade de ENTRADA com o resultado computado pela IA
```

### KPIs do Health Check — tradução para SQL

| KPI | Padrão SQL (sobre `ka_deal_allocation`) |
| --- | --- |
| Critical WOI | `COUNT(*) WHERE woi < 10` |
| Input Data Inconsistencies | `COUNT(*) WHERE allocation_W1 < 0 OR ... OR allocation_W5 < 0` |
| Rounded Allocations (blocos de 10) | `COUNT(*) WHERE allocation_W1 % 10 = 0` (repetir por semana ou considerar o total mensal) |
| Complete Request | `COUNT(*) WHERE (allocation_W1+allocation_W2+allocation_W3+allocation_W4+allocation_W5) >= req_qty` |
| Rollover / Rollback | `COUNT(*) WHERE rollover > 0` / `COUNT(*) WHERE rollback > 0` |
| Completed Deals | `COUNT(*) WHERE deal > 0 AND (soma das allocation_W1..5) >= deal` |

⚠️ **Ressalva**: "Week Supply Violation" (capacidade semanal excedida) e "Site Supply Occurrences" (redistribuição entre JAG/MAN) exigiriam comparar a soma de todas as KAs numa mesma semana contra `one_plan_week*`, ou dados de site não presentes nestas duas tabelas — trate essas duas métricas como aproximações e deixe explícito na resposta que a precisão total do KPI original (tela Health Check) depende de dados agregados que essas tabelas planas não guardam sozinhas.

### Exemplos de queries

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

## Domínio de negócio

### O que é este sistema

Plataforma de análise e explicabilidade da alocação de supply (produto) por Key Account (KA),
calculada por um algoritmo de IA. O sistema não decide a alocação em si — ele expõe, de forma
rastreável, como a IA distribuiu o volume disponível entre os clientes estratégicos (KAs) a
partir de demanda (Request), acordos comerciais (Deal) e capacidade de estoque (Supply).

### Como a alocação é calculada (waterfall)

A IA processa o volume disponível em 3 etapas sequenciais, cada uma consumindo o que sobrou da anterior:

1. **Request** (demanda) — distribuído por ordem de prioridade (Score, ver abaixo)
2. **Deal** (acordo comercial) — só usa o volume remanescente após o Request
3. **Retail** — recebe o volume residual final

MMICOM (KA especial) não passa pela etapa de Deal — segue só Request/Score. Retail não usa WOI —
segue só Booked/Entered.

### WOI (Weeks of Inventory) e faixas de risco

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

### Score de priorização (0 a 7)

Dentro da etapa de Request, cada KA é classificado num Score que determina a ordem de
atendimento — Score 0 é atendido primeiro, Score 7 só recebe se ainda sobrar supply:

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

Em cenário de escassez, apenas Score 0 e 1 tendem a ser atendidos completamente — scores
maiores só recebem se ainda sobrar supply. O Score não é uma coluna armazenada nas tabelas;
para estimá-lo numa análise, combine `woi`, `booked_quarter` e `entered_quarter` conforme a
tabela acima.

### Rollover e Rollback

- **Rollover**: demanda não atendida em períodos anteriores, transferida para o período atual —
  funciona como um incremento de demanda (aumenta o Request).
- **Rollback**: ajuste negativo aplicado ao Request — reduz a demanda planejada, libera supply.

### Glossário

| Termo | Significado |
| --- | --- |
| KA | Key Account, cliente estratégico |
| WOI | Weeks of Inventory — semanas de cobertura de estoque |
| Rollover | Demanda não atendida transferida para o período atual |
| Rollback | Ajuste negativo aplicado ao Request |
| Allocation | Volume distribuído para o KA |
| Deal | Acordo comercial, definido por quarter |
| Supply | Volume em estoque disponível para alocação |
| Booked | Volume já reservado/confirmado comercialmente no quarter |
| Entered | Volume em intenção de reserva/pedido em andamento |
| Request | Volume de demanda considerado pela IA |
| Sell-in | Volume efetivamente faturado |

### Períodos e meses

O sistema trabalha com quarters (`FQ1`, `FQ2`, ...) e, dentro de cada quarter, 3 meses
identificados por `month_seq` (1/2/3), `month_status` (`done`, `ongoing` no quarter atual;
`next` no próximo quarter) e `year_month` (mês/ano confiável em ambas as tabelas).

**Não existe granularidade diária.** `year_month` é sempre o dia 1 do mês — o detalhamento
dentro do mês é por semana (`allocation_W1..W5`), não por data de calendário. Perguntas sobre
"alocação de hoje" só fazem sentido em termos de mês/semana corrente, nunca de um dia exato.

## Exemplos task_code

### Relatório PDF com gráfico

```python
def run(from_date, to_date, ctx):
    rows = ctx.sql("""
        SELECT
            key_account_code,
            woi,
            (allocation_W1 + allocation_W2 + allocation_W3 + allocation_W4 + allocation_W5) AS alocado
        FROM ka_deal_allocation
        WHERE month_status IN ('done', 'ongoing')
    """)

    df = pd.DataFrame(rows)
    if df.empty:
        return ctx.generate_pdf('Relatório de Alocação', '## Sem dados no período.')

    por_ka = df.groupby('key_account_code').agg(
        alocado=('alocado', 'sum'),
        woi_medio=('woi', 'mean'),
    ).reset_index()

    total_alocado = df['alocado'].sum()
    kas_criticos  = df[df['woi'] < 10]['key_account_code'].nunique()

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f'Alocação — {from_date.strftime("%d/%m/%Y")} a {to_date.strftime("%d/%m/%Y")}',
                 fontsize=13, fontweight='bold')

    ax1 = axes[0]
    ax1.bar(por_ka['key_account_code'], por_ka['alocado'], color='#3b82f6')
    ax1.set_title('Alocação Total por Key Account')
    plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')

    ax2 = axes[1]
    ax2.bar(por_ka['key_account_code'], por_ka['woi_medio'], color='#f87171')
    ax2.set_title('WOI Médio por Key Account')
    plt.setp(ax2.get_xticklabels(), rotation=45, ha='right')

    plt.tight_layout()
    chart = ctx.save_chart(fig)

    linhas = '\n'.join(
        f"| {r['key_account_code']} | {r['alocado']:,.0f} | {r['woi_medio']:.1f} |"
        for _, r in por_ka.iterrows()
    )
    conteudo = (
        f"## Resumo\n\n{chart}\n\n"
        f"| Métrica | Valor |\n|---|---|\n"
        f"| Total alocado | {total_alocado:,.0f} |\n"
        f"| KAs com WOI crítico | {kas_criticos} |\n\n"
        f"## Por Key Account\n\n| KA | Alocado | WOI médio |\n|---|---|---|\n{linhas}\n"
    )
    return ctx.generate_pdf('Relatório de Alocação', conteudo)
```

### Planilha Excel — aba única

```python
def run(from_date, to_date, ctx):
    rows = ctx.sql("""
        SELECT key_account_code, product, quarter, month_seq, woi,
               allocation_W1, allocation_W2, allocation_W3, allocation_W4, allocation_W5
        FROM ka_deal_allocation
        WHERE month_status IN ('done', 'ongoing')
    """)
    df = pd.DataFrame(rows)
    return ctx.generate_excel(df, 'alocacao')
```

### Planilha Excel — múltiplas abas

```python
def run(from_date, to_date, ctx):
    rows_input = ctx.sql("""
        SELECT key_account_code, product, quarter, month_seq, req_qty, woi
        FROM ka_input_data
        WHERE month_status IN ('done', 'ongoing')
    """)
    rows_output = ctx.sql("""
        SELECT key_account_code, product, quarter, month_seq,
               allocation_W1, allocation_W2, allocation_W3, allocation_W4, allocation_W5
        FROM ka_deal_allocation
        WHERE month_status IN ('done', 'ongoing')
    """)
    df_input  = pd.DataFrame(rows_input)
    df_output = pd.DataFrame(rows_output)
    return ctx.generate_excel(
        {'Entrada': df_input, 'Alocação': df_output},
        'alocacao_detalhado',
    )
```

### Exemplos de condition_sql para monitores

```python
# Alerta se KAs com WOI crítico > 10
condition_sql = "SELECT COUNT(DISTINCT key_account_code) FROM ka_deal_allocation WHERE woi < 10"
condition_operator = ">"
condition_threshold = 10

# Alerta se não houver nenhum deal completo no quarter atual
condition_sql = "SELECT id FROM ka_deal_allocation WHERE deal > 0 AND month_status = 'ongoing' LIMIT 1"
condition_operator = "is_not_empty"

# Alerta se houver rollback aplicado
condition_sql = "SELECT id FROM ka_deal_allocation WHERE rollback > 0 LIMIT 1"
condition_operator = "is_not_empty"
```

## Dica para condition_sql

Tabelas disponíveis: `ka_input_data`, `ka_deal_allocation` (colunas: key_account_code,
material_id, quarter, month_seq, month_status, woi, allocation_W1..W5, rollover, rollback).
