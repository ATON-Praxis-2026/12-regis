---
titulo: Como testar a Regis
tipo: referencia
status: vigente
atualizado: 2026-08-30
autor: Time 12 · Hackathon Vanguarda
resumo: Os comandos do bot, o que perguntar na conversa livre e o teste que mostra a Regis aprendendo.
---

# Como testar a Regis

**No Telegram:** [t.me/ChamaARegisBot](https://t.me/ChamaARegisBot)
**O app, ao vivo:** http://SEU_IP_DO_VPS:8090

O app pede login. A conta é uma só, a da Angela, e não existe cadastro:

| | |
|---|---|
| usuário | `angela` |
| senha | `TROQUE_ESTA_SENHA` |

A persona é a **Angela**, cabeleireira MEI que aluga uma cadeira num salão e recebe por duas maquininhas e um marketplace. **Todos os dados são simulados**, então pode testar à vontade.

## Os comandos, resposta na hora

| Comando | O que faz |
|---|---|
| `/start` | Quanto ela já faturou este ano |
| `/conferir` | Tudo que a Regis achou de errado, na ordem: o que ela resolveu, o que você decide, e uma pergunta só |
| `/resumo` | O resumo do mês, pronto para encaminhar para a contadora |
| `/teto` | Quanto ainda cabe antes do teto do MEI |
| `/silencio` | O que ela achou e **escolheu não avisar**, com o motivo de cada um |

Esses saem do código, são instantâneos e não gastam nada.

## Conversa livre

Qualquer outra coisa vira pergunta para a IA, que consulta os dados reais antes de responder. Leva uns segundos e aparece o "digitando".

Perguntas boas para testar:

- qual foi meu maior gasto?
- quanto entrou por maquininha em agosto?
- me explica essa taxa da maquininha
- quanto gastei com fornecedor esse mês?
- vale a pena eu virar ME?

**Ela nunca inventa número.** Se a pergunta não couber nas ferramentas que ela tem, diz que não sabe.

## O teste que vale a pena fazer

1. Manda `/conferir`
2. No fim vem uma pergunta sobre um **Pix de R$ 340 para Maria Souza**
3. Toca em **"Foi eu"**
4. Manda `/conferir` de novo

A pergunta não volta. E se o app estiver aberto numa tela, ele muda sozinho em até 3 segundos: a suspeita sai da lista e vai para os silenciados, com o motivo "você já respondeu no chat".

É a tese do produto em 30 segundos.

## As telas do app que não aparecem sozinhas

O app abre direto no painel, com os dados já lidos. Três estados só aparecem se você pedir na URL:

| Endereço | O que mostra |
|---|---|
| `regis-app.html#conectar` | O onboarding, antes de existir número. "Conectar conta" roda a conexão pelo Open Finance e o painel aparece depois. "Usar um exemplo" pula direto |
| `regis-app.html#vazio` | O dia em que nada precisa dela, com o card "Tudo em dia" |
| `regis-app.html#limpar` | Zera o que você marcou como enviado e devolve o app ao estado inicial |

Dentro da contestação da Netflix, **"Copiar texto"** copia o rascunho e **"Já enviei"** transforma o achado em acompanhamento. Esse segundo fica gravado no navegador, então use o `#limpar` antes de mostrar para outra pessoa.

## Duas coisas que ela recusa, de propósito

**Não mexe em dinheiro.** Ela prepara o texto da contestação, quem envia é a pessoa. Se pedirem "paga o DAS pra mim", ela explica que não faz isso e oferece o que sabe fazer.

**Não dá palpite de investimento.** Se perguntarem sobre bitcoin, ela desconversa e volta para o assunto do salão.

## Se algo der errado

O bot roda no VPS, não depende do notebook de ninguém. Para ver o que aconteceu:

```bash
./deploy/logs.sh
```

E existe o plano B que roda sem internet nenhuma:

```bash
python3 bot/simular.py
```


## A página de lista de espera

Para mandar para quem respondeu a pesquisa, ou para quem pedir depois do pitch:

**http://SEU_IP_DO_VPS:8090/lista.html**

Ela explica o problema, o que a Regis faz, e pega o e-mail de quem tiver interesse. Não pede login, é pública de propósito.

Para ver quem entrou:

```bash
./deploy/lista.sh          # na tela
./deploy/lista.sh csv      # exporta para abrir no Excel
```

Os e-mails ficam no volume do VPS, junto com a memória. Não passam por serviço nenhum de fora e não entram no repositório.
