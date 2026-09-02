# A Regis tem uma dependência só, o SDK da Anthropic, que serve para a conversa
# livre com IA. Sem ele o bot ainda sobe, só sem conversa livre.
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TZ=America/Sao_Paulo \
    REGIS_MEMORIA=/dados/memoria.json

WORKDIR /app

# As dependências entram antes do código, para o cache da camada aproveitar.
COPY bot/requirements.txt /app/bot/requirements.txt
RUN pip install --no-cache-dir -r bot/requirements.txt

# Só o que a Regis precisa para rodar. O resto do repositório fica de fora.
COPY bot/    /app/bot/
COPY motor/  /app/motor/
COPY dados/  /app/dados/
COPY web/    /app/web/
COPY ui/     /app/ui/
COPY idv/    /app/idv/
COPY pitch/  /app/pitch/

# A memória vive num volume, para sobreviver a cada atualização de código.
RUN mkdir -p /dados

# Roda como usuário comum, não como root.
RUN useradd --create-home --uid 10001 regis && chown -R regis:regis /app /dados
USER regis

CMD ["python3", "-u", "bot/regis_bot.py"]
