# skill: task_code_sandbox
# descricao: Regras e template obrigatórios para escrever task_code — namespace do sandbox, variáveis pré-injetadas, proibições e exemplos
# palavras-chave: task_code, sandbox, run, imports, namespace, ctx, pd, plt, np

---

## Workflow obrigatório

**Sempre nesta ordem — nunca salve sem testar:**

1. **Escrever** o código com `def run(from_date, to_date, ctx)`
2. **Testar** com `test_task_code(task_id, code)` — valida sintaxe, executa e mostra o artifact no chat
3. **Salvar** com `save_task_code(task_id, code)` **somente após teste bem-sucedido**

Após `save_task_code`, o daemon executa o código diretamente no horário agendado, sem LLM.

---

## Regra principal

**NUNCA use `import` dentro de `run()` nem fora dela.**
Todas as bibliotecas já estão no namespace — qualquer `import` causa erro imediato.

---

## Como buscar dados

Tasks agendadas buscam dados **exclusivamente via `ctx.sql()`** — query SELECT direta no SQLite de alocação (tabelas `ka_input_data` e `ka_deal_allocation`). O retorno é sempre `list[dict]`; converta com `pd.DataFrame(rows)`.

```python
rows = ctx.sql(f"""
    SELECT key_account_code, COUNT(*) AS total
    FROM ka_deal_allocation
    WHERE woi < 10
    GROUP BY key_account_code
""")
df = pd.DataFrame(rows)
```

> `ctx.api()` existe no namespace mas serve apenas para o endpoint `/alerts` (sino de notificações) — não use em tasks de alocação.

`year_month` é confiável em ambas as tabelas; `month_seq` (1/2/3) + `month_status` (`done`/`ongoing`/`next`) também servem para ordenar meses dentro de um quarter.

---

## Variáveis pré-injetadas no namespace

| Variável / Símbolo | O que é |
|---|---|
| `pd` | pandas |
| `np` | numpy |
| `plt` | matplotlib.pyplot |
| `mticker` | matplotlib.ticker |
| `mdates` | matplotlib.dates — use `mdates.DateFormatter('%d/%m')` para formatar eixo de datas |
| `openpyxl` | openpyxl (módulo) |
| `Font`, `PatternFill`, `Alignment`, `Border`, `Side` | openpyxl.styles |
| `get_column_letter` | openpyxl.utils |
| `date`, `datetime`, `timedelta` | do módulo datetime |
| `time`, `math`, `json`, `re` | stdlib leve (pré-injetados) |
| `Counter`, `defaultdict` | collections (pré-injetados) |
| `from_date`, `to_date` | objetos `date` — janela de execução do daemon (veja regra abaixo) |
| `ctx` | TaskContext — métodos abaixo |

### Métodos do ctx

| Chamada | Retorna |
|---|---|
| `ctx.sql('SELECT ...')` | list de dicts via SQL direto no SQLite de alocação (só SELECT) |
| `ctx.today()` | string YYYY-MM-DD com a data atual |
| `ctx.date_range(days=N)` | `(from_date, to_date)` dos últimos N dias |
| `ctx.save_chart(fig)` | token `[chart:uuid]` |
| `ctx.generate_excel(df, 'nome_arquivo')` | token `[excel:uuid]` — aba única chamada "Dados" |
| `ctx.generate_excel({'Aba1': df1, 'Aba2': df2}, 'nome_arquivo')` | token `[excel:uuid]` — múltiplas abas |
| `ctx.generate_pdf('Título', 'conteudo')` | token `[pdf:uuid]` |
| `ctx.notify(msg, value=None, threshold=None)` | dispara notificação no dashboard |

---

## Regra: date_range vs from_date/to_date

`from_date` e `to_date` são calculados pelo daemon a partir do **`date_range`** da tarefa.
Se `date_range` não estiver definido, usa a janela padrão da frequência:

| `date_range` | Janela injetada |
|---|---|
| `ytd` | 1 jan do ano atual → hoje |
| `mtd` | 1º do mês atual → hoje |
| `today` | hoje → hoje |
| `last_7d` | 7 dias atrás → hoje |
| `last_30d` | 30 dias atrás → hoje |
| `last_90d` | 90 dias atrás → hoje |
| *(não definido)* | janela padrão da frequência (daily=1d, weekly=7d, monthly=30d, every_Xm=1d) |

**Sempre que o usuário especificar um intervalo de análise, defina `date_range` ao criar a tarefa.**
O task_code usa `from_date`/`to_date` normalmente — o daemon garante os valores corretos.
Como a granularidade das tabelas de alocação é por quarter/mês (não por data de calendário),
`from_date`/`to_date` tipicamente servem para rotular o período no título/conteúdo do relatório,
e os filtros reais de dados usam `quarter`/`month_status`/`month_seq` (ou `year_month`).

| O usuário pediu | `date_range` correto |
|---|---|
| "do ano atual" / "do ano" | `ytd` |
| "do mês" / "do mês atual" | `mtd` |
| "últimos 30 dias" | `last_30d` |
| "de hoje" | `today` |
| "relatório diário" | *(não definir — usa padrão da frequência)* |

> **NUNCA** calcule o intervalo dentro do task_code com `ctx.today()` para substituir `date_range`. Defina `date_range` na tarefa e use `from_date`/`to_date` no código.
>
> ⚠️ **Ao testar**: `test_task_code(task_id, code)` sem `from_date`/`to_date` usa por padrão
> "últimos 7 dias" — isso NÃO reflete o `date_range` real da tarefa. Para tarefas com
> `date_range='today'`, `'mtd'` ou `'ytd'`, passe explicitamente `from_date`/`to_date`
> equivalentes ao `date_range` (ex: `from_date=to_date=hoje` para `'today'`) para que
> o resultado do teste corresponda ao que será gerado em produção. Caso contrário, o
> teste pode mostrar dados de um dia/período diferente do esperado, mesmo que o código
> esteja correto.

---

## Templates canônicos

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

### Monitor com gatilho condicional (preferido)

> Para tarefas que só devem executar (e notificar) quando uma condição for atingida,
> use os parâmetros `condition_sql`, `condition_operator` e `condition_threshold` ao criar a tarefa.
> **Não escreva `ctx.notify()` no código** — a notificação é automática quando a condição é atingida.
> `condition_sql` roda em **dialeto SQLite** — use `date('now')`, nunca `CURRENT_DATE`/`::text`/`TO_CHAR`.

Exemplos de criação via `schedule_task`:

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

A notificação automática inclui o detalhe da condição: ex. "Monitor de WOI crítico: 12 > 10".

---

## Notificações automáticas

Quando a tarefa tem `notify=True`, o runner dispara automaticamente uma notificação com o nome da tarefa ao final de cada execução bem-sucedida — **sem precisar de `ctx.notify()` no código**.

**PROIBIDO usar `ctx.notify()` no task_code para implementar condições de threshold.**
Se o objetivo é "alertar quando X > N", use `condition_sql` + `condition_operator` + `condition_threshold` na tarefa.
O sistema bloqueia o `save_task_code` se detectar `ctx.notify()` em tarefas que já têm `condition_sql`.

## Monitores (every\_Xm / every\_Xh)

Monitores DEVEM sempre retornar uma string com o valor atual, mesmo quando o threshold não for atingido.

---

## Erros comuns — NÃO faça isso

```python
# ERRADO — ctx.notify() sem o usuário ter pedido alertas
def run(from_date, to_date, ctx):
    ...
    ctx.notify('Gráfico gerado')   # proibido em tarefas de relatório/gráfico

# CERTO — ctx.notify() só quando notify=True foi definido na criação da tarefa
# e o usuário pediu monitoramento/alertas explicitamente
```

```python
# ERRADO — import dentro do run() causa ImportError
def run(from_date, to_date, ctx):
    import pandas as pd   # proibido — use pd diretamente
```

```python
# ERRADO — nunca retorne a figura diretamente
def run(from_date, to_date, ctx):
    fig, ax = plt.subplots()
    return fig   # use ctx.save_chart(fig)
```

```python
# ERRADO — ha= não existe em tick_params
ax.tick_params(axis='x', rotation=45, ha='right')

# CERTO
plt.setp(ax.get_xticklabels(), rotation=45, ha='right')
```

```python
# ERRADO — dialeto Postgres não existe no SQLite de alocação
rows = ctx.sql("SELECT status::text FROM ka_deal_allocation WHERE created_at::date = CURRENT_DATE")

# CERTO — dialeto SQLite, sem cast, usando as colunas reais da tabela
rows = ctx.sql("SELECT key_account_code FROM ka_deal_allocation WHERE month_status = 'ongoing'")
```

```python
# ERRADO — salvar sem testar
save_task_code(task_id, code)

# CERTO — testar primeiro, salvar só se passar
test_task_code(task_id, code)
save_task_code(task_id, code)   # só após teste bem-sucedido
```
