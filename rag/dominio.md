# Domínio de negócio — KA Allocation

## O que é este sistema

Plataforma de análise e explicabilidade da alocação de supply (produto) por Key Account (KA),
calculada por um algoritmo de IA. O sistema não decide a alocação em si — ele expõe, de forma
rastreável, como a IA distribuiu o volume disponível entre os clientes estratégicos (KAs) a
partir de demanda (Request), acordos comerciais (Deal) e capacidade de estoque (Supply).

## Como a alocação é calculada (waterfall)

A IA processa o volume disponível em 3 etapas sequenciais, cada uma consumindo o que sobrou da anterior:

1. **Request** (demanda) — distribuído por ordem de prioridade (Score, ver abaixo)
2. **Deal** (acordo comercial) — só usa o volume remanescente após o Request
3. **Retail** — recebe o volume residual final

MMICOM (KA especial) não passa pela etapa de Deal — segue só Request/Score. Retail não usa WOI —
segue só Booked/Entered.

## WOI (Weeks of Inventory) e faixas de risco

```
woi = (sell_in_lifetime - activations_lifetime) / avg_activations
```

| Faixa | Classificação | Prioridade de alocação |
| --- | --- | --- |
| WOI = 0 | Ruptura grave (estoque esgotado) | Máxima |
| WOI < 10 | Crítico | Alta |
| 10 ≤ WOI < 15 | Risco médio | Moderada |
| WOI ≥ 15 | Fora de risco (saudável) | Menor |

## Score de priorização (0 a 7)

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

## Rollover e Rollback

- **Rollover**: demanda não atendida em períodos anteriores, transferida para o período atual —
  funciona como um incremento de demanda (aumenta o Request).
- **Rollback**: ajuste negativo aplicado ao Request — reduz a demanda planejada, libera supply.

## Glossário

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

## KPIs de Health Check

| Métrica | Como calcular |
|---------|---------------|
| Critical WOI | `COUNT(*) WHERE woi < 10` |
| Complete Request | `COUNT(*) WHERE soma das allocation_W1..5 >= req_qty` |
| Completed Deals | `COUNT(*) WHERE deal > 0 AND soma das allocation_W1..5 >= deal` |
| Rollover / Rollback | `COUNT(*) WHERE rollover > 0` / `COUNT(*) WHERE rollback > 0` |
| Rounded Allocations | `COUNT(*) WHERE allocation_W1 % 10 = 0` |

## Períodos e meses

O sistema trabalha com quarters (`FQ1`, `FQ2`, ...) e, dentro de cada quarter, 3 meses
identificados por `month_seq` (1/2/3), `month_status` (`done`, `ongoing` no quarter atual;
`next` no próximo quarter) e `year_month` (mês/ano confiável em ambas as tabelas).

**Não existe granularidade diária.** `year_month` é sempre o dia 1 do mês — o detalhamento
dentro do mês é por semana (`allocation_W1..W5`), não por data de calendário. Perguntas sobre
"alocação de hoje" só fazem sentido em termos de mês/semana corrente, nunca de um dia exato.
