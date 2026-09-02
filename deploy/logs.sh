#!/usr/bin/env bash
# Mostra os logs da Regis no VPS. Use -f para acompanhar ao vivo.
set -euo pipefail
VPS_HOST="${VPS_HOST:-root@SEU_IP_DO_VPS}"
TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT
printf '#!/bin/sh\nprintf "%%s\\n" "$VPS_PASS"\n' > "$TMP/askpass.sh"; chmod 700 "$TMP/askpass.sh"
printf 'VPS_PASS=pass://SEU_COFRE/SSH VPS/password\n' > "$TMP/pass.env"
pass-cli run --env-file "$TMP/pass.env" -- \
  env SSH_ASKPASS="$TMP/askpass.sh" SSH_ASKPASS_REQUIRE=force \
  ssh -o StrictHostKeyChecking=accept-new "$VPS_HOST" "docker logs ${1:---tail 40} regis-bot"
