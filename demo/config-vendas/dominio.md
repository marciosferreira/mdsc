# skill: dominio
# descricao: Análise de vendas por produto, região e período — faturamento, volume, rankings e tendências. Executa SQL na tabela vendas.
# palavras-chave: vendas, venda, faturamento, receita, produto, região, regiao, valor, ticket

---

## Regras do agente

### Período padrão

Os dados cobrem janeiro a junho de 2026 (coluna `data`, formato `YYYY-MM-DD`, granularidade
diária). Se o usuário não especificar período, use o dataset inteiro e diga isso na resposta.

## Regras do orquestrador

Este é um sistema de análise de vendas — não há alocação, WOI, produção nem pedidos de compra.
Se o usuário NÃO mencionar período nenhum, use calcular_periodo('todo o período') como padrão
e siga direto para consultar_analista — NUNCA pergunte o período ao usuário.

## Períodos

### re:todo o per[ií]odo|hist[oó]rico completo

```sql
SELECT MIN(data), MAX(data) FROM vendas
```

## Modelo de dados

### `vendas` — uma linha por venda realizada

| Coluna | Tipo | Significado |
|--------|------|-------------|
| id | INTEGER | Identificador da venda |
| produto | TEXT | Nome do produto vendido (Notebook, Mouse, Teclado, Monitor, Headset) |
| regiao | TEXT | Região da venda (Sul, Sudeste, Nordeste, Norte, Centro-Oeste) |
| data | TEXT | Data da venda, formato YYYY-MM-DD (jan a jun de 2026) |
| valor | REAL | Valor da venda em R$ |

### Exemplos de queries

```sql
-- Total de vendas por região
SELECT regiao, SUM(valor) AS total, COUNT(*) AS qtde
FROM vendas GROUP BY regiao ORDER BY total DESC;
```

## Domínio de negócio

Sistema simples de vendas de eletrônicos. Métricas usuais: faturamento (SUM(valor)),
volume (COUNT(*)), ticket médio (AVG(valor)). Dimensões: produto, região, mês
(strftime('%Y-%m', data)).

## Dica para condition_sql

Tabela disponível: `vendas` (colunas: produto, regiao, data, valor).
