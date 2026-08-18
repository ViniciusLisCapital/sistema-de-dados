"""
Servidor local que deixa o botao "Atualizar" do calendario de divulgacoes funcionar.

O relatorio e um HTML autocontido — nao existe jeito de um arquivo estatico executar
Python. Entao o botao tem dois modos, e este script e o que habilita o primeiro:

  servido  — abra por aqui e o botao roda o ETL de verdade (fetch para /api/run)
  arquivo  — aberto como file:// ou recebido por email, o ping falha e o mesmo botao
             passa a copiar o comando para o clipboard. Relatorio compartilhado nao
             fica com controle morto, e ninguem consegue rodar nada na sua maquina.

Uso:
    uv run python analytics/release_calendar/serve.py
    uv run python analytics/release_calendar/serve.py --port 9000 --no-browser

Ctrl+C para parar.

Seguranca — o que existe e por que:
  * escuta so em 127.0.0.1 (nao 0.0.0.0), entao nada na rede alcanca
  * o POST aceita um SLUG DE GRUPO e resolve os scripts pelo YAML — nunca recebe nome
    de modulo, caminho ou comando da pagina. Slug fora da lista = 400. Nao ha shell
    envolvido em nenhum ponto
  * confere o header Host: sem isso, um site qualquer aberto no mesmo browser poderia
    apontar um dominio para 127.0.0.1 e disparar POSTs (DNS rebinding)
"""

from __future__ import annotations

import argparse
import json
import sys
import threading
import webbrowser
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

_RAIZ = Path(__file__).resolve().parents[2]
_HTML = _RAIZ / "reports" / "release_calendar.html"

_HOSTS_OK = {"127.0.0.1", "localhost", "[::1]"}


def _garantir_html() -> Path:
    """Gera o relatorio se ainda nao existir (ou se o template estiver mais novo)."""
    from analytics.release_calendar.generate_report import run as gerar

    template = Path(__file__).parent / "report.html"
    if not _HTML.exists() or template.stat().st_mtime > _HTML.stat().st_mtime:
        gerar()
    return _HTML


class Handler(BaseHTTPRequestHandler):
    server_version = "LISReleaseCalendar/1.0"

    # ---------------------------------------------------------------- helpers

    def _host_ok(self) -> bool:
        host = (self.headers.get("Host") or "").rsplit(":", 1)[0]
        return host in _HOSTS_OK

    def _json(self, code: int, payload: dict) -> None:
        corpo = json.dumps(payload, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(corpo)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(corpo)

    def log_message(self, fmt, *args):  # menos ruido que o default
        sys.stderr.write("  %s\n" % (fmt % args))

    # -------------------------------------------------------------------- GET

    def do_GET(self):  # noqa: N802
        if not self._host_ok():
            self._json(403, {"erro": "host nao permitido"})
            return

        rota = self.path.split("?", 1)[0]

        if rota in ("/", "/index.html"):
            try:
                corpo = _garantir_html().read_bytes()
            except Exception as exc:
                self._json(500, {"erro": f"nao deu para gerar o relatorio: {exc}"})
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(corpo)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(corpo)
            return

        if rota == "/api/ping":
            self._json(200, {"ok": True, "modo": "servido",
                             "hoje": date.today().isoformat()})
            return

        if rota == "/api/status":
            try:
                from domain.release_calendar.sync import status_por_grupo
                self._json(200, {"ok": True, "hoje": date.today().isoformat(),
                                 "grupos": status_por_grupo()})
            except Exception as exc:
                # banco fora do ar nao deve derrubar a pagina: ela cai no modo sem
                # veredito (botao neutro em toda linha passada) em vez de quebrar
                self._json(200, {"ok": False,
                                 "erro": f"{type(exc).__name__}: {exc}"})
            return

        self._json(404, {"erro": "rota desconhecida"})

    # ------------------------------------------------------------------- POST

    def do_POST(self):  # noqa: N802
        if not self._host_ok():
            self._json(403, {"erro": "host nao permitido"})
            return
        if self.path.split("?", 1)[0] != "/api/run":
            self._json(404, {"erro": "rota desconhecida"})
            return

        try:
            n = int(self.headers.get("Content-Length") or 0)
            corpo = json.loads(self.rfile.read(n) or b"{}")
        except (ValueError, json.JSONDecodeError):
            self._json(400, {"erro": "corpo nao e JSON valido"})
            return

        slug = corpo.get("group")
        if not isinstance(slug, str) or not slug:
            self._json(400, {"erro": "informe 'group'"})
            return

        # allowlist: o slug tem que existir no YAML. Nunca recebemos nome de modulo
        # nem caminho — o mapeamento grupo -> tabelas -> script e todo do nosso lado.
        from domain.release_calendar.sync import carregar, tabelas_por_grupo
        grupos = tabelas_por_grupo(carregar())
        if slug not in grupos:
            self._json(400, {"erro": f"grupo desconhecido: {slug}"})
            return
        if not grupos[slug]:
            self._json(400, {"erro": f"grupo {slug} nao alimenta nenhuma tabela"})
            return

        from jobs.update_db import executar_grupo
        try:
            resultado = executar_grupo(slug)
        except Exception as exc:
            self._json(500, {"erro": f"{type(exc).__name__}: {exc}"})
            return

        # devolve tambem o estado novo do grupo, para o botao virar check sem F5
        try:
            from domain.release_calendar.sync import status_por_grupo
            resultado["status"] = status_por_grupo().get(slug)
        except Exception as exc:
            resultado["status"] = None
            resultado["status_erro"] = str(exc)

        resultado["ok"] = resultado["n_erro"] == 0 and not resultado["sem_script"]
        self._json(200, resultado)


class Server(ThreadingHTTPServer):
    """ThreadingHTTPServer que nao cospe traceback quando a conexao morre.

    Ao dar Ctrl+C (ou fechar a aba durante um run longo) o socket fecha embaixo da
    thread que estava lendo, e o handler default imprime um traceback de
    ConnectionAborted/Reset que parece erro e nao e. O resto dos erros continua
    aparecendo normalmente.
    """

    daemon_threads = True

    def handle_error(self, request, client_address):
        exc = sys.exc_info()[1]
        if isinstance(exc, (ConnectionAbortedError, ConnectionResetError, BrokenPipeError)):
            return
        super().handle_error(request, client_address)


def run(port: int = 8765, abrir: bool = True) -> None:
    _garantir_html()
    srv = Server(("127.0.0.1", port), Handler)
    url = f"http://127.0.0.1:{port}/"
    print(f"Calendario de divulgacoes servido em {url}")
    print("  o botao 'Atualizar' de cada divulgacao roda o ETL daquele grupo")
    print("  Ctrl+C para parar\n")
    if abrir:
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nencerrado")
    finally:
        srv.server_close()


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--no-browser", action="store_true",
                   help="nao abre o browser automaticamente")
    args = p.parse_args(argv)
    run(port=args.port, abrir=not args.no_browser)


if __name__ == "__main__":
    main()
