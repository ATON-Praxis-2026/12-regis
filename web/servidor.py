#!/usr/bin/env python3
"""
Servidor do app da Regis.

Faz duas coisas:
  1. serve os arquivos de ui/
  2. expõe /api/estado, que roda o motor e junta com o que a Regis aprendeu
     no Telegram (a memória), para o app refletir a conversa em tempo real.

Rodar local:
    python3 web/servidor.py
    # abre em http://127.0.0.1:8090

Variáveis:
    REGIS_PORTA    porta, padrão 8090
    REGIS_MEMORIA  caminho do memoria.json, padrão bot/memoria.json
"""
import http.server
import json
import os
import socketserver
import sys
import threading
import time
import base64
import hashlib
import hmac
import unicodedata
import urllib.parse
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

PORTA = int(os.environ.get("REGIS_PORTA", "8090"))
UI = os.path.join(RAIZ, "ui")
MEMORIA = os.environ.get("REGIS_MEMORIA") or os.path.join(RAIZ, "bot", "memoria.json")

# Porta de demonstração. Uma conta só, a da Angela, e ninguém se cadastra.
# Não é autenticação de verdade: serve para o app não ficar aberto na internet
# e para a demo começar pela tela de entrar, como um produto de verdade.
USUARIO = os.environ.get("REGIS_USUARIO", "angela")
SENHA = os.environ.get("REGIS_SENHA", "TROQUE_ESTA_SENHA")
SEGREDO = os.environ.get("REGIS_SEGREDO", "").encode() or hashlib.sha256(
    (USUARIO + SENHA + "regis").encode()).digest()
LOGIN_LIGADO = os.environ.get("REGIS_LOGIN", "1") not in ("0", "false", "nao")
# A raiz leva ao app. Só a lista de espera e o login ficam abertos.
LIVRE = ("/login.html", "/api/entrar", "/favicon.ico",
         # o arquivo virou espera.html no rename, e /espera e o atalho curto
         "/espera.html", "/espera", "/api/lista",
         # a pagina do QR do pitch. O jurado le o codigo e cai direto nela,
         # entao ela nao pode esbarrar em login.
         "/jurados.html", "/jurados",
         # as telas de conversa do pitch. São material de apresentação, não
         # dados de ninguém, então login ali só atrapalha quem abre o link.
         "/regis-conversa.html", "/regis-contestacao.html", "/regis-contadora.html",
         "/regis-telas.html", "/_padrao-conversa-whatsapp.html",
         # o deck do pitch. Abre no telão e em qualquer celular da banca.
         "/pitch", "/pitch/", "/pitch/regis-pitch.html")

# Aviso por e-mail a cada pessoa que entra na lista. Sem chave, ele só não acontece,
# e o cadastro é gravado do mesmo jeito.
RESEND_KEY = os.environ.get("RESEND_API_KEY", "").strip()
AVISO_PARA = os.environ.get("REGIS_AVISO_EMAIL", "contato@exemplo.com.br")
AVISO_DE = os.environ.get("REGIS_AVISO_DE", "Regis <regis@exemplo.com.br>")

# A lista de espera fica ao lado da memória, no volume, para sobreviver a deploy.
LISTA = os.environ.get("REGIS_LISTA") or os.path.join(
    os.path.dirname(MEMORIA), "lista-espera.json")


def assinar(quem):
    """Cookie assinado, para ninguém entrar escrevendo o cookie na mão."""
    marca = hmac.new(SEGREDO, quem.encode(), hashlib.sha256).hexdigest()[:32]
    return base64.urlsafe_b64encode(("%s:%s" % (quem, marca)).encode()).decode()


def conferir(cookie):
    try:
        quem, marca = base64.urlsafe_b64decode(cookie.encode()).decode().split(":", 1)
    except Exception:
        return False
    esperado = hmac.new(SEGREDO, quem.encode(), hashlib.sha256).hexdigest()[:32]
    return hmac.compare_digest(marca, esperado)

_trava = threading.Lock()
_cache = {"quando": 0.0, "dado": None, "assinatura": None}


def chave(nome):
    texto = unicodedata.normalize("NFKD", str(nome or ""))
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto.strip().lower()


def resposta_do_chat(achado, memoria):
    """
    O que a pessoa respondeu sobre este achado no Telegram, ou None.

    Procura primeiro pelo id do achado, que é como o bot grava e é casamento
    exato. Só cai no nome da contraparte se não achar, e aí exige nome inteiro
    igual: casar por pedaço fazia "Maria" silenciar "Maria Souza".
    """
    registrada = (memoria.get("respostas") or {}).get(achado.get("id"))
    if isinstance(registrada, dict) and registrada.get("resposta"):
        return registrada["resposta"]

    alvo = chave(achado.get("contraparte") or achado.get("titulo"))
    if not alvo:
        return None
    if any(c == alvo for c in memoria.get("conhecidas") or []):
        return "foi_eu"
    if any(c == alvo for c in memoria.get("negadas") or []):
        return "nao_fui_eu"
    return None


def ler_memoria():
    """O que a pessoa já respondeu no Telegram."""
    try:
        with open(MEMORIA, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
        if isinstance(dados, dict):
            return {
                "conhecidas": [chave(c) for c in dados.get("contrapartes_conhecidas", [])],
                "negadas": [chave(c) for c in dados.get("contrapartes_negadas", [])],
                "respostas": dados.get("respostas", {}),
                "mtime": os.path.getmtime(MEMORIA),
            }
    except Exception:
        pass
    return {"conhecidas": [], "negadas": [], "respostas": {}, "mtime": 0}


def avisar_por_email(registro, total):
    """
    Manda um e-mail avisando que alguém entrou na lista.

    Roda numa thread para não segurar a resposta da pessoa que se cadastrou.
    Se falhar, o cadastro continua salvo, e o erro sai no log.
    """
    if not RESEND_KEY:
        return

    def enviar():
        quem = registro.get("nome") or registro.get("email")
        linhas = ["Alguém entrou na lista de espera da Regis.", ""]
        linhas.append("E-mail: %s" % registro.get("email", ""))
        if registro.get("nome"):
            linhas.append("Nome: %s" % registro["nome"])
        if registro.get("perfil"):
            linhas.append("Perfil: %s" % registro["perfil"])
        if registro.get("canais"):
            linhas.append("Recebe por: %s" % registro["canais"])
        linhas.append("Quando: %s" % registro.get("quando", ""))
        linhas.append("")
        linhas.append("Agora são %d na lista." % total)
        linhas.append("")
        linhas.append("Para ver todos: ./deploy/lista.sh")

        corpo = json.dumps({
            "from": AVISO_DE,
            "to": [AVISO_PARA],
            "subject": "Lista de espera: %s entrou (%d no total)" % (quem, total),
            "text": "\n".join(linhas),
        }).encode("utf-8")

        pedido = urllib.request.Request(
            "https://api.resend.com/emails", data=corpo,
            headers={
                "Authorization": "Bearer " + RESEND_KEY,
                "Content-Type": "application/json",
                # sem um User-Agent de verdade o Cloudflare do Resend devolve 403
                "User-Agent": "Regis/1.0 (+https://regis.ia.br)",
                "Accept": "application/json",
            })
        try:
            with urllib.request.urlopen(pedido, timeout=20) as resposta:
                dados = json.loads(resposta.read().decode("utf-8"))
            print("[lista] avisei %s por e-mail (id %s)" % (AVISO_PARA, dados.get("id")))
        except Exception as erro:
            print("[lista] não consegui avisar por e-mail: %s" % erro)

    threading.Thread(target=enviar, daemon=True).start()


def moeda(valor):
    if valor is None:
        return None
    texto = "%.2f" % float(valor)
    inteiro, centavos = texto.split(".")
    negativo = inteiro.startswith("-")
    inteiro = inteiro.lstrip("-")
    partes = []
    while len(inteiro) > 3:
        partes.insert(0, inteiro[-3:])
        inteiro = inteiro[:-3]
    partes.insert(0, inteiro)
    return ("-" if negativo else "") + ".".join(partes) + "," + centavos


MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
         "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]


def mes_extenso(iso):
    try:
        return MESES[int(str(iso).split("-")[1]) - 1]
    except Exception:
        return None


def montar_estado():
    """Motor + memória. É isso que o app desenha."""
    from motor.detectar import detectar

    resultado = detectar(os.path.join(RAIZ, "dados"))
    memoria = ler_memoria()
    resumo = resultado["resumo"]

    achados, respondidos = [], []
    for achado in resultado.get("achados", []):
        item = {
            "id": achado.get("id"),
            "certeza": achado.get("certeza"),
            "titulo": achado.get("titulo"),
            "explicacao": achado.get("explicacao"),
            "valor_txt": moeda(achado.get("valor")),
            "tem_acao": bool(achado.get("acao")),
            "acao_titulo": (achado.get("acao") or {}).get("titulo"),
            "contraparte": achado.get("contraparte"),
        }
        resposta = resposta_do_chat(achado, memoria)

        # "Foi eu" e "Não fui eu" são respostas opostas e não podem terminar no
        # mesmo lugar. Quem confirma resolve a suspeita, ela some. Quem nega
        # está dizendo que a cobrança é indevida, e isso é o caso mais grave
        # que existe: vira fato, com contestação, no topo da lista.
        if resposta == "foi_eu" and achado.get("certeza") == "suspeita":
            item["resolvido_no_chat"] = True
            respondidos.append(item)
        elif resposta == "nao_fui_eu":
            item["certeza"] = "fato"
            item["confirmado_no_chat"] = True
            item["explicacao"] = ("Você me disse no chat que não reconhece isso. "
                                  "Então não é mais suspeita, é cobrança indevida. "
                                  + (item["explicacao"] or ""))
            achados.insert(0, item)
        else:
            achados.append(item)

    faturado = float(resumo.get("faturamento_acumulado") or 0)
    teto = float(resumo.get("teto") or 81000)

    silenciados = [{"titulo": s.get("titulo"), "explicacao": s.get("explicacao")}
                   for s in resultado.get("silenciados", [])]
    for item in respondidos:
        silenciados.insert(0, {
            "titulo": item["titulo"],
            "explicacao": "Você já respondeu no chat, então eu não pergunto mais.",
            "veio_do_chat": True,
        })

    contagem = {"fatos": 0, "regras": 0, "suspeitas": 0, "silenciados": len(silenciados)}
    for a in achados:
        if a["certeza"] == "fato":
            contagem["fatos"] += 1
        elif a["certeza"] == "regra":
            contagem["regras"] += 1
        elif a["certeza"] == "suspeita":
            contagem["suspeitas"] += 1

    return {
        "atualizado_em": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "perfil": {"nome": "Angela Nogueira", "primeiro_nome": "Angela",
                   "negocio": "cabeleireira MEI no Studio Bella"},
        "resumo": {
            "faturado": faturado, "faturado_txt": moeda(faturado),
            "teto": teto, "teto_txt": moeda(teto),
            "percentual": round(faturado / teto * 100, 1) if teto else 0,
            "falta_txt": moeda(resumo.get("falta_para_o_teto")),
            "estouro_mes": mes_extenso(resumo.get("projecao_estouro")),
            "recuperavel_txt": moeda(resumo.get("total_recuperavel")),
            "transacoes_conferidas": resumo.get("qtd_transacoes_conferidas"),
        },
        "achados": achados,
        "silenciados": silenciados,
        "contagem": contagem,
        "aprendido_no_chat": {
            "conhecidas": memoria["conhecidas"],
            "quantas": len(memoria["conhecidas"]) + len(memoria["negadas"]),
        },
    }


def estado_com_cache():
    """Recalcula quando a memória muda, ou a cada 2 segundos."""
    with _trava:
        memoria = ler_memoria()
        assinatura = (memoria["mtime"], len(memoria["conhecidas"]), len(memoria["negadas"]))
        velho = (time.time() - _cache["quando"]) > 2
        if _cache["dado"] is None or assinatura != _cache["assinatura"] or velho:
            _cache["dado"] = montar_estado()
            _cache["quando"] = time.time()
            _cache["assinatura"] = assinatura
        return _cache["dado"]


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=UI, **kwargs)

    def translate_path(self, path):
        # a identidade visual mora fora de ui/, então atendo /idv/ à parte
        limpo = path.split("?")[0].split("#")[0]
        if limpo.startswith("/idv/") or limpo.startswith("../idv/"):
            nome = limpo.split("/idv/", 1)[1]
            return os.path.join(RAIZ, "idv", urllib.parse.unquote(nome))
        # o deck do pitch mora em pitch/, fora de ui/, e atende em /pitch
        if limpo.startswith("/pitch/") or limpo.startswith("../pitch/"):
            nome = limpo.split("/pitch/", 1)[1]
            nome = os.path.basename(urllib.parse.unquote(nome))
            return os.path.join(RAIZ, "pitch", nome)
        return super().translate_path(path)

    def entrou(self):
        if not LOGIN_LIGADO:
            return True
        bruto = self.headers.get("Cookie") or ""
        for parte in bruto.split(";"):
            nome, _, valor = parte.strip().partition("=")
            if nome == "regis" and conferir(valor):
                return True
        return False

    def responder_json(self, codigo, dado, cookie=None):
        corpo = json.dumps(dado, ensure_ascii=False).encode("utf-8")
        self.send_response(codigo)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def do_POST(self):
        caminho = self.path.split("?")[0]

        if caminho == "/api/lista":
            try:
                tamanho = int(self.headers.get("Content-Length") or 0)
                if tamanho > 4000:
                    return self.responder_json(400, {"ok": False})
                corpo = json.loads(self.rfile.read(tamanho).decode("utf-8") or "{}")
            except Exception:
                return self.responder_json(400, {"ok": False, "erro": "não entendi o envio"})

            email = str(corpo.get("email", "")).strip().lower()[:160]
            if "@" not in email or "." not in email.split("@")[-1] or len(email) < 6:
                return self.responder_json(400, {"ok": False, "erro": "confere o e-mail"})

            registro = {
                "email": email,
                "nome": str(corpo.get("nome", "")).strip()[:80],
                "perfil": str(corpo.get("perfil", "")).strip()[:40],
                "canais": str(corpo.get("canais", "")).strip()[:120],
                "quando": time.strftime("%Y-%m-%dT%H:%M:%S"),
            }
            try:
                try:
                    with open(LISTA, "r", encoding="utf-8") as arquivo:
                        lista = json.load(arquivo)
                    if not isinstance(lista, list):
                        lista = []
                except Exception:
                    lista = []
                # sem duplicar quem já entrou
                lista = [x for x in lista if x.get("email") != email]
                lista.append(registro)
                os.makedirs(os.path.dirname(LISTA), exist_ok=True)
                with open(LISTA, "w", encoding="utf-8") as arquivo:
                    json.dump(lista, arquivo, ensure_ascii=False, indent=2)
                print("[lista] %s entrou. Total: %d" % (email, len(lista)))
                avisar_por_email(registro, len(lista))
                return self.responder_json(200, {"ok": True, "total": len(lista)})
            except Exception as erro:
                print("[lista] não consegui gravar: %s" % erro)
                return self.responder_json(500, {"ok": False, "erro": "tenta de novo"})

        if caminho != "/api/entrar":
            return self.send_error(404)
        try:
            tamanho = int(self.headers.get("Content-Length") or 0)
            corpo = json.loads(self.rfile.read(tamanho).decode("utf-8") or "{}")
        except Exception:
            corpo = {}
        usuario = str(corpo.get("usuario", "")).strip().lower()
        senha = str(corpo.get("senha", ""))
        ok = hmac.compare_digest(usuario, USUARIO.lower()) and hmac.compare_digest(senha, SENHA)
        resposta = json.dumps({"ok": ok}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        if ok:
            self.send_header("Set-Cookie",
                             "regis=%s; Path=/; Max-Age=86400; SameSite=Lax" % assinar(usuario))
        self.send_header("Content-Length", str(len(resposta)))
        self.end_headers()
        self.wfile.write(resposta)

    def do_GET(self):
        caminho = self.path.split("?")[0]

        # quem tiver o link antigo salvo vai para o app novo, sem erro na cara
        if caminho in ("/regis-app-desktop.html", "/regis-app-mobile.html"):
            self.send_response(301)
            self.send_header("Location", "/regis-app.html")
            self.end_headers()
            return

        # endereço curto da lista de espera: /espera, sem .html
        if caminho in ("/espera", "/espera/"):
            self.path = "/espera.html"
            caminho = "/espera.html"

        # endereço curto da página do QR do pitch: /jurados, sem .html
        if caminho in ("/jurados", "/jurados/"):
            self.path = "/jurados.html"
            caminho = "/jurados.html"

        # endereço curto do deck: /pitch abre a apresentação de 5 minutos
        if caminho in ("/pitch", "/pitch/"):
            self.path = "/pitch/regis-pitch.html"
            caminho = "/pitch/regis-pitch.html"

        # abrir regis.ia.br leva ao app, não a um índice de protótipos
        if caminho in ("/", "/index.html"):
            self.send_response(302)
            self.send_header("Location", "/regis-app.html")
            self.end_headers()
            return
        if LOGIN_LIGADO and not self.entrou() and caminho not in LIVRE \
                and not caminho.startswith("/idv/"):
            if caminho.startswith("/api/"):
                corpo = json.dumps({"erro": "entre primeiro"}).encode()
                self.send_response(401)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Content-Length", str(len(corpo)))
                self.end_headers()
                self.wfile.write(corpo)
                return
            self.send_response(302)
            self.send_header("Location", "/login.html")
            self.end_headers()
            return
        if caminho in ("/api/estado", "/api/estado/"):
            try:
                corpo = json.dumps(estado_com_cache(), ensure_ascii=False).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.send_header("Cache-Control", "no-store")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.send_header("Content-Length", str(len(corpo)))
                self.end_headers()
                self.wfile.write(corpo)
            except Exception as erro:
                self.send_error(500, "erro montando o estado: %s" % erro)
            return
        return super().do_GET()

    def end_headers(self):
        # o app muda a toda hora durante o hackathon, então nada de cache
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

    def log_message(self, formato, *args):
        # O filtro do polling olha args[0] esperando a linha do pedido, que é o
        # que o log_request manda. Mas o log_error manda o código como
        # HTTPStatus, que não é texto: sem o str() o "in" estoura TypeError
        # dentro do send_error, e aí a resposta de erro morre no meio e o
        # navegador recebe conexão vazia em vez de um 404 honesto.
        primeiro = str(args[0]) if args else ""
        if "/api/estado" not in primeiro:
            sys.stderr.write("[web] %s\n" % (formato % args))


class Servidor(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    print("[web] servindo %s" % UI)
    print("[web] login: %s (usuário %s)" % ("ligado" if LOGIN_LIGADO else "desligado", USUARIO))
    print("[web] memória em %s" % MEMORIA)
    try:
        estado = estado_com_cache()
        print("[web] motor ok: R$ %s faturados, %d achados"
              % (estado["resumo"]["faturado_txt"], len(estado["achados"])))
    except Exception as erro:
        print("[web] atenção, o motor falhou: %s" % erro)
    print("[web] no ar em http://0.0.0.0:%d" % PORTA)
    with Servidor(("0.0.0.0", PORTA), Handler) as servidor:
        servidor.serve_forever()


if __name__ == "__main__":
    sys.exit(main() or 0)
