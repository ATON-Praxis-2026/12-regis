---
titulo: O bot da Regis no Telegram
tipo: referencia
status: vigente
atualizado: 2026-08-29
autor: Time 12 · Hackathon Vanguarda
resumo: Como criar o bot no BotFather, onde colar o token, como rodar, como ligar a conversa livre com IA e como ensaiar a demo sem rede.
---

# bot/

A Regis no Telegram. Python 3, sem servidor. Você cola um token, roda um comando e o bot responde.

Os comandos são 100% determinísticos e não precisam de dependência nenhuma. A conversa livre com IA é a única parte que pede `pip install`, e ela é opcional: sem o SDK instalado o bot sobe igual e responde do jeito que sempre respondeu.

| Arquivo | O que é |
|---|---|
| `regis_bot.py` | O bot. Fala com a Bot API por `urllib` e recebe mensagem por long polling. |
| `conversa_ia.py` | A conversa livre. Manda a pergunta para o Claude com ferramentas que leem o motor. Opcional. |
| `simular.py` | A conversa inteira no terminal, sem token e sem rede. É o ensaio da demo e o plano B. |
| `stub_motor.py` | Motor de mentira, só com os dados da demo. Só entra em cena se `motor/detectar.py` não existir. |
| `requirements.txt` | A única dependência, o SDK da Anthropic. Só serve para a conversa livre. |
| `memoria.json` | Criado na primeira resposta. É onde a Regis guarda quem você já disse que conhece. |

## Antes de tudo, o teste sem token

Se você tem pressa e só quer ver o produto funcionando, comece por aqui. Não precisa de token, de internet nem de nada:

```bash
python3 bot/simular.py
```

A conversa inteira roda no terminal, com as pausas, na ordem da demo. Para conferir o texto sem esperar as pausas, use `python3 bot/simular.py --rapido`.

## Passo a passo para colocar o bot no ar

### 1. Crie o bot no BotFather

1. Abra o Telegram e procure por **@BotFather** (o verificado, com o selo azul).
2. Mande `/newbot`.
3. Ele pergunta o **nome**, que é o que aparece no topo da conversa. Responda `Regis`.
4. Ele pergunta o **username**, que precisa terminar em `bot` e ser único no mundo. Tente `RegisMEIbot`. Se der ocupado, vá variando (`RegisFinanceiroBot`, `RegisAutopilotBot`) até ele aceitar.
5. Ele responde com uma linha assim:

   ```
   Use this token to access the HTTP API:
   8123456789:AAF3xO_exemplo_de_token_nao_use_esse
   ```

   **Esse é o token.** Copie inteiro, incluindo os números antes dos dois pontos.

### 2. Deixe o bot com cara de produto (2 minutos, e aparece no pitch)

Ainda no BotFather, com o bot recém criado selecionado:

- `/setdescription`, e cole: `Eu confiro o dinheiro que entra e sai da sua conta. Você já faturou quanto este ano?`
- `/setabouttext`, e cole: `Autopilot financeiro para MEI. Confere, soma, projeta e prepara o documento.`
- `/setuserpic`, e mande a imagem que o Márcio fizer. Sem foto, o jurado vê um boneco cinza.

A lista de comandos do menu o próprio `regis_bot.py` registra sozinho quando sobe, então você não precisa de `/setcommands`.

### 3. Rode

Do diretório raiz do repositório:

```bash
TELEGRAM_TOKEN=8123456789:AAF3xO_exemplo_de_token_nao_use_esse python3 bot/regis_bot.py
```

Se der certo, aparece:

```
[regis] conectado como @RegisMEIbot, motor: motor
[regis] escutando. Abra o Telegram, procure @RegisMEIbot e mande /start.
```

A linha `motor:` diz de onde vêm os números. `motor` é o motor de verdade. `stub` quer dizer que `motor/detectar.py` ainda não existe e o bot está usando os dados de exemplo, o que é normal antes da integração.

Para não colar o token toda vez, exporte na sessão do terminal:

```bash
export TELEGRAM_TOKEN=8123456789:AAF3xO_exemplo_de_token_nao_use_esse
python3 bot/regis_bot.py
```

O token dá controle total do bot, então ele fica só no seu terminal. Não coloque em arquivo versionado.

### 4. Teste do jeito que importa

No Telegram, procure o username do seu bot e mande:

1. `/start`, que responde com quanto você faturou no ano e quanto falta pro teto.
2. `/conferir`, que manda os achados na ordem, fato primeiro, depois regra, e uma pergunta só no fim.
3. Toque em **Ver o texto** em qualquer achado, que ela devolve a contestação pronta.
4. Toque em **Foi eu** na pergunta, que ela responde "anotei, não pergunto mais sobre ela" e grava em `bot/memoria.json`.
5. `/conferir` de novo. A pergunta sobre aquela pessoa não volta. Esse é o momento que prova o aprendizado, e vale ensaiar.

Outros comandos: `/resumo` (o resumo do mês, formatado para encaminhar para a contadora), `/silencio` (o que ela achou e escolheu não mandar) e `/teto`.

Qualquer texto solto também funciona. Pergunte "quanto eu faturei?", "e o das?", "o que você deixou passar?" ou peça para ela pagar alguma coisa, e veja o que ela responde.

## A conversa livre com IA (opcional)

Sem isto, qualquer pergunta fora dos comandos cai numa frase genérica ("Não peguei essa, mas te digo o que eu tenho na mão agora"). Com isto ligado, ela responde de verdade: "quanto eu gastei com fornecedor esse mês?", "qual foi meu maior gasto?", "me explica melhor essa taxa da maquininha".

### Como ligar

```bash
pip3 install --user -r bot/requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
export TELEGRAM_TOKEN=8123456789:AAF...
python3 bot/regis_bot.py
```

Faltando o SDK, faltando a chave ou faltando os dados, o bot avisa no terminal e segue só no determinístico. Nenhum comando depende disso.

### A regra que não se quebra: ela nunca inventa um número

O modelo **não** recebe um resumo mastigado no prompt para escrever em cima. Ele recebe sete ferramentas que leem `motor/` e `dados/` na hora e devolvem texto curto e conferido. Se a resposta não estiver em nenhuma ferramenta, ela diz que não sabe.

| Ferramenta | Devolve |
|---|---|
| `resumo_do_ano` | faturamento, teto, quanto falta, projeção de estouro, total recuperável |
| `listar_achados` | os achados do motor, filtrando por fato, regra ou suspeita |
| `total_por_canal` | quanto entrou por maquininha, marketplace, Pix e boleto, bruto e líquido |
| `maiores_saidas` | as maiores saídas do período, mais o total por categoria |
| `buscar_transacoes` | lançamentos por nome de contraparte ou por descritor |
| `gastos_com` | quanto já saiu para uma contraparte, e quantas vezes |
| `o_que_calei` | o que o motor conferiu, achou normal e escolheu não falar |

Os dados carregam uma vez por processo e ficam em cache, então as sete ferramentas juntas custam um `json.load`, não sete.

### Quando ela entra, e quando não entra

Ela só entra no caso genérico, quando o determinístico não entendeu. Saudação, `teto`, `das`, `resumo` e `conferir` continuam saindo do código, instantâneos, e a demo por comandos não passa perto da IA.

A única exceção é quando a pessoa cita um canal ("quanto entrou por maquininha em agosto?"). Isso não é pergunta de teto, então vai para a IA, que responde com o número por canal. Com a IA desligada, essa pergunta volta a cair no teto, como sempre caiu.

Se a IA falhar por qualquer motivo (sem chave, sem rede, erro na API, teto de gasto estourado), o bot manda a resposta determinística de hoje. Ela nunca deixa a pessoa sem resposta.

### Teto de gasto

A chave é do time, então quem conversa com o bot gasta o crédito do time. Depois que o link circular, isso deixa de ser hipótese.

| Variável | Padrão | O que faz |
|---|---|---|
| `REGIS_LIMITE_HORA` | `20` | chamadas por pessoa por hora |
| `REGIS_TETO_USD` | `5.00` | teto de gasto estimado da sessão, em dólar |

Ao estourar qualquer um dos dois, ela responde uma frase educada e **não chama a API**. Cada chamada imprime o custo estimado no terminal:

```
[regis-ia] entrada 6554 tokens, saída 175 tokens, custo estimado US$ 0.0371, acumulado US$ 0.0371 de US$ 5.00
```

Na prática, uma pergunta custa entre US$ 0,02 e US$ 0,07 (Claude Opus 5, US$ 5,00 de entrada e US$ 25,00 de saída por milhão de tokens). Cem perguntas dão uns US$ 4,00.

## Na hora do pitch

- Rode o bot em um terminal que você não vá fechar. Enquanto ele estiver rodando, ele responde.
- `/esquecer` zera a memória e devolve as perguntas. É o que permite repetir a demo do zero.
- Se o tempo apertar, suba com ritmo acelerado: `REGIS_RITMO=0.3 TELEGRAM_TOKEN=... python3 bot/regis_bot.py`. Com `REGIS_RITMO=0` as mensagens saem de uma vez, sem pausa nenhuma.
- Se a rede do evento cair, abra o `simular.py` na tela. É a mesma conversa, saindo das mesmas funções.

## Quando alguma coisa não funciona

| O que aparece | O que é | O que fazer |
|---|---|---|
| `O Telegram não aceitou esse token` | Token errado ou cortado | Copie de novo do BotFather, inteiro, sem espaço no fim |
| `Falta o token` | A variável não chegou | Rode com `TELEGRAM_TOKEN=... python3 bot/regis_bot.py`, tudo na mesma linha |
| `getUpdates falhou: HTTP 409` | Duas cópias do bot rodando ao mesmo tempo, ou um webhook ligado | Feche o outro terminal. Se persistir, abra `https://api.telegram.org/bot<TOKEN>/deleteWebhook` no navegador |
| `motor real indisponível` | `motor/detectar.py` ainda não existe | Nada. É o esperado, o bot segue com o stub |
| `conversa com IA desligada` | O SDK da Anthropic não está instalado | `pip3 install --user -r bot/requirements.txt`. Sem isso o bot roda só no determinístico, o que também é aceitável |
| Pergunta solta cai na frase genérica | Falta `ANTHROPIC_API_KEY`, ou o teto de gasto estourou | Confira a variável no terminal e olhe as linhas `[regis-ia]` do log |
| O bot não responde e nada aparece no terminal | Você está falando com outro bot | Confira o username, é o mesmo que apareceu no `[regis] conectado como` |

## Como o bot conversa com o motor

O bot chama uma função só:

```python
from motor.detectar import detectar
resultado = detectar("dados")
# {"resumo": {...}, "achados": [...], "silenciados": [...]}
```

Se esse import falhar, ele cai em `bot/stub_motor.py`, que devolve exatamente o mesmo formato com os números do dataset sintético. Ou seja, o bot nunca fica de pé esperando o motor, e no dia que o motor entrar não muda uma linha aqui.

Dois campos opcionais melhoram o texto, se o motor quiser mandar. Nenhum dos dois é obrigatório:

- `contraparte`, o nome de quem está do outro lado. Sem ele, a memória usa o título do achado como chave.
- `recuperavel` (`true` ou `false`) e `periodicidade` (`"por mês"`), que decidem entre "dá R$ 55,90 de volta pro seu bolso" e "isso está te custando R$ 29,90 por mês". Sem eles, o bot deduz pelo `tipo`.

Nos `silenciados`, ele usa `motivo` se existir, e a primeira frase da `explicacao` se não existir. Se o valor já aparece escrito na explicação ou no título, o bot não repete o número, então texto rico do motor não vira eco.

A `projecao_estouro` pode vir como `2026-10-24` ou como `outubro de 2026`. No chat, a data ISO aparece como "24 de outubro de 2026", porque ninguém fala data em ISO.

## O que a Regis nunca faz

Ela não move dinheiro. Não paga, não transfere, não cancela cartão e não abre contestação no banco. Ela escreve o texto, mostra o passo a passo e quem aperta enviar é a pessoa. Se você for mexer no copy, essa é a linha que não pode ser cruzada.
