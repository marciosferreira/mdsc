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

Tasks agendadas buscam dados **exclusivamente via `ctx.sql()`** — query SELECT direta no PostgreSQL (schema brazil). O retorno é sempre `list[dict]`; converta com `pd.DataFrame(rows)`.

```python
rows = ctx.sql(f"""
    SELECT po.status::text, COUNT(*) AS total
    FROM purchase_order po
    WHERE po.created_at::date BETWEEN '{from_date}' AND '{to_date}'
    GROUP BY po.status
""")
df = pd.DataFrame(rows)
```

> `ctx.api()` existe no namespace mas serve apenas para widgets do dashboard — não use em tasks.

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
| `ctx.sql('SELECT ...')` | list de dicts via SQL direto no PostgreSQL (schema brazil, só SELECT) |
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

| O usuário pediu | `date_range` correto |
|---|---|
| "do ano atual" / "do ano" | `ytd` |
| "do mês" / "do mês atual" | `mtd` |
| "últimos 30 dias" | `last_30d` |
| "últimos 7 dias" | `last_7d` |
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
    rows = ctx.sql(f"""
        SELECT
            po.created_at::date          AS data,
            po.status::text              AS status,
            COUNT(*)                     AS total_pedidos,
            SUM(oi.value_price_total)    AS valor_total
        FROM purchase_order po
        JOIN order_item oi ON oi.order_id = po.id
        WHERE po.created_at::date BETWEEN '{from_date}' AND '{to_date}'
        GROUP BY po.created_at::date, po.status
        ORDER BY data
    """)

    df = pd.DataFrame(rows)
    if df.empty:
        return ctx.generate_pdf('Relatório de Pedidos', '## Sem dados no período.')

    df['data']        = pd.to_datetime(df['data'])
    df['valor_total'] = df['valor_total'].astype(float)

    por_status = df.groupby('status').agg(
        pedidos=('total_pedidos', 'sum'),
        valor=('valor_total', 'sum'),
    ).reset_index()

    por_dia = df.groupby('data')['valor_total'].sum().reset_index()

    total_pedidos = df['total_pedidos'].sum()
    total_valor   = df['valor_total'].sum()
    aprovados     = por_status.loc[por_status['status'] == 'APPROVED', 'valor'].sum()

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    fig.suptitle(f'Pedidos — {from_date.strftime("%d/%m/%Y")} a {to_date.strftime("%d/%m/%Y")}',
                 fontsize=13, fontweight='bold')

    ax1 = axes[0]
    ax1.plot(por_dia['data'], por_dia['valor_total'], marker='o', color='#3b82f6', linewidth=2)
    ax1.set_title('Valor Total por Dia')
    ax1.set_ylabel('R$')
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    plt.setp(ax1.get_xticklabels(), rotation=45, ha='right')
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'R$ {x:,.0f}'))

    ax2 = axes[1]
    ax2.bar(por_status['status'], por_status['valor'], color='#60a5fa')
    ax2.set_title('Valor por Status')
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'R$ {x:,.0f}'))

    plt.tight_layout()
    chart = ctx.save_chart(fig)

    linhas = '\n'.join(
        f"| {r['status']} | {int(r['pedidos'])} | R$ {r['valor']:,.2f} |"
        for _, r in por_status.iterrows()
    )
    conteudo = (
        f"## Resumo\n\n{chart}\n\n"
        f"| Métrica | Valor |\n|---|---|\n"
        f"| Total de pedidos | {int(total_pedidos)} |\n"
        f"| Valor total | R$ {total_valor:,.2f} |\n"
        f"| Valor aprovado | R$ {aprovados:,.2f} |\n\n"
        f"## Por Status\n\n| Status | Pedidos | Valor |\n|---|---|---|\n{linhas}\n"
    )
    return ctx.generate_pdf('Relatório de Pedidos', conteudo)
```

### Planilha Excel — aba única

```python
def run(from_date, to_date, ctx):
    rows = ctx.sql(f"""
        SELECT po.id, po.status::text, po.created_at::date, c.name AS cliente
        FROM purchase_order po
        JOIN customer c ON c.id = po.customer_id
        WHERE po.created_at::date BETWEEN '{from_date}' AND '{to_date}'
    """)
    df = pd.DataFrame(rows)
    return ctx.generate_excel(df, 'pedidos')
```

### Planilha Excel — múltiplas abas

```python
def run(from_date, to_date, ctx):
    rows_po = ctx.sql(f"""
        SELECT po.id, po.status::text, po.created_at::date, c.name AS cliente
        FROM purchase_order po
        JOIN customer c ON c.id = po.customer_id
        WHERE po.created_at::date BETWEEN '{from_date}' AND '{to_date}'
    """)
    rows_itens = ctx.sql(f"""
        SELECT oi.order_id, oi.quantity, oi.value_price_total, oi.product_group::text
        FROM order_item oi
        JOIN purchase_order po ON po.id = oi.order_id
        WHERE po.created_at::date BETWEEN '{from_date}' AND '{to_date}'
    """)
    df_po    = pd.DataFrame(rows_po)
    df_itens = pd.DataFrame(rows_itens)
    return ctx.generate_excel(
        {'Pedidos': df_po, 'Itens': df_itens},
        'pedidos_detalhado',
    )
```

### Monitor com gatilho condicional (preferido)

> Para tarefas que só devem executar (e notificar) quando uma condição for atingida,
> use os parâmetros `condition_sql`, `condition_operator` e `condition_threshold` ao criar a tarefa.
> **Não escreva `ctx.notify()` no código** — a notificação é automática quando a condição é atingida.

Exemplos de criação via `schedule_task`:

```python
# Alerta se inconsistências > 50
condition_sql = "SELECT COUNT(*) FROM purchase_order WHERE status='INCONSISTENCY' AND created_at::date=CURRENT_DATE"
condition_operator = ">"
condition_threshold = 50

# Alerta se não houver vendas hoje
condition_sql = "SELECT id FROM purchase_order WHERE created_at::date = CURRENT_DATE"
condition_operator = "is_empty"

# Alerta se houver pedido atrasado
condition_sql = "SELECT id FROM order_item WHERE delivery_week < TO_CHAR(CURRENT_DATE,'IYYY-IW')"
condition_operator = "is_not_empty"
```

A notificação automática inclui o detalhe da condição: ex. "Monitor de inconsistências: 75 > 50".

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
# ERRADO — salvar sem testar
save_task_code(task_id, code)

# CERTO — testar primeiro, salvar só se passar
test_task_code(task_id, code)
save_task_code(task_id, code)   # só após teste bem-sucedido
```
