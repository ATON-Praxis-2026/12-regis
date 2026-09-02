---
titulo: Deploy da Regis no VPS
tipo: referencia
status: vigente
atualizado: 2026-08-30
autor: Time 12 · Hackathon Vanguarda
resumo: Como a Regis roda no VPS, como atualizar o código e como ver os logs.
---

# deploy/

A Regis roda no VPS em `/opt/regis`, num container próprio. Ela não depende do seu notebook.

**O fluxo é sempre este:** edita o código, roda `./deploy/deploy.sh`, testa no celular. Ninguém precisa rodar o bot na própria máquina em momento nenhum.

| Arquivo | O que é |
|---|---|
| `Dockerfile` | Imagem `python:3.12-slim` com o código. Sem dependência nenhuma, porque o bot é stdlib puro. |
| `docker-compose.yml` | Sobe o container, monta o volume da memória e reinicia sozinho se cair. |
| `deploy.sh` | Manda o código atualizado e reconstrói. É o comando do dia a dia. |
| `logs.sh` | Mostra os logs. |

## Atualizar depois de mexer no código

Da raiz do repositório:

```bash
./deploy/deploy.sh
```

Demora menos de um minuto. Ele envia `bot/`, `motor/` e `dados/`, reconstrói a imagem e reinicia o container.

## Ver os logs

```bash
./deploy/logs.sh              # últimas 40 linhas
./deploy/logs.sh -f           # acompanha ao vivo, ctrl+C para sair
```

## O que fica onde

- **Código:** `/opt/regis/app/` no VPS, substituído a cada deploy.
- **Token:** `/opt/regis/.env`, criado uma vez, permissão 600, **nunca entra no repositório**.
- **Memória:** volume `regis-memoria`, montado em `/dados`. Sobrevive a atualização de código e a reinício do container. É onde fica o que a Regis aprendeu quando alguém respondeu "Foi eu".

## Ligar um domínio próprio (HTTPS)

Hoje o app atende em `http://SEU_IP_DO_VPS:8090`, sem depender de DNS.

Quando tiver um domínio, são dois passos e uns cinco minutos:

1. **No painel do domínio**, criar um registro **A** apontando para **SEU_IP_DO_VPS**. Pode ser o domínio raiz ou um subdomínio.
2. **Em `deploy/docker-compose.yml`**, trocar o `Host(...)` do serviço `web` pelo domínio, e rodar `./deploy/deploy.sh`.

O Traefik já está configurado e emite o certificado HTTPS sozinho, pelo Let's Encrypt, em segundos. A porta 8090 continua funcionando em paralelo, então nada quebra durante a troca.

Confira a propagação antes de rodar o deploy:

```bash
dig +short SEU-DOMINIO A     # tem que devolver SEU_IP_DO_VPS
```

## Cuidados no VPS

Este VPS roda outros projetos em produção: **n8n, Supabase e Traefik**. A Regis vive isolada em `/opt/regis`, com rede e volume próprios.

- Só mexa em `/opt/regis`.
- **Nunca rode `docker system prune`**, ele apagaria volumes dos outros projetos.
- A Regis não expõe porta e não passa pelo Traefik. Ela fala com o Telegram por long polling, ou seja, ela sai para a internet e ninguém entra nela.

## Se precisar parar ou reiniciar

```bash
./deploy/logs.sh                                     # ver o estado
ssh root@SEU_VPS "docker restart regis-bot"          # reiniciar
ssh root@SEU_VPS "docker stop regis-bot"             # parar
ssh root@SEU_VPS "cd /opt/regis && docker compose up -d"   # subir de novo
```

## Testar sem tocar no VPS

Para conferir texto e ordem das mensagens, use o simulador:

```bash
python3 bot/simular.py            # com as pausas, como na demo
python3 bot/simular.py --rapido   # sem pausas, só para ler o texto
```

Ele roda no terminal, não fala com o Telegram e não conflita com o container. É também o plano B do pitch, se a internet do evento falhar.

## Uma regra, só para constar

O Telegram aceita **um ouvinte por bot**. Como o fluxo daqui para frente é sempre deploy, isso não deve acontecer. Mas se alguém um dia rodar `python3 bot/regis_bot.py` na própria máquina com o container de pé, os dois brigam e nenhum responde. Nesse caso, pare o container antes.
