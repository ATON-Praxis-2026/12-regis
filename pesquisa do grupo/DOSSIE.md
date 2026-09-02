---
titulo: Dossiê da pesquisa
tipo: pesquisa
status: vigente
atualizado: 2026-08-29
autor: Time 12 · Hackathon Vanguarda
resumo: Todos os fatos levantados (participantes, números, anomalias, universo MEI e custo de infraestrutura), cada um com seu grau de verificação.
---

# DOSSIÊ — Financial Anomaly Autopilot

> Tudo que levantamos, em fatos. Sem interpretação de produto.
> Para conclusões e recomendações, ver `INSIGHTS.md`. Para o quadro de concorrentes, `CONCORRENTES.md`.
>
> Atualizado em 29/08/2026, depois do BRIEFING do time.

**Legenda de confiabilidade usada neste documento:**
✅ verificado na fonte · ⚠️ do briefing ou de terceiros, não verificado · ❌ contém erro

---

## Índice

1. [O desafio](#1-o-desafio)
2. [O time](#2-o-time)
3. [Arquivos nesta pasta](#3-arquivos-nesta-pasta)
4. [A pesquisa: método e roteiro](#4-a-pesquisa-método-e-roteiro)
5. [Os 14 participantes](#5-os-14-participantes)
6. [Números agregados](#6-números-agregados)
7. [Enquadramento: o ciclo e os dois eixos](#7-enquadramento-o-ciclo-e-os-dois-eixos)
8. [Catálogo de anomalias](#8-catálogo-de-anomalias)
9. [Concorrentes](#9-concorrentes)
10. [Dados sobre MEI](#10-dados-sobre-mei)
11. [Custo de infraestrutura](#11-custo-de-infraestrutura)
12. [Decisões tomadas](#12-decisões-tomadas)
13. [Documentos publicados](#13-documentos-publicados)
14. [Ressalvas](#14-ressalvas)

---

## 1. O desafio

**Tema 20 — Financial Anomaly Autopilot.** Time 12, Mesa 12. Escolhido em 29/08/2026 às 11:38. **Entrega em 24 horas.**

> *"Deixe uma IA procurando dinheiro vazando 24 horas por dia."*

Construir um autopilot que monitore movimentações financeiras e encontre cobranças duplicadas, valores atípicos, despesas inesperadas e possíveis erros.

**O que o jurado espera ver:** um autopilot funcionando. Não é dashboard de finanças, não é categorizador de gastos. É um agente que encontra o que está errado e **faz alguma coisa a respeito**.

---

## 2. O time

| Pessoa | Base | Papel no hackathon |
|---|---|---|
| **Kysa Robert** (Arcádia · Criação) | Constrói gerador automático de apresentações e propostas | **Tech lead.** Motor de detecção, agente de IA, integrações, automação |
| **Ana Silveira** (Órbital · Gestão) | UX Designer, Rio. Já constrói um app financeiro | **UX e interface.** Fluxos, telas, tom das mensagens, protótipo navegável |
| **Gabriel Hardt** (Arcádia · Criação) | Criatividade e estratégia, São Paulo | **Narrativa e pitch.** Posicionamento, história da demo, roteiro, marca |
| **Márcio Faustini Modonezi** (Arcádia · Criação) | Fundador de estúdio criativo, Campinas | **Identidade visual.** Nome, marca, slides, assets, apoio no front |

**Leitura do time (do briefing):** três de Criação, uma de Gestão. Fortes em narrativa, design e IA aplicada. Fracos em engenharia pesada e dados financeiros reais.
**Estratégia decorrente:** ganhar pela clareza do produto e pela demo, não pela sofisticação estatística.

---

## 3. Arquivos nesta pasta

```
ATON/
├── DOSSIE.md                              este arquivo — os fatos
├── INSIGHTS.md                            conclusões e decisões
├── CONCORRENTES.md                        quadro comparativo detalhado
├── transcrever.py                         transcrição local de áudio (Whisper)
├── relatorio-pesquisa-14-conversas.html   relatório da pesquisa, standalone
└── [14 pastas, uma por entrevistado]
    ├── *.ogg   áudio original do WhatsApp
    ├── *.txt   transcrição (ou resposta escrita)
    └── *.srt   transcrição com marcação de tempo
```

**Fora da pasta:** `BRIEFING.pdf` (Downloads) e a `pasta pesquisa do grupo/` citada na seção 10 do briefing — `enquadramento-problema.html`, `catalogo-anomalias.html`, `catalogo-anomalias_mei.html`, `insights-mei.html`, `custo-por-conta.html`.

**19 áudios** transcritos localmente com `faster-whisper`, modelo `small`, sem envio a serviços externos. **10 respostas escritas.**

### Como rodar a transcrição de novos áudios

```bash
py transcrever.py "C:\Users\Usuário\Desktop\ATON"
```

Varre subpastas, gera `.txt` e `.srt` ao lado de cada áudio. Use `--modelo medium` se a qualidade não bastar.

**Notas do ambiente:** Python 3.11.9 e ffmpeg 9.0.1 via winget. O Smart App Control do Windows 11 bloqueia a DLL do PyAV, então o script decodifica áudio por fora e substitui o PyAV por um stub. **Não desativar o Smart App Control** — é irreversível sem reinstalar o Windows.

---

## 4. A pesquisa: método e roteiro

- **Quando:** 29/08/2026 · **Quem:** 14 pessoas (PF, rede de contatos do time)
- **Como:** 6 perguntas abertas por WhatsApp · áudio, texto, ou ambos (6 nos dois formatos)

### Roteiro

1. Você olha extrato e fatura do cartão? Com que frequência, e como é esse momento?
2. Me conta a última vez que apareceu uma cobrança que você não reconheceu ou não esperava. Como foi que você viu?
3. Quanto tempo você acha que ela ficou lá antes de você perceber?
4. O que você fez? Chegou a contestar, cancelar, ligar pra alguém? Como terminou?
5. Tem alguma cobrança que você já viu, achou estranha e deixou passar mesmo assim? Por quê?
6. Algum comentário adicional ou sugestão que te ajudaria com suas finanças?

---

## 5. Os 14 participantes

### E1 — olha quase todo dia
- **Q1** À noite, ao abrir o app, antes de deitar. Levantamento de tudo no fim do mês.
- **Q2** Cobrança não reconhecida na revisão mensal. Também: **cobrança duplicada** de um salgado numa padaria.
- **Q3** Até o fim do mês. · **Q4** Contestou. **Teve que pagar a fatura mesmo assim**; a cobrança não voltou. · **Q5** Não.

### E2 — quase todo dia
- **Q1** Olha a fatura quase todos os dias.
- **Q2** Compra pela internet que não foi ela, em site desconhecido. Também cobranças de Uber.
- **Q4** Contestou e **teve que provar** que não fez a compra. Cartão bloqueado automaticamente.
- ⚠️ Em outro áudio diz não ter tido cobrança errada — provavelmente outro cartão. **Transcrição mais ruidosa; conferir o `.srt` antes de citar.**

### E3 — ao comprar ou pagar
- **Q1** Quando compra algo ou vai pagar a fatura.
- **Q2** Expansões de armazenamento do Google. *"Fico me perguntando meses à frente o que diabos é isso."*
- **Q3** ~3 meses. · **Q4** **Já cancelou várias vezes por não saber o que eram.** Aconteceu de novo neste mês.
- **Q5** Como compra pouco no cartão, acaba associando as cobranças a algo.

### E4 — não olha
- **Q1** Não olha.
- **Q2** Assinatura que nunca contratou, no Nubank. Descobriu porque não usava mais a conta e havia dinheiro parado lá.
- **Q3** **5 meses.** · **Q4** Contestou pelo app, foi estornado.
- **Q6** *"As análises de fraude dos cartões deviam ser melhores e já pegarem os erros."*

### E5 — planilha própria + app
- **Q1** Gasta tudo no crédito. **Planilha de acompanhamento**; revisa em detalhe 2x/mês.
- **Q2** Semana passada: o Bradesco mandou mensagem perguntando se a compra era dela. Não era. Cartão *"já foi clonado mil vezes"* — 2ª vez no ano.
- **Q3** Curto, porque foi avisada. Num caso antigo, várias **recargas de celular pequenas** passaram meses até aparecer uma compra grande.
- **Q4** Sempre contestou, sempre estornaram — inclusive R$ 3.000.
- **Q5** *"Não gosto de gastar nem R$ 5. Se tiver um gasto de R$ 5 no meu cartão eu vou reclamar."*
- **Q6** O incômodo é **ter que trocar de cartão toda vez**.

### E6 — sem cartão de crédito
- **Q1** Nunca teve cartão de crédito. Só débito, boleto e Pix — inclusive o carro.
- **Q2** Nunca teve cobrança indevida: não há autorização de pagamento cadastrada em nada.
- **Relato de terceiro:** o cartão da sogra era usado por parentes todo mês. O filho contestava sempre, conferia quase diariamente e **montava planilha**. Acabou cancelando o cartão dela.

### E7 — acompanha por notificação
- **Q1** Extrato só quando entra algo ou quando não entende o saldo. Fatura raramente. Notificações em pasta trancada.
- **Q2** Semana passada: notificação de **R$ 30** que não lembrava. · **Q3** Imediato, pelo push.
- **Q4** Espera 3 a 4 horas tentando lembrar, depois **pesquisa o nome da transação na internet**. Era um estacionamento com nome e CNPJ de um mercado. *"Na maioria das vezes tem um nome que não ajuda muito a descobrir quem é."*
- **Q5** Não. Já teve o cartão clonado; viu pela notificação e bloqueou.
- **Q6** *"Não consigo pensar em nada que me ajudaria"* — enquanto recebe notificações, sente-se tranquilo.

### E8 — só quando usa
- **Q1** Três cartões, dois em débito automático. Confere quando usa — 3 ou 4 vezes em 3 meses. Não recebe mais extrato por correio.
- **Q2** **Três episódios:** (1) juros porque um **feriado municipal de Campinas** caiu no vencimento e o débito automático rodou fora do dia; (2) **descontos indevidos no INSS**, só vistos quando entrou no extrato — *"eu não entro nunca"*; (3) o banco registrou o **cancelamento de um débito automático que continuou sendo cobrado**.
- **Q3** Quase um mês. · **Q4** Ligou e reclamou. Conseguiu, mas **não gostou**: descontaram na fatura seguinte em vez de devolver.
- **Q5** *"Se eu vejo, eu não deixo passar. Eu ligo, sou reclamona."*
- **Q6** *"São coisas que a gente tem que começar, principalmente na nossa idade, a entrar mais vezes."*

### E9 — todos os dias
- **Q1** Todos os dias. Tranquilo. Costuma adiantar a fatura. · **Q2** Não teve essa experiência.
- **Q4** Já contestou, por cancelamento atrasado na Amazon. *"Foi simples."* · **Q5** Nunca deixou passar.

### E10 — extrato diário
- **Q1** Extrato todos os dias; fatura só no vencimento.
- **Q2** Não lembra a última, mas *"apareceu um nome estranho na fatura"*.
- **Q3** No máximo dentro do mês. · **Q4** Sempre liga para o banco, que *"prontamente cancela e resolve"*. · **Q5** Não.

### E11 — perto do pagamento
- **Q1** Perto do dia do pagamento. Sentimento de *"atenção e apreensão"*.
- **Q2** Há 10 meses: cobrança de **PlayStation com o console desligado havia mais de 2 anos**. · **Q3** ~10 dias.
- **Q4** Tentou pelo cartão e não resolveu. A central do PlayStation **estornou imediatamente**. · **Q5** Não.
- **Q6** *"A fatura de cartão é sempre muito complexa. Parece que fazem pra você ter que ficar olhando dez vezes... Tenho três cartões e os três eu acho uma bosta."*

### E12 — na hora de pagar
- **Q1** Na hora de pagar, revisa todas as compras antes.
- **Q2** **Acontece quase todo mês.** Consulta a agenda do dia e o código da cobrança; em geral era algo que ele comprou mesmo.
- **Q4** Só contestou **taxas do banco**. Sempre com sucesso.
- **Q5** **Sim.** *"Porque imaginei que tivesse feito mesmo."*
- **Q6** *"Deveria ser mais fácil identificar o estabelecimento de compra, com foto, nome fantasia, ou qualquer coisa."*

### E13 — não olha
- **Q1** *"Não olho extrato e fatura. Tipo, nunca."* Abre o app, vê o limite; se tem limite, compra.
- **Q2** Usa muito **Pix crédito** — a fatura vem com nome de pessoas aleatórias e ele se habituou a não reconhecer.
- **Q4** Nunca ligou para contestar. Ligou 2x: confirmar tentativa de golpe, e quando bloquearam compra legítima dele por ser atípica.
- **Q5** **Sim, por método.** Se a fatura está na faixa típica, assume que está tudo certo.
- **Q6** Consome muito serviço de pagamento instantâneo. *"Eu olharia mais o extrato se tivesse alguma forma automática de categorizar as coisas e me mostrar só o que fosse relevante ou atípico."* Usa BB e Nubank; *"o BB é uma derrota"*.

### E14 — 1x por semana
- **Q1** Uma vez por semana. · **Q2** Compra online que poderia ser cancelada no prazo — e não foi.
- **Q3** Imediato. · **Q4** Falou com empresa e banco. **"Foi cancelado depois de muito trampo."** · **Q5** Não. *"Reclamo tudo."*

---

## 6. Números agregados

### Frequência de checagem (Q1)

| Faixa | N | Quem |
|---|---|---|
| Todo dia ou quase | 4 | E9, E10, E2, E1 |
| Rotina de pagamento | 5 | E14, E5, E12, E11, E3 |
| Só quando estranha algo | 2 | E7, E8 |
| Nunca | 2 | E13, E4 |
| Sem cartão de crédito | 1 | E6 |

### Tempo até perceber (Q3)

| Tempo | Quem |
|---|---|
| Imediato | E14, E7 (push), E5 (banco avisou), E2 (bloqueio automático) |
| 10 dias | E11 |
| Dentro do mês | E1, E10, E8 |
| ~3 meses | E3 |
| 5 meses | E4 |
| Nunca olha | E13 |

### Contestação (Q4)

- **10 contestaram. 10 recuperaram o valor.**
- Simples: E5, E10, E4, E9, E12, E11 (via PlayStation)
- Com atrito: **E14** ("muito trampo"), **E2** ("tive que provar"), **E8** (desconto na fatura seguinte)
- Nunca precisaram: E7, E13, E6 · E3 cancela sem contestar

### Deixou passar (Q5)

- **Não:** 9 · **Sim:** 2 — E12 (*"imaginei que tivesse feito mesmo"*) e E13 (por método) · Outro: 3

### Tipos de episódio

| Tipo | N | Quem |
|---|---|---|
| **Dificuldade de identificar o estabelecimento** | **6** | E7, E12, E3, E10, E13, E11 |
| Fraude ou clonagem | 4 | E5, E2, E7, E13 (tentativa) |
| Cobrança recorrente não reconhecida | 3 | E4, E11, E3 |
| Cancelamento não honrado | 3 | E14, E9, E8 |
| Erro ou taxa da instituição | 2 | E8, E12 |
| Estorno virou desconto na fatura seguinte | 2 | E1, E8 |
| Cobrança duplicada | 1 | E1 |
| **Reajuste silencioso de assinatura** | **0** | — |

---

## 7. Enquadramento: o ciclo e os dois eixos

*(Do briefing, seção 3.1 e 3.2.)*

### O ciclo do vazamento — seis etapas

```
Acontece → Aparece → Percebe → Entende → Age → Resolve
```

O tempo se perde em **Percebe** e **Age**. A pesquisa mostrou que **Resolve é menos doloroso do que se supunha** (10 de 10 recuperaram) e que o gargalo real está em **Percebe** (quem não tem push demora meses) e sobretudo em **Entende** (não sei o que é essa cobrança, então assumo que fui eu).

### Quatro enquadramentos possíveis

| | Problema | Produto | Risco |
|---|---|---|---|
| **A** | "Ninguém olha" — cobertura | vigilância contínua | vira feed de alertas e morre de fadiga |
| **B** | "Olho mas não sei se é problema" — julgamento | contexto e evidência | depende de dados que não teremos |
| **C** | "Sei que está errado mas resolver é um inferno" — resolução | agente que redige contestação e acompanha estorno | depende de terceiros, difícil demonstrar |
| **D** | "Não quero ser eu que deixou passar" — responsabilidade | rastro auditável | vende tranquilidade, valor difícil de medir |

### O eixo de certeza — a tese central

Toda anomalia tem **tipo** (duplicidade, valor, recorrência, contraparte, comportamento, processo, conciliação, fiscal) e **certeza**. É a certeza que decide o comportamento do produto:

| Certeza | O que é | O que o autopilot faz |
|---|---|---|
| **Fato** | verificável — duplicata exata, estorno que não caiu, teste grátis que virou pago | resolve sozinho ou entrega a ação pronta |
| **Regra** | fato que só existe se conhecermos a política de quem usa | encaminha para quem decide |
| **Suspeita** | desvio estatístico; na maioria das vezes é legítimo | pergunta, contextualiza ou registra em silêncio |

> **A tese:** o nível de autonomia do autopilot varia com o nível de certeza da anomalia.
> Nenhum concorrente comunica isso — todos jogam tudo no mesmo feed.

**O que dá para demonstrar em 24h:** tudo marcado como **fato** (sem baseline, sem configuração). Regra exige política cadastrada — exceto a fiscal do MEI, que é pública. Suspeita exige histórico que não teremos.

### O problema do dia 1

**O que é "normal" no dia 1?** Sem histórico, o sistema fica mudo ou grita para tudo. Resolver bem a primeira semana de uso já diferencia. A saída adotada: **a resposta do usuário na conversa constrói o "normal"** — "foi eu sim" registra a contraparte como conhecida, sem tela de configuração.

---

## 8. Catálogo de anomalias

12 tipos, com regra de detecção, evidência e nível de certeza.

### Grupo 1 — validadas pela pesquisa (3+ menções)

**Estabelecimento não identificável** · 6 de 14 · **núcleo** · certeza: *suspeita → entendimento*
- *Sinal:* descritor sem correspondência no histórico nem em base conhecida · razão social do CNPJ diferente do nome de fachada · padrão de gateway (`PAG*`, `MP *`) · Pix crédito com nome de pessoa física
- *Custo:* erra nos dois sentidos — E12 pagou o que não reconheceu, E3 cancelou serviço que usava. Mais o tempo: 3h do E7 por R$ 30.
- *Construir:* **difícil.** É onde o LLM ganha de regex.

**Assinatura ou recorrência fantasma** · 3 de 14 · certeza: **fato**
- *Sinal:* série mensal estável do mesmo estabelecimento · intervalo 28–31 dias · valor constante
- *Custo:* **o mais alto do catálogo** — multiplica por mês.

**Cancelamento não honrado** · 3 de 14 · certeza: **fato** (se houver data)
- *Sinal:* recorrência que persiste após a data marcada como cancelamento

**Fraude e cartão clonado** · 4 de 14 · **não competir**
- Em vários casos **o banco detectou primeiro**. Antifraude de emissor é maduro.

### Grupo 2 — citadas por poucos (1–2 menções)

**Tarifa ou juro indevido** · 2 de 14 · certeza: **fato** (subcaso feriado)
- *Sinal:* tarifa ou juro cruzado com **calendário de feriados**, com o contrato e com o saldo do dia
- *Construir:* o caso do feriado é **determinístico e barato**.

**Estorno que virou desconto** · 2 de 14 · certeza: **fato**
- *Sinal:* contestação registrada + ausência de crédito em N dias

**Cobrança duplicada** · 1 de 14 · certeza: **fato** · **trivial de construir**
- *Sinal:* par (estabelecimento, valor) em janela < 24h · excluir categorias com repetição legítima

### Grupo 3 — hipóteses sem evidência na nossa pesquisa (0 menções)

| Anomalia | Situação |
|---|---|
| **Reajuste silencioso** | Zero menções. **A mais fácil de construir** — entra no código, sai do pitch como dor validada. |
| **Gasto fora do padrão** | Zero direto. Demanda indireta: E13 pediu "só o relevante ou atípico". Certeza: *suspeita*. |
| **Anomalia por ausência** | Zero. Diferencial conceitual — ninguém olha o que faltou. |
| **Projeção de saldo negativo** | Zero. Ninguém pediu previsão. |
| **Pré-autorização não estornada** | Zero. |

### Família fiscal MEI *(do briefing — sem evidência de campo)*

Certeza: **regra pública**, aritmética, sem modelo estatístico.

- Faturamento acumulado projetado contra o teto de R$ 81 mil
- Receita recebida no CPF ligada à atividade (ver CGSN 183/2025, seção 10)
- DAS do mês não pago
- Repasse de marketplace menor que a venda
- Antecipação automática ligada sem que o titular saiba

### Ordem de construção

1. **Identificação do estabelecimento** — pré-requisito de quase tudo
2. **Detecção de recorrência** — destrava assinatura fantasma, reajuste e cancelamento não honrado
3. **Duplicidade e feriado** — as duas regras determinísticas, baratas
4. **Motor fiscal MEI** — aritmética sobre regra pública
5. **O limiar de quando falar** — separa autopilot de relatório agendado

> Os itens 1 e 2 sozinhos cobrem **cinco** das doze anomalias de PF.

---

## 9. Concorrentes

**Detalhe completo em `CONCORRENTES.md`.** Resumo:

| Produto | Dado | Fala sozinho? | Verificação |
|---|---|---|---|
| **ALL** (myall.com.br) | Open Finance, 120+ instituições, +1M transações classificadas | Parcial — assistivo | ✅ site e FAQ |
| **FinAI** | 100% registro manual | Não | ✅ site e FAQ |
| **Mobills** | "integração automática" | Não | ⚠️ parcial |
| **Organizze** | não verificado | Não | ❌ |
| **Cora / InfinitePay / Asaas** | é a própria conta | Não | ⚠️ parcial |
| **Meu MEI Digital** (governo) | não lê dado bancário | avisa prazo por calendário | ✅ gov.br |
| **Bancos** | é o próprio banco | **Sim** — push na compra | ⚠️ conhecimento geral |

**Três fatos que importam:**
1. A linha divisória não é a IA — todos usam IA. É **de onde vem o dado**.
2. **Ninguém, além do banco, procura o usuário.** O ALL diz na home: *"é isto que você abre todo dia"*.
3. **A parte difícil já foi construída.** Conectar e classificar virou infraestrutura, não diferencial.

⚠️ **O briefing não menciona concorrentes em nenhuma seção.** Ver `INSIGHTS.md`.

---

## 10. Dados sobre MEI

> ⚠️ **Nenhum MEI foi entrevistado.** Nada nesta seção vem da nossa pesquisa de campo.

### ✅ Verificados

**Resolução CGSN nº 183/2025 — receita no CPF soma ao limite do MEI.**
Publicada em 26/09/2025, altera a CGSN nº 140/2018 (acrescenta o §10 ao art. 2º). **Em vigor**, efeitos a partir de 01/01/2026 para o art. 3º. Não foi sustada nem revogada.
Receitas apuradas em inscrições cadastrais distintas — CPF e CNPJ — passam a ser somadas para verificar o limite anual.
⚠️ **Citar com cuidado:** a Receita Federal publicou em novembro de 2025 uma nota **desmentindo fake news** sobre esta resolução, e há questionamento sobre seus limites constitucionais. Dizer com precisão o que ela faz, sem dramatizar.

**570 mil MEIs desenquadrados por excesso de faturamento em 2024.**
Dados da Receita Federal. **É 30 vezes mais que em 2023.**
**A explicação importa:** o salto é atribuído ao **cruzamento de Pix, cartão e transações financeiras** pela administração tributária.
⚠️ **Contra-narrativa:** a imprensa enquadrou isso como notícia **boa** — negócios crescendo (CartaCapital: *"reforçando expansão da economia"*). Ter resposta pronta.

**Teto do MEI: R$ 81.000/ano — congelado desde 2018**, não 2019.
- Até 20% acima (R$ 97.200): continua no regime até dezembro, com DAS complementar
- Acima de 20%: **desenquadramento retroativo** ao início do ano, recálculo pelas alíquotas do Simples, multa de 0,33% ao dia (teto 20%), juros pela Selic
- DASN-SIMEI não entregue: multa mínima de R$ 50 e suspensão do CNPJ após 90 dias

**~60% dos MEIs misturam finanças pessoais e do negócio.**
Sebrae, *Pesquisa Hábitos de Uso de Produtos Financeiros* (2ª ed.), 6,1 mil MEIs em todos os estados e no DF, fim de 2022 a início de 2023.
⚠️ As fontes descrevem de formas diferentes: ~60% para *MEIs*, 61% para *pequenos negócios* em geral, e outra redação fala em "usar recursos de PF na empresa". **São populações diferentes.** Citar como *"cerca de 60% dos MEIs, Sebrae, 2023"*.

**1,59 milhão de novos MEIs entre janeiro e abril de 2026**, alta de ~15% sobre 2025. MEIs são **78% de todas as empresas abertas em 2026.** (Sebrae sobre dados da Receita Federal, 28/05/2026.)

**Dinheiro do negócio em conta PF fica invisível ao score de crédito empresarial.**
O Open Finance exige login com CNPJ para dados PJ. (Let's Money, 29/05/2026. Mesma fonte: 1,4 milhão de empresas compartilhando dados, +159% de consentimentos no ano.)
**Nota:** o gargalo principal descrito é a burocracia de **múltiplos sócios**. **O MEI tem um sócio só — não se aplica a ele.**

**Misturar contas pode fazer renda não-empresarial contar contra o teto.**
Se o MEI tem outras fontes de renda e não separa, fica difícil comprovar à Receita que o dinheiro que entrou não é do negócio. (Fecomercio — fonte editorial.)

### ⚠️ Do briefing, NÃO verificados

- **404 mil MEIs receberam Termo de Exclusão do Simples por dívida em março de 2026**
- **59% controlam finanças em caderno, 15% de cabeça** — sustenta a frase *"o concorrente real não é um app"*, que é afirmação de mercado forte. **Prioridade de verificação.**

### ⚠️ Ainda em aberto

**Total de MEIs ativos:** fontes divergem entre 11,5, 12,9 e 16,8 milhões. **Puxar do Portal do Empreendedor ou dos dados abertos da Receita antes de usar.**

Bônus encontrado na verificação: **mais de 1 milhão de CNPJs excluídos da categoria em 2024 por acúmulo de dívidas** — métrica diferente do Termo de Exclusão de março/2026.

### Fontes

- https://www.gov.br/receitafederal/pt-br/assuntos/noticias/2025/novembro/simples-nacional-entenda-as-regras-da-resolucao-cgsn-no-183-2025-e-se-proteja-contra-fake-news
- https://www.cartacapital.com.br/do-micro-ao-macro/570-mil-meis-foram-desenquadrados-em-2024-por-excesso-de-faturamento-reforcando-expansao-da-economia/
- https://rn.agenciasebrae.com.br/economia-e-politica/cerca-de-60-dos-meis-ainda-misturam-financas-do-negocio-com-contas-pessoais/
- https://agenciasebrae.com.br/dados/meis-lideram-abertura-de-empresas-no-pais-e-ja-representam-78-dos-novos-negocios-em-2026/
- https://www.letsmoney.com.br/open-finance/open-finance-pj-burocracia-socios-credito
- https://simplifique.contmatic.com.br/blogs/mei-2026-limite-faturamento-o-que-muda
- https://www.fecomercio.com.br/noticia/conta-mei-conta-pessoal-misturar-da-confusao-e-pode-custar-o-seu-cnpj

---

## 11. Custo de infraestrutura

*(Do briefing, seção 3.5. ⚠️ Origem: relatos de desenvolvedores no TabNews, não tabela oficial. Citar como tal.)*

A pergunta certa não é "quanto custa o Open Finance", é **quanto custa cada conta que o agente precisa ler**.

| Plataforma | Custo reportado | Unidade | Observação |
|---|---|---|---|
| **Pluggy** | R$ 2.500/mês | plano fechado | limite de contas não divulgado |
| **Belvo** | R$ 6.000/mês | até 25 links | acima disso, negociação |
| **Tecnospeed** | R$ 1.500 + R$ 540/mês | plano fechado | limite não confirmado |
| **Celcoin** | por transação | sem setup | valor não divulgado |
| **Banco MCP** | **R$ 19,90/mês** | **por conta conectada** | único com preço unitário confirmado. Revende a Pluggy no varejo. |

**Cadeia de dependência:** Banco Central → Pluggy (licenciada ITP) → Banco MCP (revende) → nosso produto.
**Risco:** o intermediário não é oficial. Se o Banco MCP mudar preço ou sair do ar, o acesso quebra.

**Calculadora** (5 contas por usuário, R$ 9,90 por conta acima da faixa base):

| Usuários | Contas | Custo/mês |
|---|---|---|
| 10 | 50 | R$ 499 |
| 50 | 250 | R$ 2.495 |
| 200 | 1.000 | R$ 9.980 |

**Benchmark:** Plaid cobra US$ 0,30 a 1,00 por conta (Auth) e US$ 0,05 a 0,15 por chamada (Balance). Não cobre bancos brasileiros — serve só de referência.

**Para o MEI:** costuma ter menos contas que a média (PJ, PF e maquininha). **Custo de infra por usuário: R$ 40 a 60/mês.**

⚠️ **Isso pressiona o preço final.** O FinAI cobra R$ 29,90/mês. Ver a ressalva em `INSIGHTS.md`.

**Alternativa gratuita:** o **sandbox da Pluggy é gratuito e sem aprovação**.

---

## 12. Decisões tomadas

*(Do briefing, seção 4.)*

### ✅ Decisão 5 — Canal (FECHADA)

**O agente mora no chat. O app existe só como apoio.**
**MVP no Telegram, produto final no WhatsApp.** O Telegram tem API de bot gratuita, sem aprovação, criada em 2 minutos pelo BotFather, com botões, foto e PDF. O WhatsApp é o destino — é onde o ICP vive. A troca é só de canal: agente, motor e mensagens são os mesmos.

**Consequências:**
- **Entrada de dados pela conversa.** Print do extrato, PDF da fatura, foto do comprovante, notificação encaminhada. Importar CSV vira exceção.
- **Fato, regra e suspeita viram três tons de mensagem**, não três caixas de tela.
- **A resposta do usuário ensina o sistema.** "Foi eu sim" registra a contraparte.
- **Resumo de tranquilidade periódico** — segunda de manhã ou dia 20 antes do DAS.
- **O app é a memória.** Nunca obrigatório. Se a demo tiver que escolher, o chat roda e o app vira slide.

### Recomendadas, a confirmar

| Decisão | Recomendação do briefing |
|---|---|
| **1 · Usuário** | **MEI como personagem central**, com motor cobrindo também anomalias de PF (duplicata, recorrência, aumento de preço) |
| **2 · Enquadramento** | **B (julgamento) como coração, com toque de C (resolução)** para as anomalias de fato |
| **3 · Dados** | **Extrato sintético em CSV/JSON**, com anomalias plantadas. Ser honesto no pitch. Sandbox da Pluggy só se sobrar tempo. |
| **4 · Métrica** | **Dinheiro encontrado + tempo entre o vazamento e a ação.** "R$ X encontrados em Y segundos, que ficariam Z meses sem ninguém ver." |

### Escopo de 24 horas

**Obrigatórios:** agente no Telegram ao vivo · motor com os três níveis de certeza · IA lendo print/PDF e redigindo contestação · app web de apoio · pitch de 3–5 min com demo no celular · nome e identidade mínima.

**Fora do escopo (dizer no pitch, com orgulho):** integração real com Open Finance ou Receita · detecção estatística com baseline · fluxo multi-pessoa (PJ) · monetização definida.

**Corte de emergência, nesta ordem:** (1) app vira screenshot, (2) leitura de print vira CSV colado, (3) suspeitas saem da demo, (4) Telegram vira simulador de chat.
**Não caem:** o agente conversando, o motor fiscal MEI e a duplicidade.

**Regra do time:** a partir da hora 18, ninguém adiciona feature. Só conserta.

---

## 13. Documentos publicados

Todos privados — abrem só para quem receber o compartilhamento.

| Documento | Link |
|---|---|
| **O Que Sabemos Até Aqui** | https://claude.ai/code/artifact/454a74dc-3f15-4824-8de6-1b07ca7b042b |
| **14 Conversas Sobre Fatura** | https://claude.ai/code/artifact/3127dae6-d010-4b0d-a027-1eaadd7249bd |
| **Catálogo de Anomalias** | https://claude.ai/code/artifact/a3089b00-2387-4145-874b-370ca067fc8d |
| **De Onde Vem o Dado** | https://claude.ai/code/artifact/21f66939-eda8-452c-b377-3c76c82fdf84 |
| **Onde o Dinheiro Vaza** | https://claude.ai/code/artifact/e50d18cd-7f57-49b1-b74e-83eb39ae7711 |

---

## 14. Ressalvas

**Amostra pequena e por conveniência.** 14 pessoas da rede da equipe. Os números descrevem este grupo, não o mercado.

⚠️ **Parte dos entrevistados vem da rede pessoal do time**, incluindo parentes de integrantes. Se um jurado perguntar quem foi entrevistado, *"14 pessoas"* e *"nossas famílias"* têm pesos diferentes. **Ter a resposta pronta.**

**"6 de 14" é menção espontânea, não incidência.** Ninguém foi perguntado diretamente sobre nenhuma anomalia. **Ausência de menção não é ausência do problema.**

**Um terço não é cliente.** E9, E10, E7, E5 e E6 têm dor baixa ou nenhuma.

**Autorrelato, sem observação.** Frequência e tempo até perceber são sujeitos a imprecisão de memória.

**A pesquisa não capturou valores.** Sabemos os tempos, não os montantes. Faltam três perguntas: *quanto era? por quantos meses? recuperou tudo?*

**Zero entrevista com MEI.** A mitigação do briefing (cada um manda para 2 MEIs nas primeiras 3 horas) acontece **depois** da hora em que a Decisão 1 deveria estar fechada.

**Erros de transcrição corrigidos nas citações:** "mestrado" → MasterCard, "NSS" → INSS, "esquecer na internet" → pesquisar na internet, "combrança" → cobrança.

**As regras de detecção não foram testadas contra dado real.** Limiares (24h para duplicidade, 28–31 dias para recorrência) são pontos de partida.

**Custos de Open Finance vêm de relatos de desenvolvedores**, não de tabela oficial.

**O mercado se move.** O quadro de concorrentes é de 29/08/2026.

**Contém respostas identificadas.** Nomes, bancos e valores. **Não sobe em repositório público, não vai em slide sem anonimizar.**
