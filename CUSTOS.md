---
titulo: Custos, COGS e ARR da Regis
projeto: Regis · Financial Anomaly Autopilot
time: Time 12 · Hackathon Vanguarda
data: 30 de agosto de 2026
status: modelo base, premissas fechadas com o time
---

# Custos, COGS e ARR da Regis

Modelo simples de custo e receita, com os valores que a nossa pesquisa já confirmou. Nada aqui é estimativa de terceiro: o preço do Open Finance veio da pesquisa de custo por conta e o custo de IA foi medido nos logs da Regis rodando em produção.

## 1. Premissas

| Premissa | Valor | Origem |
|---|---|---|
| Usuários pagantes ativos | 1.000 | Cenário de referência do time |
| Contas de banco por usuário | 2 (máximo) | Perfil do MEI: uma conta PJ e a maquininha |
| Conexões totais de Open Finance | 2.000 | 1.000 × 2 |
| Open Finance | R$ 2.500/mês, plano fechado | Pluggy, plano fixo |
| Modelo de IA | Claude Opus 5 | Em produção no bot |
| Câmbio | R$ 5,40 por dólar | Referência do período |
| Preço da assinatura | R$ 29,90/mês | Mesmo patamar do concorrente mais próximo |

O plano da Pluggy é **fixo**. Ele não sobe quando entra mais um usuário, o que muda completamente o formato da curva de custo. Esse é o ponto central deste documento.

## 2. Custo de IA, medido e não estimado

A Regis registra o consumo de cada chamada. Estes são os números reais do servidor:

```
entrada 3.062 tokens · saída  71 tokens  →  US$ 0,0171
entrada 8.826 tokens · saída 324 tokens  →  US$ 0,0522
entrada 3.056 tokens · saída 113 tokens  →  US$ 0,0181
                                  total     US$ 0,0874
```

A chamada de 8.826 tokens de entrada é a segunda volta do mesmo raciocínio (a Regis consultou o motor de detecção e voltou para responder). Ou seja, as três chamadas de API correspondem a **duas perguntas reais** de uma pessoa.

> **Custo de IA por pergunta: US$ 0,044, ou R$ 0,236.**

Vale registrar o que **não** consome IA. O motor de detecção é Python determinístico e roda todo dia sobre todas as transações sem chamar modelo nenhum. Conferir duplicata, somar faturamento, projetar o teto do MEI e comparar repasse com venda custam zero. A IA entra apenas quando a pessoa conversa em texto livre, lê um print ou pede uma contestação escrita.

## 3. COGS mensal com 1.000 usuários

**Custo fixo, não muda com o número de usuários:**

| Item | Por mês |
|---|---|
| Open Finance (Pluggy, plano fechado) | R$ 2.500,00 |
| Servidor | R$ 200,00 |
| **Total fixo** | **R$ 2.700,00** |

**Custo variável, muda com o uso:**

| Item | Por usuário/mês |
|---|---|
| IA, 10 perguntas × R$ 0,236 | R$ 2,36 |

**Fechamento:**

| | Valor |
|---|---|
| Custo fixo | R$ 2.700,00 |
| Custo variável (1.000 × R$ 2,36) | R$ 2.360,00 |
| **COGS mensal** | **R$ 5.060,00** |
| **COGS por usuário** | **R$ 5,06/mês** |
| **COGS anual** | **R$ 60.720,00** |

Custo por conexão de Open Finance: **R$ 1,25 por mês** (R$ 2.500 divididos por 2.000 conexões).

### Sensibilidade ao uso de IA

O único item que cresce com o uso é a conversa. Mesmo triplicando o volume de perguntas, o custo continua confortável:

| Perguntas por usuário/mês | IA por usuário | COGS por usuário | COGS anual |
|---|---|---|---|
| 10 (base) | R$ 2,36 | R$ 5,06 | R$ 60.720 |
| 15 | R$ 3,54 | R$ 6,24 | R$ 74.876 |
| 30 | R$ 7,08 | R$ 9,78 | R$ 117.353 |

A IA não é o risco do modelo. A R$ 0,24 por pergunta, uma pessoa teria que conversar 126 vezes por mês para consumir a própria assinatura.

## 4. ARR e margem bruta

ARR é receita recorrente anualizada: quanto entra num mês, multiplicado por 12.

```
1.000 pagantes × R$ 29,90  =  R$ 29.900 por mês
R$ 29.900 × 12             =  R$ 358.800 de ARR
```

| | Valor |
|---|---|
| ARR | R$ 358.800 |
| COGS anual | R$ 60.720 |
| **Lucro bruto** | **R$ 298.080** |
| **Margem bruta** | **83,1%** |

### Se o preço mudar

| Preço/mês | ARR | Lucro bruto | Margem |
|---|---|---|---|
| R$ 19,90 | R$ 238.800 | R$ 178.082 | 74,6% |
| **R$ 29,90** | **R$ 358.800** | **R$ 298.082** | **83,1%** |
| R$ 39,90 | R$ 478.800 | R$ 418.082 | 87,3% |
| R$ 49,90 | R$ 598.800 | R$ 538.082 | 89,9% |

Mesmo no piso de R$ 19,90 a margem passa de 74%. O modelo aguenta preço agressivo de entrada.

## 5. Break-even

Cada assinante deixa **R$ 27,54 de contribuição** por mês (R$ 29,90 de receita menos R$ 2,36 de IA). O custo fixo é de R$ 2.700 por mês.

```
R$ 2.700 ÷ R$ 27,54 = 98 usuários
```

> **Com 98 MEIs pagantes a Regis se paga.**

Esse é o número mais forte que temos, porque é pequeno e verificável. Os 1.000 usuários são projeção. Os 98 são um alvo que dá para atingir e mostrar.

## 6. Por que o custo cai conforme crescemos

Como o Open Finance é plano fechado, o custo por usuário despenca com a escala:

| Usuários | COGS por usuário/mês |
|---|---|
| 50 | R$ 56,36 |
| 100 | R$ 29,36 |
| 250 | R$ 13,16 |
| 500 | R$ 7,76 |
| **1.000** | **R$ 5,06** |
| 2.000 | R$ 3,71 |
| 5.000 | R$ 2,90 |

De 50 para 1.000 usuários o custo por pessoa cai 11 vezes. É o inverso da intuição de quem imagina custo por conta conectada, e é o argumento de viabilidade do produto: **cada novo usuário é mais barato que o anterior.**

## 7. Premissa a confirmar

O plano fechado da Pluggy custa R$ 2.500 por mês, e a quantidade de conexões incluída não é divulgada publicamente. Nosso cenário precisa de **2.000 conexões**.

Confirmar esse limite com o comercial da Pluggy é o próximo passo, e o sandbox deles é gratuito e não exige aprovação. É a única premissa deste documento que ainda não está fechada, e vale dizer isso em voz alta no pitch antes que alguém pergunte.
