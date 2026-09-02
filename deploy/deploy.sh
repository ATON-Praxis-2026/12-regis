#!/usr/bin/env bash
# Manda a Regis para o VPS. Rode da raiz do repositório: ./deploy/deploy.sh
#
# Precisa de acesso ao Proton Pass (pass-cli destravado). A senha do VPS nunca
# aparece na tela nem fica em arquivo: o pass-cli injeta na hora.
set -euo pipefail

VPS_HOST="${VPS_HOST:-root@SEU_IP_DO_VPS}"
DESTINO="/opt/regis"
AQUI="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

cat > "$TMP/askpass.sh" <<'ASK'
#!/bin/sh
printf '%s\n' "$VPS_PASS"
ASK
chmod 700 "$TMP/askpass.sh"

cat > "$TMP/pass.env" <<'ENV'
VPS_PASS=pass://SEU_COFRE/SSH VPS/password
ENV

no_vps() {
  pass-cli run --env-file "$TMP/pass.env" -- \
    env SSH_ASKPASS="$TMP/askpass.sh" SSH_ASKPASS_REQUIRE=force \
    ssh -o StrictHostKeyChecking=accept-new "$VPS_HOST" "$@"
}
copiar() {
  pass-cli run --env-file "$TMP/pass.env" -- \
    env SSH_ASKPASS="$TMP/askpass.sh" SSH_ASKPASS_REQUIRE=force \
    scp -o StrictHostKeyChecking=accept-new -q -r "$@"
}

echo "==> preparando $DESTINO no VPS"
no_vps "mkdir -p $DESTINO/app"

echo "==> enviando código (bot, motor, dados, web, ui, pitch)"
no_vps "rm -rf $DESTINO/app/bot $DESTINO/app/motor $DESTINO/app/dados $DESTINO/app/web $DESTINO/app/ui $DESTINO/app/idv $DESTINO/app/pitch"
copiar "$AQUI/bot" "$AQUI/motor" "$AQUI/dados" "$AQUI/web" "$AQUI/ui" "$AQUI/idv" "$AQUI/pitch" "$VPS_HOST:$DESTINO/app/"
no_vps "rm -f $DESTINO/app/bot/.env $DESTINO/app/bot/memoria.json"

echo "==> enviando Dockerfile e compose"
copiar "$AQUI/deploy/Dockerfile" "$AQUI/deploy/docker-compose.yml" "$VPS_HOST:$DESTINO/"

echo "==> subindo o container"
no_vps "cd $DESTINO && docker compose up -d --build"

echo "==> logs (primeiras linhas)"
sleep 6
no_vps "docker logs --tail 8 regis-bot; echo; echo '--- web:'; docker logs --tail 6 regis-web"

echo
echo "Pronto. Para ver os logs depois:"
echo "  ./deploy/logs.sh"
