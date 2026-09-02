---
titulo: Dataset sintético da Regis
tipo: referencia
status: vigente
atualizado: 2026-08-29
autor: Time 12 · Hackathon Vanguarda
resumo: O extrato sintético que alimenta o motor de detecção e a demo, a persona por trás dele, o formato de cada arquivo e o gabarito das anomalias plantadas.
---

# dados/

Dataset sintético da Regis. É o que alimenta o motor de detecção e a demo, conforme a Decisão 3 do `BRIEFING.md`.

**Os dados são simulados e isso se diz antes que perguntem.** É a regra 3 da seção 3.9 do briefing. Simulação declarada é método, escondida é problema. Nenhuma pessoa, empresa ou CNPJ aqui é real.

## Arquivos

| Arquivo | O que é |
|---|---|
| `gerar.py` | Gera os três JSON. Determinístico, `random.seed = 20260829`. Rodar de novo produz exatamente os mesmos arquivos e os mesmos ids. |
| `transacoes.json` | O extrato da conta PJ, transação por transação, de 01/06/2026 a 29/08/2026. É o que a Regis lê. |
| `vendas.json` | O registro de vendas do lado da Angela, a agenda de atendimentos dela. É o outro lado do cruzamento, o que permite comparar o que foi vendido com o que caiu na conta. |
| `anomalias-esperadas.json` | O gabarito. Quais anomalias foram plantadas, em quais transações, de que tipo e com que nível de certeza. Serve para testar o motor. |

Para regerar:

```bash
python3 dados/gerar.py
```

O script imprime uma conferência no fim: totais por mês, por canal, faturamento acumulado do ano e a lista de anomalias com os ids resultantes. Ele também trava com `assert` se o faturamento do ano não fechar em R$ 58.400,00 ou se alguma venda apontar para a transação errada.

## A persona

Segue o ICP fechado na seção 3.9 do briefing, e segue de propósito. Se a demo mostrar um MEI de serviço que recebe só Pix, ela contradiz a nossa própria tese.

**Angela Nogueira, cabeleireira.** MEI, CNAE 9602-5/01, em Campinas (SP). Atende de terça a sábado. Controla tudo no caderno.

**Ela não é dona de salão.** Aluga uma cadeira no Studio Bella e atende a própria clientela lá dentro, dividindo o espaço com outras três profissionais (Jéssica, Tainara e Simone). Cada uma fatura no próprio CNPJ, então a conta que a Regis lê é só dela e **as 337 vendas de `vendas.json` são atendimentos dela**. O aluguel da cadeira, R$ 1.850,00 todo dia 5, sai dessa mesma conta e é a maior despesa fixa do mês.

Isso importa para a tese: o MEI que a Regis atende é a pessoa que trabalha, não a empresa que emprega. É o formato mais comum do ICP e é o que mantém a camada de regra como lei pública, sem configuração.

Ela **recebe por maquininha (crédito e débito) e por marketplace de agendamento**, com Pix como minoria. Volume alto, concentrado nas sextas e nos sábados. O valor que cai na conta não é o valor que ela vendeu, e é exatamente aí que o produto existe.

| Canal | Participação no faturamento | Vendas |
|---|---|---|
| Maquininha crédito | 36,7% | 130 |
| Maquininha débito | 27,9% | 99 |
| Marketplace (BelezaNet) | 27,4% | 84 |
| Pix | 8,0% | 24 |

## Os números que fecham

| | |
|---|---|
| Período detalhado | 01/06/2026 a 29/08/2026 (sábado, o dia da demo) |
| Transações | **367** (265 entradas, 102 saídas) |
| Vendas | **337** |
| Ticket médio | R$ 84,27 (mínimo R$ 35,00, máximo R$ 380,00) |
| Faturamento bruto de junho | R$ 8.200,00 |
| Faturamento bruto de julho | R$ 9.400,00 |
| Faturamento bruto de agosto (até o dia 29) | R$ 10.800,00 |
| Janeiro a maio (consolidado, sem detalhe) | R$ 30.000,00 |
| **Faturamento bruto acumulado em 2026** | **R$ 58.400,00** |
| Percentual do teto de R$ 81.000 | 72,1% |
| Falta para o teto | R$ 22.600,00 |
| Projeção de estouro do teto | outubro de 2026 (estimado em 24/10) |
| Recebido líquido no período detalhado | R$ 26.996,81 |
| Saídas no período detalhado | R$ 13.769,25 |

**Atenção a uma distinção que muda o número.** O que conta para o teto do MEI é a **receita bruta**, ou seja, o valor da venda, não o valor que sobrou depois da taxa. Por isso R$ 58.400,00 é a soma dos valores vendidos, e é esse o número da frase de abertura do pitch. A soma dos valores efetivamente creditados na conta é menor, porque taxa de maquininha, comissão de marketplace e antecipação ficam pelo caminho. Os dois números estão em `transacoes.json`, no bloco `totais`.

### Duas simplificações declaradas

1. **Janeiro a maio entram consolidados**, mês a mês, no bloco `acumulado_anterior` de `transacoes.json`. Só junho, julho e agosto têm detalhe de transação. O motor fiscal soma os dois para chegar no acumulado do ano.
2. **A liquidação é D+0.** No mundo real o crédito cai em D+1 (ou D+0 com antecipação, que é o caso dela) e o débito em D+1. Aqui a venda e o crédito acontecem no mesmo dia, o que mantém a aritmética conferível dentro da janela. O repasse do marketplace continua semanal, com defasagem real de 1 a 7 dias.

### Sobre o volume

O salão faz de 10 a 13 movimentações nos dias de pico (sextas e sábados de agosto) e de 3 a 5 nos dias mais fracos. O volume é calibrado para o faturamento fechar em R$ 58.400,00, que é o número do pitch e da tela do app. Um salão com o dobro de movimento estouraria o teto antes de agosto, e a história do produto seria outra.

## Formato de `transacoes.json`

Objeto com cinco blocos.

```
meta                 quem é a persona, período, seed, aviso de dado sintético
contexto             o que o motor precisa saber para transformar número em anomalia
acumulado_anterior   janeiro a maio de 2026, consolidado por mês
totais               os números conferidos acima
transacoes[]         a lista de movimentações
```

Cada transação:

| Campo | O que é |
|---|---|
| `id` | `TX-0001` em diante, numerado por ordem cronológica |
| `data` | ISO 8601 com hora e fuso, por exemplo `2026-08-12T21:47:00-03:00` |
| `tipo` | `entrada` ou `saida` |
| `canal` | `maquininha_credito`, `maquininha_debito`, `marketplace`, `pix`, `boleto`, `debito_automatico` |
| `descritor_bruto` | como apareceria no extrato, sujo e difícil de ler (`PAG*BELEZANET`, `MP *SALAO`, `CIELO 4829`, `SOMPRO*MUSICA AMBIENT`) |
| `valor` | sempre positivo. A direção está em `tipo`, não no sinal |
| `valor_bruto_venda` | o valor vendido, quando difere do recebido. `null` quando são iguais (Pix, boleto, débito automático) |
| `contraparte` | quem é de verdade. É a resposta certa do motor de identificação, o que ele deveria conseguir deduzir a partir do `descritor_bruto` |
| `categoria` | `venda`, `repasse`, `antecipacao`, `insumo`, `assinatura`, `aluguel`, `utilidade`, `tarifa`, `imposto`, `pessoal`, `nao_classificado` |
| `venda_ids` | nas entradas de venda, as vendas de `vendas.json` que aquela transação liquidou |
| `qtd_vendas` | nos repasses de marketplace, quantas vendas o repasse cobre |
| `competencia` | nos pagamentos de DAS, a competência fiscal paga |

O bloco `contexto` é a parte que decide o que é anomalia e o que é vida normal. Ele carrega o que é contrato ou evento declarado, nunca inferência: taxas contratadas da maquininha, comissão do marketplace, estado da antecipação automática, isenção da tarifa da conta PJ, assinaturas com data de início e de cancelamento, lista de contrapartes conhecidas, faixa de horário habitual e feriados do período. Sem ele, metade das anomalias vira ruído.

## Formato de `vendas.json`

É o registro do lado da Angela, a agenda dela. Sem ele não dá para detectar repasse menor que a venda.

| Campo | O que é |
|---|---|
| `id` | `VD-0001` em diante |
| `data`, `cliente`, `profissional`, `servico` | o atendimento. `profissional` é sempre Angela, porque as colegas de salão faturam no CNPJ delas e não entram nesta conta |
| `valor_venda` | o valor cobrado da cliente |
| `forma_recebimento` | o canal |
| `transacao_id` | a transação de `transacoes.json` que liquidou essa venda |
| `taxa_contratada` e `liquido_previsto` | nas vendas de cartão, o que deveria ter caído |
| `marketplace`, `repasse_previsto`, `data_repasse_previsto` | nas vendas de marketplace |

**Como cruzar.** Cartão e Pix são um para um: uma venda, uma transação, mesma data. Marketplace é muitos para um: várias vendas caem no mesmo repasse semanal (toda sexta, cobrindo de sexta anterior até quinta). É esse cruzamento que revela o repasse curto.

## Formato de `anomalias-esperadas.json`

O gabarito. Cada anomalia traz `catalogo` (o nome exato do item no catálogo de anomalias da pesquisa), `tipo`, `certeza`, `comportamento_esperado` (resolve, encaminha ou pergunta), a lista de `transacoes` por id, `valor_impacto`, `sinal_de_deteccao` e `contexto_necessario`.

Há também um bloco `falsos_positivos_esperados`, com seis coisas que parecem anomalia e não são (o aluguel de cadeira de R$ 1.850, as vendas de química de R$ 380, o pico de sexta e sábado, o DAS mensal, a taxa de 1,49% no débito que bate com o contrato e o Pix único para o supermercado). Um motor que acerta as 12 e também erra nessas seis não está pronto. A tela do app diz isso de propósito: "outros achados ficaram de fora, são normais para o seu histórico".

## As 12 anomalias plantadas

**8 fato, 2 regra, 2 suspeita.** Dinheiro recuperável nos fatos: **R$ 1.145,15**.

A tese do produto está aqui dentro: a autonomia varia com a certeza. Fato a Regis resolve, regra ela encaminha, suspeita ela pergunta.

### Fato (a Regis resolve ou entrega a ação pronta)

| id | Anomalia | Tipo | Transações | Impacto |
|---|---|---|---|---|
| **AN-01** | Boleto do fornecedor pago duas vezes no mesmo dia. Beleza Distribuidora, R$ 487,60 às 09:12 e às 16:48 de 14/07 | duplicidade | `TX-0165`, `TX-0167` | R$ 487,60 |
| **AN-02** | Assinatura cobrada duas vezes no dia 12. Netflix, R$ 55,90 às 09:14 e às 21:47 de 12/08 | duplicidade | `TX-0274`, `TX-0277` | R$ 55,90 |
| **AN-03** | Assinatura que continua depois do cancelamento. Agenda Salão App, cancelado em 12/06 (protocolo AGS-2026-88421), cobrou em 22/06, 22/07 e 22/08 | recorrência | `TX-0084`, `TX-0196`, `TX-0323` | R$ 119,70 |
| **AN-04** | Reajuste silencioso. SomPro Música Ambiente saltou de R$ 32,90 para R$ 47,90 em 08/08, alta de 45,6% sem aviso | valor | `TX-0261` | R$ 15,00 por mês |
| **AN-05** | Repasse de marketplace menor que a soma das vendas. Sexta 28/08, 11 vendas somando R$ 1.042,00, esperado R$ 916,96 com a comissão de 12%, caiu R$ 878,96 | conciliação | `TX-0344` | R$ 38,00 |
| **AN-06** | DAS pago duas vezes. Competência 06/2026, R$ 87,05 em 17/07 e de novo em 20/07. Não cabe na janela de 24 horas, se detecta pela competência | duplicidade | `TX-0175`, `TX-0193` | R$ 87,05 |
| **AN-07** | Antecipação automática ligada, descontando 2,99% do crédito todo dia desde 02/03/2026 | valor | 57 lançamentos, de `TX-0004` a `TX-0367` | R$ 312,00 no trimestre |
| **AN-08** | Tarifa de conta PJ que deixou de ser gratuita. Isenta até 31/07, primeira cobrança de R$ 29,90 em 05/08 | valor | `TX-0244` | R$ 29,90 por mês |

### Regra (a Regis encaminha para quem decide)

| id | Anomalia | Tipo | Transações | Impacto |
|---|---|---|---|---|
| **AN-09** | Faturamento acumulado em ritmo de estourar o teto. R$ 58.400,00 em 29/08, 72,1% do teto, faltam R$ 22.600,00. A série de junho a agosto cresce R$ 1.300,00 por mês, o que joga o estouro em outubro de 2026 | fiscal | agregada, sem transação única | o que está em jogo não é dinheiro, é o regime |
| **AN-10** | Taxa efetiva da maquininha diferente da contratada. De 17/08 a 29/08 o crédito veio com 3,49% de desconto contra os 2,89% contratados | valor | 24 transações, de `TX-0308` a `TX-0363` | R$ 11,03 no período |

### Suspeita (a Regis pergunta uma vez e registra a resposta)

| id | Anomalia | Tipo | Transações | Impacto |
|---|---|---|---|---|
| **AN-11** | Pagamento para contraparte sem histórico. Pix de R$ 340,00 para Maria Souza em 03/08. Na demo a resposta é legítima, é a manicure nova | contraparte | `TX-0241` | nenhum, é pergunta |
| **AN-12** | Transação em horário atípico. Pix de R$ 268,00 às 03:41 de domingo 19/07, para uma contraparte conhecida. É a única movimentação do dataset fora da faixa de 06:00 às 23:59 | comportamento | `TX-0192` | nenhum, é pergunta |

## Notas de calibragem

- **AN-12 é a única transação fora do horário habitual.** Os débitos automáticos foram colocados a partir das 06:00 de propósito, para o detector de horário atípico ter um alvo só e o teste ser limpo.
- **AN-01 e AN-02 são as únicas duplicatas de saída em janela menor que 24 horas.** Conferido por varredura de pares. Se o motor achar uma terceira, é falso positivo.
- **AN-06 não cabe na regra de 24 horas** e isso é de propósito. Os dois pagamentos estão a três dias de distância. A duplicidade fiscal se detecta pela competência repetida, não pelo relógio.
- **AN-10 é regra e não fato** porque depende do contrato da titular com a adquirente, que está em `contexto.maquininha`. Sem contrato cadastrado, uma taxa de 3,49% é só uma taxa.
- **A taxa do débito é 1,49% e bate com o contrato.** É o caso em que a Regis confere e cala, que é metade da tese. Está na lista de falsos positivos esperados.
