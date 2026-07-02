**W23004 - SW - MDSC - FUNCTIONAL SPECIFICATION**

**GCA - USE CASE [00X] – AI KA Allocation Distribution Explainability**

SUMÁRIO

########### 

**1.	INFORMAÇÕES GERAIS	2**

**2.	CONTROLE DE REVISÕES	3**

**3.	ACRÔNIMO, ABREVIATURAS E SINÔNIMOS	4**

**4.	PRÉ-CONDIÇÃO	5**

**5.	REQUISITOS FUNCIONAIS	6**

**5.1	Descrição	6**

**5.2	Fluxo Principal	10**

**5.3	Regras de Negócio	19**

**5.4	Fluxo Alternativo	30**

**5.5	Critérios de Aceitação	31**

**5.6	Matriz de Rastreabilidade	37**

**6.	APROVAÇÕES	40**

## 1 INFORMAÇÕES GERAIS

| **Nome do projeto:**     | W23004 – GCA Global Customer Allocation  Frente: GCA KA AI Distribution                                                                                                                                                                                            |
|--------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Resumo da meta:**      | Prover uma solução de  **Explainability AI**  para o processo de distribuição de alocações, realizada pela IA, por Key Account (KA), garantindo transparência, rastreabilidade e compreensão completa da lógica de cálculo utilizada pela inteligência artificial. |
| **Área do projeto:**     | 02-Software                                                                                                                                                                                                                                                        |
| **Cliente:**             | Motorola Mobility Brasil                                                                                                                                                                                                                                           |
| **Gerente de Programa:** | Lara Goulart                                                                                                                                                                                                                                                       |
| **Gerente de Projeto:**  | Luciano Ferreira                                                                                                                                                                                                                                                   |
| **Coordenação Técnica:** | Guilherme Novelleto                                                                                                                                                                                                                                                |

## 2 CONTROLE DE REVISÕES

|   **Versão** | **Data**   | **Autor**       | **Comentários**      |
|--------------|------------|-----------------|----------------------|
|          1.0 | 30/06/2026 | Kamila Pimentel | Criação do documento |
|              |            |                 |                      |
|              |            |                 |                      |
|              |            |                 |                      |
|              |            |                 |                      |
|              |            |                 |                      |
|              |            |                 |                      |
|              |            |                 |                      |

## 3 ACRÔNIMO, ABREVIATURAS E SINÔNIMOS

| **KA**         | Key Account, cliente estratégico.                                                                                                                   |
|----------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| **WOI**        | Weeks of Inventory, quantidade de semanas de inventário disponível.                                                                                 |
| **Rollover**   | Volume transferido de períodos anteriores para meses futuros.                                                                                       |
| **Rollback**   | Volume antecipado de meses futuros com ajustes negativos na demanda.                                                                                |
| **Allocation** | Distribuição de volume.                                                                                                                             |
| **Deal**       | Acordos comerciais, definidos por quarter.                                                                                                          |
| **Supply**     | Volume em estoque disponível para alocação, relacionado à capacidade de atendimento.                                                                |
| **Booked**     | Booked representa o volume de produto já reservado e confirmado comercialmente (pedido) para uma Key Account (KA) dentro de um determinado quarter. |
| **Entered**    | Entered representa o volume de produto registrado como intenção de reserva ou pedido em andamento, também considerando o período do quarter.        |
| **Request**    | Volume solicitado pelo cliente, relacionado à demanda.                                                                                              |
| **Sell-in**    | Volume que foi efetivamente faturado (vendido para o cliente).                                                                                      |

## 4 PRÉ-CONDIÇÃO

- Usuário deve estar autenticado no sistema.
- Usuário com permissão para visualizar resultados de distribuição.
- Deve existir pelo menos uma versão de alocação (DRAFT ou PUBLISH) gerada pelo modelo de IA.
- Os dados de Request, Deal e Supply devem estar carregados e disponíveis no sistema.
- O Sistema deve possuir dados referente ao quarter  atual e o próximo.

## 5 REQUISITOS FUNCIONAIS

### 5.1 Descrição

O sistema deve permitir a visualização detalhada e explicável dos resultados de distribuição de alocação por Key Account (KA), garantindo total , rastreabilidade e compreensão do processo de cálculo realizado pela inteligência artificial.

A visualização dos resultados deve ser disponibilizada por meio de duas funcionalidades complementares:

- Allocation Breakdown – visão operacional da alocação;
- Health Check – visão executiva da alocação.

A solução deve permitir que o usuário entenda como a alocação foi construída, considerando:

- Request;
- Rollover;
- Rollback;
- Supply;
- Site Supply;
- Deal e suas proporções;

Compreenda os fatores que influenciaram a distribuição dos volumes para cada Key Account, considerando:

- WOI (Weeks of Inventory);
- Booked;
- Entered;
- Regras de capacidade e restrições operacionais;

Visualize os resultados da alocação em dois níveis de análise:

- Allocation Breakdown: detalhamento operacional dos dados e componentes utilizados no cálculo da alocação;
- Health Check: indicadores, dashboards e KPIs para avaliação da qualidade e consistência dos resultados.

Além disso, a solução deve:

- Permitir a navegação entre diferentes versões de alocação;
- Permitir segmentação dos dados por filtros e períodos;
- Garantir rastreabilidade dos resultados apresentados;
- Disponibilizar informações suficientes para validação da alocação antes da publicação da versão.

A solução também deve possibilitar a análise dos impactos causados por fatores como:

- Supply insuficiente;
- Ajustes de Sell-In;
- Redistribuição por Site Supply;
- Aplicação de Rollover;
- Aplicação de Rollback;
- Atendimento de Deals comerciais.

**Figura 1 - Tela Allocation Breakdown “Request Allocation Details”**

<!-- image -->

**Figura 2 - Tela Allocation Breakdown “Deal Allocation Details”**

<!-- image -->

**Figura 3 - Tela Allocation Breakdown “Request + Deal Allocation Details”**

<!-- image -->

Figura 4 - Tela “Health Check”

<!-- image -->

Figura 4 - Tela “Health Check”

<!-- image -->

<!-- image -->

Link Figma – Allocation Breakdown : [2024 | GCA Brazil / Visual Design – Figma](https://www.figma.com/design/UN8a2TEnk1u2U4PToOCQFd/2024-%7C-GCA-Brazil---Visual-Design?node-id=40834-109939&t=clwY9cZ6YO95TwvI-0)

Link Figma – Health Check : [2024 | GCA Brazil / Visual Design - Prototype](https://www.figma.com/proto/UN8a2TEnk1u2U4PToOCQFd/2024-%7C-GCA-Brazil---Visual-Design?node-id=41324-91901&viewport=-50315%2C3078%2C0.66&t=IT7BjY97blcj3m9V-1&scaling=scale-down-width&content-scaling=fixed&starting-point-node-id=20449%3A82801&page-id=0%3A1)

### 5.2 Fluxo Principal

1. O usuário acessa a funcionalidade clicando na opção menu *Home → KA AI DISTRIBUTION→ ALLOCATION BREAKDOWN ou HEALTH CHECK.*
2. O sistema apresenta as duas opções de análise disponíveis:

- Allocation Breakdown (visão operacional)
- Health Check (visão executiva)

1. **Allocation Breakdown** : O sistema carrega automaticamente a ultima versão de alocação previamente gerada pela funcionalidade KA AI Distribution.
- 1.1. Versão selecionada, o sistema carrega a tela de análise executiva contendo:
- 1.2. Abas de navegação:
- 1.2.2. Deal
- 1.2.3. Request + Deal
- 1.4. Tabela com os dados de alocação, onde o usuário pode:
- 1.4.2. Selecionar o mês desejado
- 1.4.3. Aplicar filtros obrigatórios conforme a aba
- 1.5.2. Aba ativa
- 1.5.3. Mês selecionado
- 1.5.4. Filtros aplicados
- 1.6.2. Rollover e Rollback
- 1.6.3. Supply disponível
- 1.6.4. Proporções do Deal
- 1.6.5. Indicadores como WOI e Score
- 1.6.6. Identificação da alocação realizada pela IA
2. O usuário seleciona a opção Health Check.
3. **Health Check :** O sistema carrega automaticamente a última versão de alocação gerada pela IA. O usuário também pode modificar a versão que deseja exibir/analisar, e então o sistema carrega a tela de análise detalhada contendo:
    - 3.1. Versão selecionada.
    - 3.2. Exibição da tela de análise executiva contendo:
        - 3.2.1. Dashboards visuais
        - 3.2.2. Indicadores de performance (KPIs)
        - 3.2.3. Comparações entre resultados da IA (e opcionalmente usuário)
    - 3.3. O sistema apresenta métricas consolidadas, tais como:
        - 3.3.1. Qualidade da alocação
        - 3.3.2. Percentual de atendimento de Request e Deal
        - 3.3.3. Indicadores de WOI crítico
        - 3.3.4. Consumo de Supply
        - 3.3.5. Inconsistências de dados
4. Acesso Alternativo: Após executar uma nova distribuição na funcionalidade KA AI Distribution, o usuário poderá acessar diretamente as telas Allocation Breakdown ou Health Check para analisar os resultados da versão recém-gerada antes da sua publicação (FA\_xx e FA\_xx).
5. O usuário visualiza as telas para validação e análise da alocação antes da publicação da alocação realizada pela IA.

Se desejar, o usuário pode modificar a versão para exibir/analisar e então o sistema carrega a tela de análise detalhada contendo:

- 1.2.1. Request

- 1.4.1. Navegar entre as abas

- 1.5.1. Versão selecionada

- 1.6.1. Valores de Request, Deal e Retail

- 1.1.1. Aplicação de filtros

1. Tela **Allocation Breakdown**

O usuário aplica os filtros **obrigatórios** conforme o cenário:

- Aba Request: Quarter, Produto e Origem.
- Aba Deal: Quarter, Deal Group e KA.
- Aba Request + Deal : Quarter, Produto e Origem.

Caso o usuário ache necessário, aplica os filtros **opcionais** conforme o cenário:

- Aba Request: Month, KA.
- Aba Deal: Product, Month, origin.
- Aba Request + Deal: Month, KA.

O sistema valida os filtros obrigatórios e carrega o dataset filtrado.

1. **Tela Health Check**

Esta tela não possui filtros obrigatórios para dashboards ou KPIs. A utilização dos filtros é opcional e deve ser realizada conforme a necessidade do usuário. Para análise dos dados apresentados tabela **Product Level Validation Breakdown** , é obrigatório realizar o filtro de Key Account ou Product, devido grande volume de dados apresentados.

Os filtros ficarão disponíveis, conforme:

- **Request Fulfillment Dashboard:** permite a aplicação de filtros por Product.
- **Product Level Validation Breakdown:** filtro obrigatório de visualização por Key Account ou Product.

- 1.1.1. Tabela de Dados

A tabela permite que as informações sejam apresentadas de forma estruturada e organizada, facilitando a visualização e a compreensão dos dados exibidos nos campos. Isso ajuda os usuários a localizar rapidamente as informações que precisam.

1. Tela **Allocation Breakdown**
| **Aba Request**         |                                                                                                                                                         |                                        |             |
|-------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------|-------------|
| **Campo**               | **Descrição**                                                                                                                                           | **Tamanho Máximo**                     | **Formato** |
| **Product**             | Identificação do produto considerado no processo de alocação.                                                                                           | 100 caracteres                         | Texto       |
| **KA**                  | Identificação da Key Account (cliente) para o qual a alocação está sendo calculada.                                                                     | 50 caracteres                          | Texto       |
| **Origin**              | Local de origem do produto (JAG ou MAN).                                                                                                                | 10 caracteres                          | Texto       |
| **Month Allocation**    | Volume total alocado para o mês correspondente, considerando a soma das alocações semanais.                                                             | Numérico (inteiro)                     | Number      |
| **Week Allocation**     | Volume alocado para a semana específica dentro do mês.                                                                                                  | Numérico (inteiro)                     | Number      |
| **Allocation**          | Volume total alocado para o KA no contexto da linha (produto, origem e período), considerando o resultado do processamento da IA.                       | Numérico (inteiro)                     | Number      |
| **Initial Request**     | Volume inicial de demanda informado antes da aplicação de ajustes de planejamento.                                                                      | Numérico (inteiro)                     | Number      |
| **Request**             | Volume final de demanda considerado no cálculo da IA, composto por Initial Request ajustado por Rollover e Rollback.                                    | Numérico (inteiro)                     | Number      |
| **Rollover**            | Volume de demanda transferido de períodos anteriores.                                                                                                   | Numérico (inteiro)                     | Number      |
| **Rollback**            | Ajuste negativo aplicado à demanda planejada.                                                                                                           | Numérico (inteiro)                     | Number      |
| **Booked**              | Volume de produto reservado e confirmado comercialmente para a KA, definido por quarter e com alta prioridade na alocação.                              | Numérico (inteiro)  Numérico (inteiro) | Number      |
| **Entered**             | Volume de produto registrado como intenção de reserva ou pedido em andamento para a KA, definido por quarter e com prioridade inferior ao Booked.       | Numérico (inteiro)                     | Number      |
| **WOI**                 | Indicador de Weeks of Inventory que representa a projeção de semanas de cobertura de estoque para o KA e produto, utilizado na priorização da alocação. | Decimal (até 2 casas)                  | Number      |
|                         |                                                                                                                                                         |                                        |             |
| **Aba Deal**            |                                                                                                                                                         |                                        |             |
| **Campo**               | **Descrição**                                                                                                                                           | **Tamanho Máximo**                     | **Formato** |
| **Product**             | Produto associado ao acordo comercial (Deal).                                                                                                           | 100 caracteres                         | Texto       |
| **Origin**              | Origem do produto considerada dentro do acordo (JAG ou MAN).                                                                                            | 10 caracteres                          | Texto       |
| **Deal Value**          | Volume total acordado no Deal para o período analisado.                                                                                                 | Numérico (inteiro)                     | Number      |
| **Deal Allocation**     | Volume total alocado pela IA no Deal para o registro e período analisado.                                                                               | Numérico (inteiro)                     | Number      |
| **Deal Missing**        | Quantidade de volume ou produtos não atendidos em relação ao Deal.                                                                                      | Numérico (inteiro)                     | Number      |
| **Deal Proportion**     | Proporção geral do Deal atribuída ao contexto da linha.                                                                                                 | Decimal (até 4 casas)                  | Number      |
| **KA (Deal prop)**      | Percentual do Deal destinado à Key Account.                                                                                                             | Decimal (até 4 casas)                  | Number      |
| **Product (Deal prop)** | Percentual do Deal distribuído por produto.                                                                                                             | Decimal (até 4 casas)                  | Number      |
| **Origin (Deal prop)**  | Percentual do Deal distribuído por origem.                                                                                                              | Decimal (até 4 casas)                  | Number      |
| **Month (Deal prop)**   | Percentual do Deal distribuído ao longo dos meses.                                                                                                      | Decimal (até 4 casas)                  | Number      |
|                         |                                                                                                                                                         |                                        |             |
| **Aba Deal + Request**  |                                                                                                                                                         |                                        |             |
| **Campo**               | **Descrição**                                                                                                                                           | **Tamanho Máximo**                     | **Formato** |
| **Product**             | Produto considerado na alocação.                                                                                                                        | 100 caracteres                         | Texto       |
| **KA**                  | Cliente (Key Account) para o qual a alocação está sendo calculada.                                                                                      | 50 caracteres                          | Texto       |
| **Month Allocation**    | Volume total alocado para o mês correspondente, considerando a soma das alocações semanais (Request + Deal + Retail).                                   | Numérico (inteiro)                     | Number      |
| **Week Allocation**     | Volume alocado para a semana específica dentro do mês.                                                                                                  | Numérico (inteiro)                     | Number      |
| **Deal**                | Volume Alocado pela IA de Deal considerado para o KA após aplicação das regras.                                                                         | Numérico (inteiro)                     | Number      |
| **Inital Request**      | Volume de demanda inicial informado pelo usuário ou sistema antes da aplicação de ajustes.                                                              | Numérico (inteiro)                     | Number      |
| **Final Request**       | Volume final de demanda considerado no cálculo da IA, incluindo ajustes de Rollover e Rollback.                                                         | Numérico (inteiro)                     | Number      |
| **Rollover**            | Volume de demanda não atendido em períodos anteriores e transferido para o período atual, impactando o cálculo do Request.                              | Numérico (inteiro)                     | Number      |
| **Rollback**            | Volume de ajuste negativo aplicado ao Request, reduzindo a demanda planejada.                                                                           | Numérico (inteiro)                     | Number      |
| **Booked**              | Volume de produto reservado e confirmado comercialmente para a Key Account, definido por quarter e com alta prioridade na alocação.                     | Numérico (inteiro)                     | Number      |
| **Entered**             | Volume de produto registrado como intenção de reserva ou pedido em andamento para a Key Account, definido por quarter.                                  | Numérico (inteiro)                     | Number      |
| **Deal Monthly**        | Volume mensal do Deal após aplicação das proporções de distribuição (KA, produto, origem e mês).                                                        | Numérico (inteiro)                     | Number      |
| **Deal Prop**           | Proporção do Deal aplicada ao contexto da linha (KA, produto, origem e mês), utilizada para distribuir o volume do acordo comercial.                    | Decimal (até 4 casas)                  | Number      |
| **WOI**                 | Indicador de Weeks of Inventory que representa a projeção de cobertura de estoque (em semanas), calculado com base no sell-in e ativações.              | Decimal (até 2 casas)                  | Number      |
2. KPIs da Tela **Health Check**
| **Campo**           | **Descrição**                                                                                                                                                                        | **Tamanho Máximo**   | **Formato**   |
|---------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------|---------------|
| **KPI**             | Exibe a descrição da métrica de KPI.                                                                                                                                                 | 100 caracteres       | Texto         |
| **User**            | Exibe o resultado do KPI relacionado da alocação do usuário.                                                                                                                         | Numérico (inteiro)   | Number        |
| **AI**              | Exibe o resultado do KPI relacionado da alocação realizada pela IA.                                                                                                                  | Numérico (inteiro)   | Number        |
| **Status / Impact** | Exibe uma descrição resumida do comportamento ou condição do KPI, no formato [Quantidade] + [Problema/Condição] + [Impacto], permitindo rápida interpretação executiva do resultado. | 255 caracteres       | Texto         |
3. Product Level Validation Breakdown
| **Campo**                | **Descrição**                                                                                                                  | **Tamanho Máximo**   | **Formato**   |
|--------------------------|--------------------------------------------------------------------------------------------------------------------------------|----------------------|---------------|
| **Product/SKU**          | Identificação do produto ou SKU considerado na análise dos KPIs.                                                               | 100 caracteres       | Texto         |
| **Key Account**          | Identificação da Key Account (KA) associada ao resultado do KPI.                                                               | 100 caracteres       | Texto         |
| **Complete Deals**       | Quantidade de ocorrências em que o Deal foi totalmente atendido para o contexto do produto e KA.                               | Numérico (inteiro)   | Number        |
| **Complete Requests**    | Quantidade de ocorrências em que o Request foi totalmente atendido para o produto e KA.                                        | Numérico (inteiro)   | Number        |
| **Critical WOI**         | Quantidade de ocorrências em que o WOI está em nível crítico (WOI &lt; 10) para o produto e KA.                                | Numérico (inteiro)   | Number        |
| **Data inconsistencies** | Quantidade de ocorrências de inconsistências nos dados de entrada, como valores negativos ou incoerentes, para o produto e KA. | Numérico (inteiro)   | Number        |
| **Rollback**             | Quantidade de ocorrências em que foi aplicado rollback no contexto do produto e KA dentro do quarter.                          | Numérico (inteiro)   | Number        |
| **Rollover**             | Quantidade de ocorrências em que houve rollover (demanda não atendida transferida) para o produto e KA dentro do quarter.      | Numérico (inteiro)   | Number        |
| **Rounded Allocations**  | Quantidade de ocorrências em que a alocação foi realizada em múltiplos de 10 para o produto e KA.                              | Numérico (inteiro)   | Number        |
| **Site Supply**          | Quantidade de ocorrências em que houve redistribuição de site (JAG/MAN) para atendimento da demanda.                           | Numérico (inteiro)   | Number        |
| **Supply Violation**     | Quantidade de ocorrências em que a capacidade de supply semanal foi excedida para o produto e KA.                              | Numérico (inteiro)   | Number        |

Tabela 1 – Dados por Aba, Tela Allocation Breakdown

Tabela 2 – Dados da Tabela KPIs

Tabela 3 – Dados da Tabela de Drill Down

#### 5.2.1 Ações dos Botões

**BTN\_001 - Allocation Breakdown:**

Ao clicar no botão Allocation Breakdown, o sistema deve:

- Identificar automaticamente a última versão de alocação disponível;
- Selecionar automaticamente a versão mais recente;
- Carregar os dados da versão selecionada;
- Exibir a tela de análise operacional contendo:
    - Aba Request;
    - Aba Deal;
    - Aba Request + Deal;
    - Seletores de mês do quarter;
    - Filtros disponíveis;
    - Tabelas de detalhamento da alocação;
- Permitir ao usuário alterar a versão selecionada para análise;
- Atualizar automaticamente os dados da tela sempre que houver alteração de versão, mês ou filtros.

**BTN\_002 – Health Check:**

Ao clicar no botão Health Check, o sistema deve:

- Identificar automaticamente a última versão de alocação disponível;
- Selecionar automaticamente a versão mais recente;
- Carregar os dados da versão selecionada;
- Exibir os dashboards, KPIs e tabelas de validação referentes à versão carregada;
- Permitir ao usuário alterar a versão para análise;
- Atualizar automaticamente todas as informações exibidas sempre que houver alteração da versão ou filtros.

**BTN\_003 - Meses do quarter:**

O sistema deve permitir que o usuário selecione apenas um mês por vez e ao selecionar um mês:

- O botão correspondente deve ser destacado visualmente (ex: cor diferente, borda ativa ou preenchimento)
- Os demais botões devem permanecer inativos

Ao alterar o mês selecionado:

- O sistema deve atualizar automaticamente os dados exibidos na tabela

A atualização deve considerar:

- O mês selecionado
- A versão escolhida
- Os filtros aplicados
### 5.3 Regras de Negócio

##### RN\_001 – Controle de Versão

O Sistema deve garantir que cada execução do processo de alocação seja registrada como uma versão independente.

Cada versão deve permitir a identificação clara das seguintes informações:

- Data e hora da execução;
- Usuário responsável pela execução;

Adicionalmente, o sistema deve limitar a análise aos dados pertencentes ao quarter atual e ao próximo quarter disponível, assegurando relevância e consistência das informações exibidas.

##### RN\_002 – Ordem de Processamento de Alocação

O sistema deve obrigatoriamente processar a alocação respeitando a seguinte sequência:

1. Request (Demanda);
2. Deal (acordos comerciais);
3. Retail (volume residual);

Durante a etapa de Request, a distribuição do volume disponível deve seguir as regras de priorização definidas na RN\_013 – Scores (WOI, Booked e Entered).

Somente após a conclusão da alocação de Request o sistema deve iniciar o processamento do Deal. Após a conclusão das etapas de Request e Deal, qualquer volume remanescente deve ser destinado ao Retail.

##### RN\_003 – Regra de Request (Demanda)

O processamento deve iniciar pela análise da demanda. O volume de Request considerado deve corresponder à soma do Request final com os ajustes de Rollover e Rollback.

A alocação baseada em Request deve respeitar o limite da demanda disponível, ou seja, o volume alocado não deve ultrapassar o total calculado de Request. Garantindo que o sistema não distribua volumes superiores ao que foi efetivamente demandado.

Exceção: Essa validação pode ser flexibilizada quando o volume de sell-in (unidades faturadas) for superior ao total de Request calculado, para isso, o sistema pode apresentar alocações que excedam o request, refletindo ajustes operacionais de faturamento.

Com relação a Capacidade semanal (One Plan Week), a distribuição deve respeitar o limite de capacidade semanal disponível. Assim, a soma das alocações de todos os KAs dentro de uma mesma semana não deve ultrapassar o valor definido como One Plan Week. Essa validação garante que a alocação esteja alinhada com a capacidade operacional de atendimento.

Exceção: Quando houver alocação manual realizada pelo usuário e essa funcionalidade estiver ativa, o sistema deve permitir que o volume alocado ultrapasse o limite da capacidade semanal definida.

Para validação de Retail, quando há alocação manual (user allocation), o sistema deve garantir que os valores atribuídos ao Retail não sejam negativos, asegurando a integridade dos dados e evitando inconsistências na distribuição residual.

##### RN\_004 – Regra de Supply (Capacidade Disponível)

O Supply representa o limite máximo de volume disponível para distribuição, sendo que a soma das alocações não deve ultrapassar a capacidade de supply disponível.

Exceção: Caso exista intervenção manual do usuário com uma alocação superior ao supply disponível (Override do Usuário), o sistema deve respeitar a alocação definida pelo usuário, sem bloqueio.

Durante a semana corrente podem ocorrer ajustes de Sell-in relacionados a ajustes de faturamento quando há divergências entre o Request e o Sell-in, esses valores são representados como sell-in compensation, sendo um ajuste manual/técnico para corrigir os dados podendo impactar o balanceamento dos valores exibidos. Esse comportamento não deve ser tratado como regra de validação, sendo considerado apenas como cenário operacional ou de teste.

##### RN\_005 – Regra de Deal (Acordo Comercial)

O processamento do Deal deve ocorrer após a etapa de Request, sendo que o volume de Deal deve ser aplicado exclusivamente sobre o volume remanescente após alocação do Request e respeitará a seguinte distribuição:

- O valor total do Deal (Deal value);
- As proporções definidas no acordo;
- As dimensões de análise (KA, mês e origem);

A alocação resultante não pode assumir valores negativos e deve sempre respeitar o limite de Supply restante. Caso o volume necessário para completar o Deal seja superior ao supply restante, a distribuição deve ser ajustada proporcionalmente, garantindo que a alocação não ultrapasse a capacidade disponível.

O cálculo do Deal deve considerar apenas o volume necessário para complementar o total acordado, ou seja, a diferença entre o Deal e o volume alocado no Request.

Para semanas já encerradas, o sistema deve considerar que não há possibilidade de alteração de alocação, e o valor dessa semana deve ser zero, garantindo que apenas períodos futuros ou em aberto sejam considerados no processo de distribuição.

Com relação à distribuição por proporção, a alocação do Deal deve seguir as proporções definidas no acordo e são utilizadas para distribuir volumes entre diferentes dimensões, como: KA, Produto, Origem e Mês. A soma das proporções consideradas em cada cenário deve ser igual a 1, garantindo que todo o volume seja distribuído de forma completa e consistente.

O volume a ser distribuído pelo Deal deve considerar apenas o montante necessário para complementar o acordo comercial após o atendimento do Request, ou seja, o sistema deve calcular o volume restante do Deal subtraindo o que já foi atendido via Request, não podendo assumir valores negativos e deve ser distribuído proporcionalmente entre os KAs e as demais dimensões de Produto, Origem e Mês.

As variáveis consideradas no processo de alocação do Deal serão:

- Valor total do Deal (Deal Value);
- Volume alocado via Deal (Deal Allocation);
- Supply disponível após o Request;
- Quantidade de produtos não atendidos no Deal (missing products);
- Proporções e quantidades distribuídas por: KA, Produto, Origem e Mês;

##### RN\_006 – Regra de MMICOM/Retail

Para KAs classificados como MMICOM ou Retail, a lógica de deal não deve ser aplicada. Nesses casos, a alocação deve seguir exclusivamente as regras de Request e Scores.

O sistema deve garantir que os valores atribuídos a esses KAs não sejam negativos.

##### RN\_007 – Regra de Alocação Residual (Retail)

Após a execução das etapas de request e deal, qualquer volume de supply ainda disponível deve ser alocado para Retail. Esse volume residual representa o excedente não utilizado pelas etapas anteriores.

A alocação residual não pode assumir valores negativos e deve sempre respeitar o saldo de supply disponível.

##### RN\_008 – Regra de Alocação Final

A alocação final deve ser composta pela soma dos volumes atribuídos nas três etapas do processo: Request, Deal e Retail.

O resultado final deve refletir integralmente a ordem de processamento estabelecida, garantindo consist~encia entre demanda, acordos comerciais e capacidade disponível.

##### RN\_010 – Rollover

O Rollover representa o volume de demanda não atendido em períodos anteriores e que deve ser carregado para o período atual, impactando diretamente o cálculo do Request, funciona como um incremento de demanda, aumentando o volume que precisa ser atendido na alocação. Tendo como influência na Alocação, o aumento do volume de Request, eleva a prioridade de atendimento daquele KA/produto podendo consumir maior parcela do supply disponível.

- Regra de Cálculo : O valor de rollover deve ser somado ao Request Final para compor a demanda total considerada pela IA.
- Quanto maior o rollover, maior a pressão sobre o supply
- Pode reduzir o volume disponível para Deal

##### RN\_011 – Rollback

O Rollback representa um ajuste negativo aplicado ao Request, reduzindo a demanda originalmente planejada. Atua como um fator de redução do request, pode compensar excesso de planejamento ou ajustes comerciais.

- Regra de Cálculo : O valor de rollback deve ser subtraído do total de demanda.
- Reduz o volume de Request
- Libera supply para: outros KAs, atendimento de Deal e residual (Retail)

##### RN\_012 – WOI (Weeks of Invetory)

O WOI (Weeks of Inventory) representa a quantidade de semanas que o estoque disponível será capaz de sustentar com base no ritmo médio de consumo (ativações), sendo utilizado como indicador de risco e equilíbrio da distribuição.

Regra de Cálculo : O WOI deve ser calculado conforme a seguinte lógica:

WOI = (Sell-in Lifetime – Activations Lifetime) / Avg Activations, onde:

- Sell-in Lifetime: total acumulado de unidades faturadas;
- Activations Lifetime: total acumulado de unidades ativadas;
- Avg Activations: média de ativações por semana;
- É uma métrica dinâmica ao longo do tempo:
    - Deve reduzir progressivamente a cada semana.
    - A redução ocorre conforme o consumo (ativações).
    - Na ausência de reposição, o WOI tende a diminuir aproximadamente em 1 unidade por semana (dependendo da média de ativação).

Classificação e Influência de Alocação com relação ao Risco do WOI

- WOI = 0 : Ruptura Grave, Estoque esgotado - prioridade máxima de alocação;
- WOI &lt; 10 : Crítico, Alto risco de ruptura - alta prioridade de alocação;
- 10 ≤ WOI &lt; 15 : Risco Médio, Situação de atenção - prioridade moderada de alocação;
- WOI ≥ 15 : Fora de Risco, Estoque saudável - menor prioridade de alocação;

Quando o WOI for igual a zero, o sistema deve reconhecer como ruptura total de estoque representando um cenário crítico onde não há mais unidades disponíveis e o atendimento ao cliente está comprometido.

Durante o processo de alocação :

- KAs com WOI baixo ou crítico tendem a receber maior volume;
- KAs com WOI elevado podem ter volume reduzido;
- A IA busca equilibrar os níveis de estoque entre os KAs;

Exceção: O WOI não deve ser considerado para MMICOM e Retail. Nestes casos, a alocação para MMICOM segue exclusivamente a lógica de Request e Retail segue exclusivamente a lógica de Book e Entered.

##### RN\_013 – Scores (Book, Entered, WOI)

Os scores representam um ranking de priorização da alocação, onde a IA classifica os KAs com base no risco de estoque (WOI), compromissos comerciais (Booked) e intenção de demanda (Entered), realizando a distribuição do supply de forma sequencial, priorizando sempre os cenários mais críticos ou estratégicos.

- WOI (Weeks of Inventory) → indicador de risco de estoque
- Booked → volume reservado no quarter (prioritário)
- Entered → volume solicitado / em processo de reserva

Como Princípio de Funcionamento, a IA deve:

- Classificar cada KA em um Score (0 a 7);
- Processar a alocação seguindo essa ordem de prioridade;
- Consumir o supply disponível de forma sequencial;

A alocação não é simultânea e acontece por prioridade, conforme ranking abaixo:

- Score 0 – MMICOM, Prioridade Máxima:
    - Sempre possui prioridade máxima
    - A alocação deve ocorrer até completar 100% do Request
    - Ignora WOI, Book e Entered
    - É processado antes de todos os demais KAs
- Score 1 – WOI Crítico:
    - Condição: WOI &lt; 10
    - Peso: 100% WOI
    - Possui Alta prioridade (risco de ruptura)
- Score 2 – WOI Médio + Book:
    - Condição: 10 ≤ WOI &lt; 15 e Book &gt; 0
    - Peso: 50% WOI e 50% Book
- Score 3 – WOI Médio + Entered:
    - Condição: 10 ≤ WOI &lt; 15 AND Book = 0 e Entered &gt; 0
    - Peso: 75% WOI e 25% Entered
- Score 4 – WOI Médio (sem Book/Entered):
    - Condição: 10 ≤ WOI &lt; 15,  Book = 0 e Entered = 0
    - Peso: 100% WOI
- Score 5 – WOI Alto + Book:
    - Condição: WOI ≥ 15 e Book &gt; 0
    - Peso: 100% Book
- Score 6 – WOI Alto + Entered:
    - Condição: WOI ≥ 15, Book = 0 e Entered &gt; 0
    - Peso: 100% Entered
- Score 7 – Demais casos:
    - Condição: não atende nenhum dos critérios anteriores
    - Menor prioridade de alocação

Os Scores influenciam na Distribuição seguindo a seguinte lógica:

- Ordenar os KAs por Score (0 → 7);
- Iniciar alocação pelos scores mais prioritários;
- Consumir o supply disponível progressivamente;

Comportamento esperado:

- Scores menores → recebem primeiro
- Scores maiores → recebem apenas se ainda houver supply

Score com relação ao Request : dentro de cada Score a alocação deve respeitar o Request e não deve ultrapassar a demanda;

Score com relação ao Supply : atua como limitador global do ranking, se o supply acabar antes, Scores mais baixos ficam sem alocação. Ou seja, em um  cenário de escassez apenas Score 0 e 1 tendem a ser atendidos completamente.

##### RN\_014 – Compensação de Sell in

A compensação de sell-in é um ajuste operacional que corrige divergências de faturamento sem interferir na lógica principal da alocação.

O sell-in deve ser comparado com o Request, caso haja diferença, pode existir um valor de compensação (coluna sell-in comp).

Esta compensação não altera diretamente o cálculo da IA, mas atua como ajuste externo refletido nos dados. Pode resultar em:

- Alocações maiores que o request;
- Diferenças entre planejamento e execução;

Comportamento do Sistema:

- Não deve bloquear o cálculo;
- Não deve alterar regras de validação;
- Deve apenas refletir o ajuste no resultado;

##### RN\_015 – Site Supply

Site Supply representa a distribuição da capacidade de atendimento por site de origem (JAG, MAN) para cada produto, sendo utilizado para garantir o atendimento da demanda (Request).

O valor de referência dessa distribuição é o Initial Request, definido previamente pelo cliente com base na capacidade operacional de cada site e representa a expectativa de atendimento por origem.

O sistema analisa as semanas abertas, verifica o limite de capacidade definido no One Plan (weekly capacity) e avalia se é possível attender 'Request + Rollover – Rollback'.

Caso o site originalmente definido não possua capacidade suficiente, o sistema deve redistribuir a alocação para outro site disponível. O sistema identifica o site alternativo com capacidade disponível e realoca o volume excedente respeitando a capacidade semanal e restrições operacionais.

Caso, mesmo após redistribuição entre sites, não haja capacidade suficiente para atender toda a demanda nos dois sites JAG e MAN, o sistema não deve forçar a alocação além da capacidade disponível e o volume não atendido deve ser tratado como demanda pendente gerando rollover para períodos futuros.

O Site Supply atua antes ou durante o atendimento do Request e define onde (origem) o volume será alocado. Este movimento não altera a prioridade (Score), mas limita a execução.

##### RN\_016 – Transparência e Explicabilidade

O sistema deve apresentar de forma clara e detalhada todos os elementos utilizados no cálculo de alocação, permitindo total rastreabilidade e entendimento do resultado. E deve exibir as seguintes informações:

- Request inicial e final
- Valores de Rollover e Rollback
- Deal value e proporções aplicadas
- Supply disponível

##### RN\_017 – Validações Gerais

O sistema deve garantir que:

- Nenhum valor de alocação seja negativo.
- A distribuição respeite os limites de Supply, exceto em casos de Overrride de usuário.
- A alocação de Deal não ultrapasse o valor do acordado.
- A consistência entre Request, Deal e Supply seja mantida em todas as etapas.
- Volume distribuído em cada etapa de Request, Deal e Retail.

##### RN\_018 – Aplicação dos Filtros

Os Filtros devem ser aplicados somente após seleção de uma versão de alocação. A exibição dos dados deve ocorrer apenas após definição dos critérios de filtro pelo usuário.

Cada aba da funcionalidade deve obedecer às seguintes regras:

- Aba Request
- Aba Deal
- Aba Request + Deal

A visualização dos dados exige obrigatoriamente a seleção dos filtros de Quarter, Product e Origin.

Os filtros de Month e KA são opcionais e podem ser utilizados para aprofundamento da análise, conforme necessidade do usuário.

Para visualização dos dados, é obrigatória a seleção dos filtros de Quarter, Deal Group e KA.

Os filtros Product, Origin e Month são opcionais e podem ser utilizados para aprofundamento da análise, conforme necessidade do usuário.

Nesta Aba não há filtros obrigatórios específicos, ela se adapta ao tipo de cliente KA. Onde Retail segue a lógica de Request, enquanto que os demais seguem a lógica do Deal.

O usuário pode aplicar livremente os filtros estando disponíveis apenas os filtros Month, KA e Origin, conforme necessidade de análise do usuário.

O sistema deve adaptar-se automaticamente o comportamento de visualização da alocação conforme o tipo de KA e a disponibilidade de Deal associado.

##### RN\_019 – Acesso às funcionalidades de Análise de Alocação

O sistema deve disponibilizar duas funcionalidades para análise dos resultados da alocação realizada pela IA, acessíveis através do seguinte fluxo de navegação: Home → KA AI Distribution → Allocation Breakdown ou Health Check.

1. Allocation Breakdown (Visão Operacional)

- Representa a visão detalhada da alocação
- Apresenta os dados em formato de tabelas
- Permite entender como os cálculos foram realizados, incluindo:
    - Request;;
    - Deal;
    - Retail;
    - Variáveis utilizadas no cálculo;
- Representa a visão consolidada e analítica da alocação
- Apresenta os resultados por meio de dashboards e KPIs
- Permite avaliar a qualidade e consistência da distribuição
- Essa funcionalidade tem como objetivo:
- Permitir validação prévia dos resultados da IA
- Suportar tomada de decisão antes da publicação da alocação
- Garantir maior controle e governança do processo

Objetivo: explicar “como” a alocação foi construída.

2. Health Check (Visão Executiva)

Objetivo: explicar “quão boa” foi a alocação.

Além do acesso via AI Explainability, o sistema deve permitir que o Health Check ou Allocation Breakdown seja acessado diretamente a partir da funcionalidade KA AI Distribution, após a execução da alocação pela IA e antes da publicação da versão, através do botão Health Check ou Allocation Breakdown. Assim, usuário poderá visualizar as informações como etapa intermediária permitindo avaliação dos resultados antes da publicação.

##### RN\_020 – KPIs – Tela Health Check

A Tela Health Check apresenta indicadores (KPIs) em formato de quantidade de ocorrências, com o objetivo de avaliar a qualidade, consistência e eficiência da alocação realizada pela IA. Cada KPI deve ser calculado com base na versão de alocação selecionada.

Os KPIs definidos são:

1. Input Data Inconsistencies : Mede a quantidade de ocorrências de alocações negativas, independentemente da origem (IA ou usuário).
2. Critical WOI : Mede a quantidade de ocorrências de WOI em nível crítico, considerando WOI &lt; 10.
3. Week Supply Violation : Mede a quantidade de ocorrências em que a capacidade semanal foi ultrapassada, a tabela mostra o número de semanas com violação de capacidade.
4. Rounded Allocations (Blocos de 10) : Mede a quantidade de alocações arredondadas em múltiplos de 10.
5. Site Supply Occurrences : Mede a quantidade de ocorrências em que houve redistribuição de site para atendimento da demanda, quando o site definido no Initial Request não possuía capacidade disponível. Métrica válida somente para alocação realizada pela IA.
6. Complete Request : Mede a quantidade de ocorrências em que o volume de Request foi totalmente atendido pela alocação.
7. Rollover : Mede a quantidade de ocorrências em que houve aplicação de rollover no quarter analisado. Considerar no máximo 2 ocorrências por quarter corrente, devido à inexistência de rollover no mês corrente. Esta métrica não se aplica para alocação realizada pelo usuário.
8. Rollback : Mede a quantidade de ocorrências em que houve aplicação de rollback no quarter analisado. Considerar no máximo 2 ocorrências por quarter corrente, devido à inexistência de rollback no mês corrente. Esta métrica não se aplica para alocação realizada pelo usuário.
9. Completed Deals : Mede a quantidade de ocorrências em que o Deal foi totalmente atendido.

##### RN\_021 – Elegibilidade de Alocação pela IA

O sistema deve possuir um indicador que determine se uma determinada combinação de dados poderá ou não ser considerada no processo de alocação realizado pela IA, ou seja, o campo Enable Allocation controla dinamicamente quais Key Accounts participam do cálculo da IA, sendo automaticamente definido com base na seleção realizada pelo usuário no momento da execução da distribuição.

Este indicador deve ser representado por uma coluna do tipo booleano (True/False), denominada Enable Allocation.

O valor do campo Enable Allocation (True/False) deve ser definido no momento da solicitação de uma nova  distribuição na funcionalidade KA AI Distribution → New AI Distribution.

Quando uma Key Account (KA) for selecionada pelo usuário na execução da distribuição, o campo deve ser definido como True. E quando uma Key Account (KA) não for selecionada, o campo deve ser definido como False.

Para cada registro (KA, Produto, Origem, Período), o sistema deve avaliar o campo "Enable Allocation".

Quando o valor for True, o registro deve ser considerado no cálculo da alocação pela IA e distribuir volume normalmente. O cálculo seguirá todas as regras definidas:

- Request
- Score (WOI, Booked, Entered)
- Supply
- Deal
- Retail

Quando o valor for False, o registro não deve ser considerado no cálculo da IA esta não deve alterar ou recalcular os valores existentes. O sistema deve manter os valores previamente definidos, considerando User Allocation, quando disponível. Nesse cenário, a IA deve ignorar completamente esses registros durante:

- classificação de Score
- distribuição de supply
- aplicação de Deal

Esses registros devem permanecer com valores fixos e a exclusão não deve comprometer o cálculo dos demais registros.

A configuração do campo Enable Allocation pode impactar o resultado da alocação da seguinte forma:

- Redistribuição do supply entre os KAs habilitados
- Possível aumento de Rollover para KAs não atendidos
- Redução da participação de determinados KAs no resultado final

Importante: Esta regra não é exibida em nenhuma tela da funcionalidade AI Explainability. Trata-se de uma regra interna aplicada durante o processamento da alocação pela IA para definir a elegibilidade das Key Accounts no cálculo da distribuição.

##### RN\_022 – Carregamento Automático da Última Versão de Simulação

Ao acessar as funcionalidades Allocation Breakdown ou Health Check, o sistema deve carregar automaticamente a última versão de simulação de alocação disponível, ou seja, o sistema deve carregar automaticamente a última versão de simulação disponível ao acessar as telas de análises, garantindo agilidade e melhor experiência do usuário.

Esse comportamento deve ser sempre que o usuário acessar uma das telas Allocation Breakdown ou Health Check.

O sistema deve identificar a versão mais recente de alocação gerada (baseada em data e hora de execução) e carregar automaticamente essa versão como padrão.

Ao carregar a tela, a versão mais recente deve ser automaticamente selecionada e os dados devem ser exibidos sem necessidade de ação adicional do usuário.

A tela deve refletir os resultados da versão carregada KPIs ou tabelas correspondentes.

O usuário deve ter a opção de:

- Alterar manualmente a versão selecionada
- Consultar versões anteriores, se disponíveis

Caso não exista nenhuma versão de alocação disponível, o sistema não deve carregar dados automaticamente e deve exibir mensagem informativa ao usuário, por exemplo: “No allocation versions available.”

### 5.4 Fluxo Alternativo

FA\_001 - Ausência de Versões de Alocação

Caso não exista nenhuma versão de alocação disponível no sistema:

- O sistema não deve permitir a seleção de versão
- O sistema deve exibir uma mensagem informativa ao usuário

Mensagem sugerida:

“No allocation versions available.”

FA\_002 – Falha no Carregamento da Versão

Caso ocorra erro ao carregar a versão selecionada:

- O sistema deve interromper o carregamento dos dados;
- O sistema deve exibir mensagem de erro ao usuário.

Mensagem sugerida: Failed to load allocation version. Please try again.

FA\_003 - Filtros Obrigatórios Não Informados

Caso o usuário tente visualizar os dados sem preencher os filtros obrigatórios:

- O sistema deve impedir o carregamento dos dados
- O sistema deve destacar os campos obrigatórios não preenchidos

Mensagem sugerida:

“Please fill in all required filters.”

Aplicável para: Aba Request e Aba Deal

FA\_004 – Nenhum Dado encontrado

Caso não existam dados correspondentes aos filtros aplicados:

- O sistema deve exibir uma mensagem informativa
- Nenhum dado deve ser apresentado na tabela

Mensagem sugerida:

“No data available for selected filters.”

FA\_005 - Acesso Direto ao Allocation Breakdown

Caso o usuário acesse a funcionalidade a partir da tela KA AI Distribution após a execução da IA:

- O sistema deve abrir diretamente a tela Allocation Breakdown;
- O sistema deve carregar automaticamente a versão recém-gerada;
- O usuário deve visualizar os dados detalhados da alocação antes da publicação da versão.

FA\_006 - Acesso Direto ao Health Check

Caso o usuário acesse a funcionalidade a partir da tela KA AI Distribution após a execução da IA:

- O sistema deve abrir diretamente a tela Health Check;
- O sistema deve carregar automaticamente a versão recém-gerada;
- O usuário deve visualizar os KPIs e dashboards antes da publicação da versão.

FA\_007 - Alteração Manual da Versão

Caso o usuário altere a versão carregada automaticamente:

- O sistema deve atualizar os dados apresentados;
- As informações devem refletir exclusivamente a versão selecionada;
- Os filtros já preenchidos devem ser mantidos quando aplicáveis.

### 5.5 Critérios de Aceitação

CA\_001 – Acesso ao Allocation Breakdown

Dado que o usuário esteja autenticado e possua permissão de acesso

Quando acessar o menu Home → KA AI Distribution → Allocation Breakdown

Então o sistema deve exibir a tela Allocation Breakdown contendo a última versão de alocação disponível carregada automaticamente.

CA\_002 – Acesso ao Health Check

Dado que o usuário esteja autenticado e possua permissão de acesso

Quando acessar o menu Home → KA AI Distribution → Health Check

Então o sistema deve exibir a tela Health Check contendo a última versão de alocação disponível carregada automaticamente.

CA\_003 – Carregamento automático da última versão no Allocation Breakdown

Dado que exista pelo menos uma versão de alocação disponível

Quando o usuário acessar a tela Allocation Breakdown

Então o sistema deve carregar automaticamente a versão mais recente disponível.

CA\_004 – Carregamento automático da última versão no Health Check

Dado que exista pelo menos uma versão de alocação disponível

Quando o usuário acessar a tela Health Check

Então o sistema deve carregar automaticamente a versão mais recente disponível.

CA\_005 – Alteração da versão selecionada

Dado que o usuário esteja visualizando uma versão de alocação

Quando selecionar outra versão disponível

Então o sistema deve atualizar automaticamente todos os dados exibidos na tela conforme a versão selecionada.

CA\_006 – Navegação entre abas do Allocation Breakdown

Dado que o usuário esteja na tela Allocation Breakdown

Quando selecionar uma das abas disponíveis (Request, Deal ou Request + Deal)

Então o sistema deve exibir os dados correspondentes à aba selecionada.

CA\_007 – Seleção de mês do Quarter - Tela Allocation Breakdown

Dado que o usuário esteja visualizando uma tela do Allocation Breakdown

Quando selecionar um mês do Quarter

Então o sistema deve destacar visualmente o mês selecionado

E atualizar automaticamente os dados exibidos.

CA\_008 – Filtros obrigatórios da Aba Request - Tela Allocation Breakdown

Dado que o usuário esteja na aba Request

Quando informar os filtros obrigatórios Quarter, Product e Origin

Então o sistema deve executar a consulta e exibir os dados correspondentes aos filtros selecionados.

E

Dado que o usuário esteja na aba Request

Quando tentar consultar os dados sem informar Quarter, Product e Origin

Então o sistema deve impedir a consulta

E exibir a mensagem: "Please fill in all required filters".

CA\_009 – Filtros obrigatórios da Aba Deal - Tela Allocation Breakdown

Dado que o usuário esteja na aba Deal

Quando informar os filtros obrigatórios Quarter, Deal Group e KA

Então o sistema deve executar a consulta e exibir os dados correspondentes aos filtros selecionados.

E

Dado que o usuário esteja na aba Deal

Quando tentar consultar os dados sem informar Quarter, Deal Group e KA

Então o sistema deve impedir a consulta

E exibir a mensagem: "Please fill in all required filters".

CA\_010 – Exibição da Aba Request - Tela Allocation Breakdown

Dado que exista uma versão válida selecionada

Quando o usuário acessar a aba Request

Então o sistema deve exibir a tabela contendo os campos definidos para a visualização de Request.

CA\_011 – Exibição da Aba Deal - Tela Allocation Breakdownn

Dado que exista uma versão válida selecionada

Quando o usuário acessar a aba Deal

Então o sistema deve exibir a tabela contendo os campos definidos para a visualização de Deal.

CA\_012 – Exibição da Aba Request + Deal - Tela Allocation Breakdown

Dado que exista uma versão válida selecionada

Quando o usuário acessar a aba Request + Deal

Então o sistema deve exibir a tabela contendo os campos definidos para a visualização consolidada da alocação.

CA\_013 – Visualização dos KPIs - Tela Allocation Health Check

Dado que o usuário esteja na tela Health Check

Quando existir uma versão válida selecionada

Então o sistema deve exibir os KPIs calculados para a versão selecionada.

CA\_014 – Visualização do Product Level Validation Breakdown - Tela Allocation Health Check

Dado que o usuário esteja na tela Health Check

Quando aplicar os filtros necessários para consulta

Então o sistema deve exibir os dados da tabela Product Level Validation Breakdown.

CA\_015 – Acesso direto ao Allocation Breakdown

Dado que uma nova distribuição tenha sido executada na funcionalidade KA AI Distribution

Quando o usuário acessar o botão Allocation Breakdown

Então o sistema deve abrir a tela Allocation Breakdown carregando automaticamente a versão recém-gerada.

CA\_016 – Acesso direto ao Health Check

Dado que uma nova distribuição tenha sido executada na funcionalidade KA AI Distribution

Quando o usuário acessar o botão Health Check

Então o sistema deve abrir a tela Health Check carregando automaticamente a versão recém-gerada.

CA\_017 – Ausência de versões disponíveis

Dado que não existam versões de alocação disponíveis

Quando o usuário acessar Allocation Breakdown ou Health Check

Então o sistema não deve apresentar dados

E deve exibir a mensagem “No allocation versions available”.

CA\_018 – Nenhum dado encontrado

Dado que os filtros informados não retornem resultados

Quando o sistema executar a consulta

Então nenhuma informação deve ser apresentada

E o sistema deve exibir a mensagem "No data available for selected filters".

CA\_019 – Consistência do Deal Prop

Dado que o usuário esteja visualizando a aba Deal

Quando existirem registros de Deal para o contexto selecionado

Então o sistema deve exibir o valor de Deal Prop correspondente à proporção aplicada ao registro

E a soma das proporções utilizadas para distribuição do Deal deve totalizar 1 (100%).

CA\_020 – Consistência entre Deal Value e Deal Missing

Dado que o usuário esteja visualizando a aba Deal

Quando existir um Deal associado ao registro

Então o valor apresentado em Deal Missing não deve ser superior ao valor apresentado em Deal Value (Deal Missing = Deal Value - Deal Allocation).

CA\_021 – Consistência do Request

Dado que o usuário esteja visualizando a aba Request ou Request + Deal

Quando existir um registro de demanda

Então o valor apresentado em Request deve corresponder ao resultado de:

Initial Request + Rollover - Rollback

CA\_022 – Consistência da Alocação Mensal

Dado que o usuário esteja visualizando um mês específico

Quando existirem alocações semanais para o período

Então o valor apresentado em Month Allocation deve corresponder à soma dos respectivos valores exibidos em Week Allocation.

CA\_023 – Consistência entre Allocation Breakdown e Health Check (Complete Request)

Dado que o usuário esteja visualizando a mesma versão de alocação

Quando comparar os dados do Allocation Breakdown com o KPI Complete Request do Health Check

Então a quantidade apresentada no KPI deve corresponder à quantidade de registros cujo Request foi totalmente atendido.

CA\_024 – Consistência entre Allocation Breakdown e Health Check (Completed Deals)

Dado que o usuário esteja visualizando a mesma versão de alocação

Quando comparar os dados da aba Deal com o KPI Completed Deals

Então a quantidade apresentada no KPI Completed Deals deve corresponder ao total de ocorrências identificadas na aba Deal.

CA\_025 – Consistência entre Allocation Breakdown e Health Check (Critical WOI)

Dado que o usuário esteja visualizando a mesma versão de alocação

Quando comparar a coluna WOI do Allocation Breakdown com o KPI Critical WOI do Health Check

Então a quantidade apresentada no KPI deve corresponder ao número de registros com WOI inferior a 10.

### 5.6 Matriz de Rastreabilidade

| **Regra de Negócio**                                                | **Critérios de Aceitação**                                                                        | **Fluxo Alternativo**                       |
|---------------------------------------------------------------------|---------------------------------------------------------------------------------------------------|---------------------------------------------|
| **RN\_001 – Controle de Versão**                                    | CA\_003, CA\_004, CA\_005, CA\_017                                                                | FA\_001, FA\_002, FA\_007                   |
| **RN\_002 – Ordem de Processamento de Alocação**                    | -                                                                                                 | -                                           |
| **RN\_003 – Regra de Request (Demanda)**                            | CA\_010, CA\_012, CA\_021, CA\_022                                                                | -                                           |
| **RN\_004 – Regra de Supply (Capacidade Disponível)**               | -                                                                                                 | -                                           |
| **RN\_005 – Regra de Deal (Acordo Comercial)**                      | CA\_011, CA\_012, CA\_019, CA\_020, CA\_024                                                       |                                             |
| **RN\_006 – Regra de MMICOM/Retail**                                | -                                                                                                 | -                                           |
| **RN\_007 – Regra de Alocação Residual (Retail)**                   | CA\_012                                                                                           | -                                           |
| **RN\_008 – Regra de Alocação Final**                               | CA\_012, CA\_022                                                                                  | -                                           |
| **RN\_010 – Rollover**                                              | CA\_021                                                                                           | -                                           |
| **RN\_011 – Rollback**                                              | CA\_021                                                                                           | -                                           |
| **RN\_012 – WOI (Weeks of Inventory)**                              | CA\_025                                                                                           | -                                           |
| **RN\_013 – Scores (Book, Entered e WOI)**                          | -                                                                                                 | -                                           |
| **RN\_014 – Compensação de Sell-In**                                | -                                                                                                 | -                                           |
| **RN\_015 – Site Supply**                                           | -                                                                                                 | -                                           |
| **RN\_016 – Transparência e Explicabilidade**                       | CA\_010, CA\_011, CA\_012, CA\_013, CA\_014                                                       | -                                           |
| **RN\_017 – Validações Gerais**                                     | CA\_019, CA\_020, CA\_021, CA\_022                                                                | -                                           |
| **RN\_018 – Aplicação dos Filtros**                                 | CA\_008, CA\_009, CA\_014, CA\_018                                                                | FA\_003, FA\_004                            |
| **RN\_019 – Acesso às Funcionalidades de Análise da Alocação**      | CA\_001, CA\_002, CA\_006, CA\_007, CA\_010, CA\_011, CA\_012, CA\_013, CA\_014, CA\_015, CA\_016 | FA\_005, FA\_006                            |
| **RN\_020 – KPIs – Tela Health Check**                              | CA\_013, CA\_014, CA\_023, CA\_024, CA\_025                                                       | -                                           |
| **RN\_021 – Elegibilidade de Alocação pela IA**                     | -                                                                                                 | -                                           |
| **RN\_022 – Carregamento Automático da Última Versão de Simulação** | CA\_001, CA\_002, CA\_003, CA\_004, CA\_005, CA\_015, CA\_016, CA\_017                            | FA\_001, FA\_002, FA\_005, FA\_006, FA\_007 |

Tabela 4 – Matriz de Rastreabilidades

Notas:

RN\_002 – Ordem de Processamento de Alocação

Esta regra descreve a sequência interna de processamento da IA (Request → Deal → Retail). Não possui comportamento visível diretamente nas telas e sua validação ocorre durante testes do motor de alocação.

RN\_004 – Regra de Supply (Capacidade Disponível)

Trata-se de uma regra de processamento da alocação. Os valores resultantes são refletidos nas telas, porém a validação do limite de Supply não possui operação visível específica para o usuário da funcionalidade Explainability.

RN\_006 – Regra de MMICOM/Retail

Esta regra define um comportamento específico da IA para determinados tipos de KA. Não possui representação visual explícita ou interação direta do usuário nas telas de Explainability.

RN\_013 – Scores (Book, Entered e WOI)

Os Scores influenciam o cálculo da alocação, porém não são exibidos diretamente nas telas Allocation Breakdown ou Health Check. A validação desta regra ocorre durante testes funcionais da IA e análise dos resultados da distribuição.

RN\_014 – Compensação de Sell-In

A compensação de Sell-In representa um ajuste operacional dos dados de entrada. Apesar de poder impactar os resultados exibidos, não existe funcionalidade específica na interface que permita sua validação isolada.

RN\_015 – Site Supply

A ocorrência de redistribuição entre sites é refletida apenas por meio dos resultados da alocação e do KPI "Site Supply Occurrences". Não existe visualização detalhada do cálculo ou do processo de redistribuição nas telas de Explainability.

RN\_021 – Elegibilidade de Alocação pela IA

Esta regra não possui representação visual nas telas Allocation Breakdown ou Health Check. Seu processamento ocorre exclusivamente durante a execução da alocação automática realizada pela IA, definindo quais Key Accounts participarão do cálculo da distribuição.

## 6 APROVAÇÕES

As pessoas identificadas abaixo confirmam que estão cientes e aprovam os requisitos:

| **Cargo - Nome**                                | **Assinatura**   |
|-------------------------------------------------|------------------|
| **Project Manager**  – Luciano Ferreira (FIT)   |                  |
| **SW Coordinator**  – Guilherme Novellato (FIT) |                  |
| **Stakeholder I – Caio Lenotti (Motorola)**     |                  |
| **Cientista de Dados - Hiparco Vieira (FIT)**   |                  |
| **System Analyst**  – Kamila Pimentel           | **Visualizar**   |