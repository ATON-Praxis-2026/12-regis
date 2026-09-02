---
titulo: Insights da pesquisa
tipo: insight
status: vigente
atualizado: 2026-08-29
autor: Time 12 · Hackathon Vanguarda
resumo: O que as 14 conversas confirmaram, quais hipóteses do time caíram e por que o gargalo está em entender, não em resolver.
---

# INSIGHTS — o que concluímos

> Interpretação, conclusões e o que ainda precisa ser resolvido.
> Para os dados e as fontes, ver `DOSSIE.md`. Para concorrentes, `CONCORRENTES.md`.
>
> Atualizado em 29/08/2026, depois do BRIEFING do time.

---

## O problema central

> **O extrato é escrito na língua do sistema de pagamentos, não na língua da vida da pessoa — e por isso ela não reconhece o que é dela.**

Um estacionamento aparece com o CNPJ de um mercado. Um Pix crédito aparece com o nome de um desconhecido. Uma expansão do Google aparece como um código.

Nas palavras deles:

- **E3:** *"fico me perguntando o que diabos é isso"*
- **E10:** *"apareceu um nome estranho na fatura"*
- **E7:** *"tem um nome que não ajuda muito a descobrir quem é"*
- **E11:** *"parece que fazem pra você ter que ficar olhando dez vezes"*

**E como ninguém sabe, todo mundo chuta.** E12 chutou que era dele e pagou. E3 chutou que não era dela e cancelou um serviço que usava. E7 não quis chutar e gastou 3 horas no Google por R$ 30. E13 cansou de chutar e parou de olhar.

**Não é o dinheiro sumindo. É a pessoa não reconhecer a própria vida no extrato — e ter que adivinhar.**

No vocabulário do briefing: o gargalo está em **Entende**, não em **Resolve**.

---

## Cinco coisas que acreditávamos e não se sustentaram

### 1. "Contestar é difícil, o valor está em agir pelo usuário" → **falso**

**10 pessoas contestaram. 10 recuperaram o dinheiro.** A maioria achou simples.

> E5: *"rapidamente eles estornam"* — inclusive R$ 3.000
> E10: *"prontamente cancela e resolve"*
> E4: *"contestei pelo app e foi estornado"*

Só 3 relataram atrito: E14 (*"muito trampo"*), E2 (*"tive que provar"*), E8 (não gostou do reembolso via desconto).

**Consequência:** o gargalo não é `Age → Resolve`. É **`Percebe`** e sobretudo **`Entende`**.

### 2. "As pessoas deixam passar por preguiça" → **falso**

9 de 14 negaram com veemência. O único "sim" espontâneo foi o do E12: *"imaginei que tivesse feito mesmo."*

**O dinheiro não vaza por negligência. Vaza por incapacidade de reconhecer.** E o erro acontece **nas duas direções**: E12 pagou o que não era dele, E3 cancelou o que era. Ninguém foi desatento — os dois estavam prestando atenção e erraram assim mesmo.

### 3. "Reajuste sorrateiro é uma das maiores dores" → **zero evidência**

Nenhuma menção em 14 entrevistas. **Fica no código** (é a anomalia mais fácil, sai quase de graça depois da recorrência). **Sai do pitch** como dor validada.

### 4. "Fraude é o gancho mais forte" → **é comum, mas o banco pega primeiro**

4 de 14 tiveram clonagem. Mas o Bradesco avisou a E5 **antes** de ela ver, e o cartão da E2 foi bloqueado **automaticamente**. Antifraude de emissor é maduro. **Não dá para ganhar aí.**

### 5. "Identificar o estabelecimento é detalhe técnico" → **é o produto**

Dor mais citada (6 de 14, espontânea) e **pré-requisito de quase todas as outras detecções**.

---

## Três achados que sustentam o projeto

### 1. O produto não muda o valor. Muda o tempo.

```
custo do vazamento = valor da cobrança × meses até alguém perceber
```

A pesquisa **não capturou os valores**, mas capturou os **tempos**:

| Como acompanha | Tempo até perceber |
|---|---|
| Recebe aviso externo (push, mensagem do banco) | **imediato** |
| Tem ritual mensal | **~1 mês** |
| Não olha | **3 a 5 meses, ou nunca** |

**O produto move todo mundo para a primeira faixa — e o ganho é maior em quem hoje está na última.** Numa recorrência, multiplica: os 5 meses do E4 são cinco cobranças.

Isso valida a métrica escolhida no briefing: **dinheiro encontrado + tempo entre o vazamento e a ação.**

### 2. Duas peças destravam cinco das doze anomalias

**Identificação de estabelecimento** e **detecção de recorrência**. A primeira é pré-requisito da segunda, da duplicidade e do reajuste.

**O esforço não se divide por anomalia. Concentra em duas peças.** E depois que toda linha está identificada, a anomalia se detecta quase sozinha. O problema difícil nunca foi a matemática — era resolver identidade. É aí que LLM ganha de regex, o que justifica IA no projeto em vez de ser enfeite.

### 3. Existe um usuário que escreveu a especificação

> **E13:** *"Eu olharia mais o extrato se tivesse alguma forma automática de categorizar as coisas e me mostrar só o que fosse relevante ou atípico."*

---

## O que o briefing acrescentou — e onde ele nos corrigiu

Três coisas do briefing são melhores que a análise anterior:

**O ciclo de seis etapas** (Acontece → Aparece → Percebe → **Entende** → Age → Resolve) é mais preciso que a cadeia de cinco. Separar *Percebe* de *Entende* é exatamente a distinção que a pesquisa pedia.

**O eixo fato / regra / suspeita, com autonomia proporcional à certeza.** Mesma intuição do "limiar de quando falar", mas virou tese comunicável, com três comportamentos distintos. **É o diferencial mais forte do projeto** — e nenhum concorrente comunica isso.

**MEI como resolução do impasse PF/PJ.** A recomendação anterior aqui era *"construir PF, narrar PJ"*. **Está superada.** O MEI é PJ no papel e PF na prática — uma pessoa só decide, paga e resolve — **e carrega uma camada de regra pública e idêntica para todos** (teto de R$ 81 mil, DAS dia 20, DASN em maio). Ganha-se a camada de regra sem cadastrar política nenhuma. É melhor.

**E o problema do dia 1**, que não tínhamos levantado: sem histórico, o sistema fica mudo ou grita para tudo. A saída adotada — a resposta do usuário na conversa constrói o "normal", sem tela de configuração — é elegante e demonstrável.

---

## A concorrência: o que falta no briefing

⚠️ **O briefing não menciona concorrentes em nenhuma seção** — nem nas referências, nem nos riscos.

Isso é perigoso porque o **ALL** (myall.com.br) já tem Open Finance com **120+ instituições, +1 milhão de transações classificadas por IA, PF e PJ separados na mesma conta**, e parceria de distribuição com o curso do Gustavo Cerbasi.

**A pergunta mais perigosa do pitch:** *"por que isso não é só uma feature deles?"*

**A resposta é forte, só não está escrita:**
- O ALL classifica para **preencher um orçamento**, não para achar o que está errado
- É declaradamente **assistivo**: *"o que muda o seu dinheiro só acontece depois que você confirma"*
- É um produto que **você abre**: *"é isto que você abre todo dia"*
- **Não tem nada de fiscal do MEI**

A tese fato/regra/suspeita é literalmente o que ele não faz. **Adicionar ao risco 9 e uma linha ao pitch.**

E o **FinAI** é o oposto de nós — registro 100% manual, *"não precisa conectar banco"*. Não pode achar vazamento invisível por construção. Rodando as 14 entrevistas contra ele: **só a E5 seria cliente.**

**Nenhum produto independente do mercado procura o usuário.** Todos esperam ser abertos. A única coisa proativa é o push do banco — e só vê o próprio banco, quase só para fraude. **É esse o espaço.**

---

## Verificações: o que confere e o que corrigir

### ✅ Confere

**Resolução CGSN nº 183/2025.** Real, em vigor, efeitos desde 01/01/2026. Receita no CPF soma ao limite do MEI.
⚠️ **Mas a Receita Federal publicou nota desmentindo fake news sobre ela**, e há questionamento constitucional. Dizer com precisão, sem dramatizar. Se um jurado for contador, ele conhece a polêmica.

**570 mil MEIs desenquadrados em 2024.** Dados da Receita Federal. **30 vezes mais que em 2023.**

**E tem um ganho que o briefing não está usando:** o salto é atribuído ao **cruzamento de Pix, cartão e transações pela Receita**.

> **O Estado começou a cruzar os dados do MEI. O MEI é o único que não cruza os próprios dados.**

Muito mais forte que citar o número seco.

### ❌ Corrigir

**"Teto congelado desde 2019" → é desde 2018.** O limite de R$ 81 mil passou a valer em janeiro de 2018.

**"61% dos empreendedores usam conta pessoal"** — a fonte descreve o número de três formas: ~60% para *MEIs*, 61% para *pequenos negócios* em geral, e outra redação fala em "usar recursos de PF na empresa". **São populações diferentes**, e o dado é de 2022-2023. Citar como *"cerca de 60% dos MEIs, Sebrae, 2023"*.

### ⚠️ Não verificados — prioridade

- **404 mil Termos de Exclusão em março/2026**
- **59% em caderno, 15% de cabeça** — sustenta *"o concorrente real não é um app"*, que é afirmação de mercado forte

---

## Três problemas práticos a resolver

### 1. Sequenciamento no cronograma

A **Decisão 1** (quem é o usuário) fecha na **hora 1**. As entrevistas com MEI acontecem *"nas primeiras 3 horas"*.

**Vocês vão decidir MEI antes de as entrevistas voltarem.**

Ou assumem que elas são cor para o pitch e não validação — legítimo, mas precisa ser consciente — ou **alguém dispara as mensagens agora, antes da hora 0**.

### 2. A conta da monetização não fecha no slide

O pitch diz: *"R$ 19,90 por conta, um MEI tem 2 a 3 contas, o produto se paga com uma duplicata evitada por mês."*

Mas 2–3 contas = **R$ 40 a 60/mês de custo**, e o FinAI cobra R$ 29,90. Se o jurado fizer a conta, pergunta quanto vocês cobram — e a resposta é desconfortável.

O briefing já sabe (*"monetização direta é difícil"*), mas o **slide 5 não**. Ou tirem o número, ou já entrem com *"por isso a distribuição é via banco, adquirente ou contador"*.

### 3. "570 mil desenquadrados" tem contra-narrativa

A imprensa enquadrou como notícia **boa** — negócios crescendo. A CartaCapital titula *"reforçando expansão da economia"*.

Se apresentarem como tragédia, alguém devolve: *"isso não é bom?"*

**Resposta pronta:** crescer é ótimo. **Ser pego de surpresa retroativamente, com multa de 0,33% ao dia e recálculo do ano inteiro, não é.** O produto não impede crescer — impede ser surpreendido.

---

## Duas adições ao pitch

**O erro nos dois sentidos.** O briefing usa o E12 (*"imaginei que tivesse feito mesmo"*) mas não o par dele: a **E3 cancelou serviços que usava** por não lembrar o que eram. Juntos, provam que o problema é **reconhecimento, não negligência** — os dois estavam prestando atenção e erraram assim mesmo. É o argumento mais forte que a pesquisa produziu.

**Mostrar o agente decidindo ficar calado.** A demo dispara as três mensagens. Se mostrar também **algo que o agente achou e escolheu não mandar**, isso prova a tese fato/regra/suspeita melhor que os três alertas juntos — e é o que separa autopilot de relatório agendado. Custa uma linha.

---

## Um ponto delicado

Parte dos entrevistados vem da rede pessoal do time, e alguns são parentes de integrantes.

Se um jurado perguntar quem foi entrevistado, *"14 pessoas"* e *"nossas famílias"* têm pesos bem diferentes. Não é problema, pesquisa de conveniência em 24h é isso, mas **tenham a resposta pronta e não deixem descobrir**.

E reforça o alerta do próprio briefing: **o relatório com nomes não sobe em repositório público e não vai em slide sem anonimizar.**

---

## Frases para o pitch

| Momento | Frase | Quem |
|---|---|---|
| **Abertura** | *"Eu olharia mais o extrato se tivesse alguma forma automática de me mostrar só o que fosse relevante ou atípico."* | E13 |
| **O problema** | *"Na maioria das vezes tem um nome que não ajuda muito a descobrir quem é."* — 3h e uma busca no Google por R$ 30 | E7 |
| **O erro nos dois sentidos** | *"Porque imaginei que tivesse feito mesmo."* + E3 cancelando o que usava | E12 / E3 |
| **A raiva** | *"Parece que fazem pra você ter que ficar olhando dez vezes."* | E11 |
| **O fechamento** | *"São coisas que a gente tem que começar, principalmente na nossa idade, a entrar mais vezes."* | E8 |

**A frase do briefing:**

> *"O vazamento do MEI não é só o que sai. É o que entra sem ele perceber."*

**A tese:**

> Autonomia proporcional à certeza. Fato ele resolve, regra ele encaminha, suspeita ele pergunta.

**O reenquadramento:**

> Não é um detector de anomalias. É um tradutor — e a detecção é o que sobra depois que tudo está traduzido.

**Contra o ALL:**

> Orçar e vigiar são trabalhos diferentes. Orçamento pressupõe que você vai olhar. Nosso usuário não olha — e para ele o produto tem que falar primeiro.

---

## Riscos conhecidos

**"E daí?"** — mostrar a anomalia sem oferecer a ação. É a morte do Guiabolso repetida.

**Alarme demais.** Vira notificação silenciada em três dias. Cinco achados certos valem mais que quarenta duvidosos. *(O briefing resolve isso bem: uma pergunta por vez, resumo no máximo semanal, suspeita agrupa e espera.)*

**Falar como banco.** *"Achei R$ 47 por mês saindo à toa"*, não *"detectamos outlier no cluster 3"*.

**Tom de imposto gera medo em vez de alívio.** O produto vende tranquilidade e controle, nunca ameaça.

**LGPD e confiança.** Dado financeiro é o mais sensível que existe. Ter resposta de 20 segundos sobre consentimento, escopo e não-compartilhamento.

**Um terço da amostra não é cliente.** E9, E10, E7, E5 e E6 têm dor baixa ou nenhuma — E6 nem cartão de crédito tem. **A banca vai encontrar isso; melhor sermos nós a dizer.**

**Zero entrevista com MEI**, e a decisão está sendo tomada antes da mitigação chegar.

**O intermediário do Open Finance não é oficial.** Banco MCP revende a Pluggy. Se mudar preço ou sair do ar, o acesso quebra. Citar custos como *"relatos de desenvolvedores"*, não como tabela.
