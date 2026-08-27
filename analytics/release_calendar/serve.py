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
from datetime import date, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

_RAIZ = Path(__file__).resolve().parents[2]
_HTML = _RAIZ / "reports" / "release_calendar.html"

_HOSTS_OK = {"127.0.0.1", "localhost", "[::1]"}


def _garantir_html() -> Path:
    """Gera o relatorio se ainda nao existir (ou se o template estiver mais novo).

    Passa pelo `status.gerar()` e nao pelo `run()` direto para o stamp sair junto —
    sem isso a propria linha do calendario na aba "Status dashboard" viveria em "sem
    stamp". Aqui e barato: as dependencias deste relatorio sao dois YAML, sem MySQL.
    """
    template = Path(__file__).parent / "report.html"
    if _HTML.exists() and template.stat().st_mtime <= _HTML.stat().st_mtime:
        return _HTML

    try:
        from domain.dashboards.status import gerar

        gerar("release_calendar")
    except Exception:
        from analytics.release_calendar.generate_report import run

        run()
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
            agora = datetime.now()
            self._json(200, {"ok": True, "modo": "servido",
                             "hoje": agora.date().isoformat(),
                             "agora": agora.strftime("%H:%M")})
            return

        if rota == "/api/dashboards":
            # Mesmo shape que generate_report.py embute, so recalculado agora -- e o
            # que deixa a aba usar UM renderizador para os dois modos. `live=1`
            # acrescenta as fontes externas (FRED), que custam uma chamada de rede
            # cada e por isso ficam fora do default.
            live = "live=1" in (self.path.split("?", 1)[1] if "?" in self.path else "")
            try:
                from domain.dashboards.status import estado
                agora = datetime.now()
                self._json(200, {"ok": True, "agora": agora.strftime("%H:%M"),
                                 "dashboards": estado(live=live)})
            except Exception as exc:
                # Mesmo tratamento do /api/status: banco fora do ar degrada a aba
                # para o retrato embutido, nao derruba a pagina.
                self._json(200, {"ok": False,
                                 "erro": f"{type(exc).__name__}: {exc}"})
            return

        if rota == "/api/status":
            try:
                from domain.release_calendar.sync import status_por_grupo
                agora = datetime.now()
                self._json(200, {"ok": True, "hoje": agora.date().isoformat(),
                                 "agora": agora.strftime("%H:%M"),
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
        rota = self.path.split("?", 1)[0]
        if rota not in ("/api/run", "/api/gerar"):
            self._json(404, {"erro": "rota desconhecida"})
            return

        try:
            n = int(self.headers.get("Content-Length") or 0)
            corpo = json.loads(self.rfile.read(n) or b"{}")
        except (ValueError, json.JSONDecodeError):
            self._json(400, {"erro": "corpo nao e JSON valido"})
            return

        if rota == "/api/gerar":
            self._gerar_dashboard(corpo)
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

    # ---------------------------------------------------------- regerar dashboard

    def _gerar_dashboard(self, corpo: dict) -> None:
        """POST /api/gerar — regera UM dashboard e devolve o estado novo dele.

        Um de cada vez, por decisao explicita do usuario: quem acabou de atualizar o
        IPCA escolhe qual dos seis dashboards que o consomem interessa agora. Nao
        existe "regerar todos os atrasados" aqui nem na pagina.

        Mesma guarda do /api/run, so que por `key`: a pagina manda um id do manifesto
        e quem resolve id -> modulo e o nosso lado. Nunca chega caminho nem nome de
        modulo pela rede, e nao ha shell em ponto nenhum.
        """
        key = corpo.get("key")
        if not isinstance(key, str) or not key:
            self._json(400, {"erro": "informe 'key'"})
            return

        from domain.dashboards.status import estado, gerar, por_chave

        manifesto = por_chave()
        if key not in manifesto:
            self._json(400, {"erro": f"dashboard desconhecido: {key}"})
            return
        if not manifesto[key].get("module"):
            self._json(400, {"erro": f"{key} nao tem entry point automatico; "
                                     f"rode a mao: {manifesto[key].get('command')}"})
            return

        try:
            resultado = gerar(key)
        except Exception as exc:
            self._json(500, {"erro": f"{type(exc).__name__}: {exc}"})
            return

        # O estado novo SO deste dashboard: o card volta com o veredito atualizado sem
        # pagar a consulta dos outros dez.
        try:
            resultado["dashboard"] = estado(chaves=[key])[0]
        except Exception as exc:
            resultado["dashboard"] = None
            resultado["estado_erro"] = str(exc)

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
