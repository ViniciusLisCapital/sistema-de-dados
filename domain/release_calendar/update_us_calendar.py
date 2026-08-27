"""
Refresca as datas e horas dos grupos AMERICANOS do calendario a partir das fontes.

Contrapartida de `update_calendar.py` (que cobre o BCB) para BLS e BEA. A divisao e
a mesma do resto do projeto: `connectors/us_agenda.py` fala HTTP e faz o parse,
este modulo orquestra — le o YAML, confronta com a fonte, reporta o drift e grava.

    uv run python -m domain.release_calendar.update_us_calendar            # dry-run
    uv run python -m domain.release_calendar.update_us_calendar --write    # aplica
    uv run python -m domain.release_calendar.update_us_calendar --catalogo # o que da para adicionar
    uv run python -m domain.release_calendar.update_us_calendar --sem-fred # pula a conferencia

--------------------------------------------------------------------------------
COMO SE ADICIONA UMA SERIE NOVA
--------------------------------------------------------------------------------
O vinculo serie -> agenda e DECLARATIVO, no proprio YAML, do mesmo jeito que o bloco
`ics:` dos grupos do BCB. Um grupo americano se declara assim:

    - group: bls_ppi
      institution: "BLS"
      name: "Producer Price Index"
      tables: [inflc_ppi]
      cadence: monthly
      release_time_tz: America/New_York
      us:
        source: bls_schedule        # bls_schedule | bls_ics | bea_ics
        match: ppi                  # slug da pagina do BLS (ou titulo do release, no BEA)
        fred_release_id: 46         # opcional: conferencia independente
      entries: []

...e o `--write` preenche `entries`. Nada mais precisa ser escrito em codigo: os tres
`source` cobrem as duas agencias, e `--catalogo` lista o que existe de cada lado
(13 releases com pagina no BLS, 34 titulos no feed do BEA) junto com o id do FRED.

`bls_schedule` e o default para o BLS porque e a unica fonte com periodo de
referencia. Use `bls_ics` so para um release sem pagina propria — ai o periodo tem
que ser escrito a mao, e o script avisa entrada por entrada.
"""

from __future__ import annotations

import argparse
import io
import re
import sys
from datetime import date
from pathlib import Path

from connectors.us_agenda import BEAAgenda, BLSAgenda, FREDReleases, USAgendaError

# Reuso deliberado dos helpers de escrita do irmao BCB: sao genericos sobre dicts de
# entrada, e duplicar a manipulacao de ruamel (que custou tres tentativas para
# preservar a linha em branco entre grupos) so criaria duas formatacoes divergentes
# no mesmo arquivo.
from domain.release_calendar.update_calendar import (
    _diff,
    _em_escopo,
    _gravar_entries,
    _merge,
    _yaml,
)

_AQUI = Path(__file__).parent
_YAML_DEFAULT = _AQUI / "calendar_2026.yaml"

_FONTES = ("bls_schedule", "bls_ics", "bea_ics")


# ------------------------------------------------------------------- entradas


def _entradas_da_fonte(
    cfg: dict,
    cutoff: date,
    until: date,
    bls: BLSAgenda,
    bea: BEAAgenda,
) -> list[dict]:
    """Entradas que a fonte declarada implica, no formato do YAML."""
    fonte = str(cfg.get("source") or "")
    match = str(cfg.get("match") or "")
    if fonte not in _FONTES:
        raise USAgendaError(
            f"source invalido: {fonte!r} (esperado um de {', '.join(_FONTES)})"
        )
    if not match:
        raise USAgendaError(f"bloco us: sem `match` (source={fonte})")

    if fonte == "bls_schedule":
        eventos = [
            e for e in bls.schedule(match) if cutoff <= e["date"] <= until
        ]
    elif fonte == "bls_ics":
        eventos = bls.eventos(start=cutoff, end=until, summary_contains=match)
    else:
        eventos = bea.eventos(start=cutoff, end=until, summary_starts=match)

    out = []
    for e in eventos:
        item: dict = {"date": e["date"].isoformat()}
        if e.get("time"):
            item["time"] = e["time"]
        if e.get("reference_period"):
            item["reference_period"] = e["reference_period"]
        item["confirmed"] = True
        out.append(item)
    return out


def _conferir_fred(
    cfg: dict, novas: list[dict], fred: FREDReleases | None
) -> list[str]:
    """Confronta as datas com o FRED. Devolve as divergencias, uma linha cada.

    Nao e redundancia decorativa: o FRED e a unica fonte independente das agencias,
    e uma divergencia aqui e o sinal de que uma das duas mudou de forma (o parse do
    HTML e o candidato mais fragil).

    A conferencia e ASSIMETRICA de proposito, e so um dos lados e problema:

    * data nossa que o FRED nao tem -> **suspeita**. Ou o parser leu errado, ou a
      agencia mudou a agenda e o FRED ainda nao refletiu.
    * data do FRED que nao e nossa -> **esperado**. Um "release" do FRED e o
      conjunto de publicacoes que atualizam aquelas series, nao um evento com um
      titulo. O release 54 inclui as divulgacoes trimestrais de PIB, que republicam
      o indice de preco do PCE sem se chamarem "Personal Income and Outlays" --
      medido em 2026-08-26: o FRED tem 2025-12-23 (GDP 3T25) e a agenda do BEA,
      filtrada por titulo, nao. Sai como nota, nao como alerta.
    """
    rid = cfg.get("fred_release_id")
    if not rid or fred is None or not novas:
        return []
    try:
        do_fred = set(fred.dates(int(rid)))
    except Exception as exc:  # chave ausente, rede fora: avisa e segue
        return [f"conferencia FRED indisponivel: {exc}"]

    minha = {date.fromisoformat(str(n["date"])) for n in novas}
    janela = {d for d in do_fred if min(minha) <= d <= max(minha)}
    avisos = []
    for d in sorted(minha - janela):
        avisos.append(f"SUSPEITO: {d} esta na agenda da agencia e nao no release "
                      f"{rid} do FRED")
    extras = sorted(janela - minha)
    if extras:
        avisos.append(f"nota: o release {rid} do FRED tem mais {len(extras)} data(s) "
                      f"na janela ({', '.join(str(d) for d in extras[:4])}"
                      f"{'...' if len(extras) > 4 else ''}) — outras publicacoes que "
                      f"mexem nas mesmas series")
    return avisos


# -------------------------------------------------------------------- refresh


def refresh(
    path: Path | str = _YAML_DEFAULT,
    cutoff: date | None = None,
    until: date | None = None,
    write: bool = False,
    fred: bool = True,
) -> int:
    """Le o YAML, busca as agendas do BLS/BEA, reporta o drift e opcionalmente grava.

    Returns:
        int: numero de grupos com alguma mudanca.
    """
    path = Path(path)
    cutoff = cutoff or date.today()
    if until is None:
        m = re.search(r"(20\d{2})", path.name)
        ano = int(m.group(1)) if m else cutoff.year
        until = date(ano, 12, 31)

    y = _yaml()
    doc = y.load(path.read_text(encoding="utf-8"))

    grupos = [g for g in doc["groups"] if "us" in g]
    if not grupos:
        print("nenhum grupo com bloco `us:` no calendario — nada a fazer")
        return 0

    bls, bea = BLSAgenda(), BEAAgenda()
    conferente = FREDReleases() if fred else None

    print(f"calendario : {path.name}")
    print(f"janela     : {cutoff} -> {until}")
    print(f"modo       : {'ESCRITA' if write else 'dry-run (nada sera gravado)'}\n")

    mudados = 0
    for group in grupos:
        slug = group["group"]
        cfg = group["us"]
        antigas = group.get("entries") or []
        try:
            novas = _entradas_da_fonte(cfg, cutoff, until, bls, bea)
        except Exception as exc:
            print(f"! {slug}  FALHOU: {exc}")
            continue

        d = _diff([e for e in antigas if _em_escopo(e, cutoff, until)], novas)
        tem_mudanca = bool(d["shifts"] or d["add"] or d["rem"] or d["horas"])
        mudados += int(tem_mudanca)

        marca = "*" if tem_mudanca else " "
        print(f"{marca} {slug}  [{cfg['source']}: {cfg['match']}]")
        for a, n in d["shifts"]:
            print(f"      ~ {a['date']} -> {n['date']}   "
                  f"{n.get('reference_period', '')}   REVISAO DE DATA")
        for n in d["add"]:
            print(f"      + {n['date']}   {n.get('reference_period', '')}   nova")
        for a in d["rem"]:
            print(f"      - {a['date']}   {a.get('reference_period', '')}   saiu da agenda")
        for a, n in d["horas"]:
            print(f"      h {n['date']}   {a.get('time') or 'sem hora'} -> {n['time']}   HORA")
        if not tem_mudanca:
            print(f"      = {len(d['iguais'])} entradas, sem mudanca")

        for aviso in _conferir_fred(cfg, novas, conferente):
            print(f"      ! {aviso}")

        itens, avisos = _merge(antigas, novas, cutoff, until)
        for aviso in avisos:
            print(f"      ! {aviso}")
        if write:
            _gravar_entries(group, itens)

    if write:
        buf = io.StringIO()
        y.dump(doc, buf)
        path.write_text(buf.getvalue(), encoding="utf-8", newline="\n")
        print(f"\ngravado: {path}")
    elif mudados:
        print(f"\n{mudados} grupo(s) com drift — rode com --write para aplicar")
    else:
        print("\nnenhuma mudanca; os grupos americanos estao em dia")

    return mudados


# ------------------------------------------------------------------- catalogo


def catalogo(fred: bool = True) -> None:
    """Lista o que existe de agenda dos dois lados — o passo antes de adicionar serie.

    Imprime os releases do BLS que tem pagina de agenda propria (com hora e periodo
    de referencia) e os titulos de release do feed do BEA, que sao os valores validos
    de `match` no bloco `us:`.
    """
    bls, bea = BLSAgenda(), BEAAgenda()

    print("BLS — releases com pagina de agenda (source: bls_schedule)\n")
    for slug in bls.releases():
        try:
            linhas = bls.schedule(slug)
        except Exception as exc:
            print(f"  {slug:9s}  (falhou: {exc})")
            continue
        proximas = [e for e in linhas if e["date"] >= date.today()]
        hora = {e["time"] for e in linhas}
        prox = proximas[0] if proximas else None
        print(
            f"  {slug:9s}  {len(linhas):2d} linhas  hora {'/'.join(sorted(hora))}  "
            f"proxima {prox['date'] if prox else '—'} "
            f"(ref {prox['reference_period'] if prox else '—'})"
        )

    print("\nBEA — titulos de release no feed ICS (source: bea_ics)\n")
    eventos = bea.eventos()
    por_titulo: dict[str, list[dict]] = {}
    for e in eventos:
        por_titulo.setdefault(e["summary"].split(",")[0].strip(), []).append(e)
    for titulo in sorted(por_titulo):
        itens = por_titulo[titulo]
        futuras = [e for e in itens if e["date"] >= date.today()]
        prox = futuras[0] if futuras else None
        print(
            f"  {len(itens):3d}x  {titulo[:58]:58s}  proxima "
            f"{prox['date'] if prox else '—'} "
            f"(ref {prox['reference_period'] if prox else '—'})"
        )

    if fred:
        print("\nFRED — id de release por serie (para `fred_release_id`)\n")
        f = FREDReleases()
        for sid in ("CPIAUCSL", "PCEPI", "PPIACO", "PAYEMS", "JTSJOL", "ECIALLCIV"):
            try:
                rs = f.release_for_series(sid)
            except Exception as exc:
                print(f"  {sid:12s} (falhou: {exc})")
                continue
            for r in rs:
                print(f"  {sid:12s} -> {r['id']:<4} {r['name']}")


# ----------------------------------------------------------------------- CLI


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    p.add_argument("--yaml", default=str(_YAML_DEFAULT), help="caminho do calendario")
    p.add_argument("--write", action="store_true", help="grava as mudancas no YAML")
    p.add_argument("--from", dest="cutoff", metavar="YYYY-MM-DD",
                   help="inicio da janela (default: hoje)")
    p.add_argument("--until", metavar="YYYY-MM-DD",
                   help="fim da janela (default: 31/dez do ano do arquivo)")
    p.add_argument("--catalogo", action="store_true",
                   help="lista as agendas disponiveis nas duas agencias e sai")
    p.add_argument("--sem-fred", dest="fred", action="store_false",
                   help="pula a conferencia independente pelo FRED")
    args = p.parse_args(argv)

    if args.catalogo:
        catalogo(fred=args.fred)
        return 0

    refresh(
        path=args.yaml,
        cutoff=date.fromisoformat(args.cutoff) if args.cutoff else None,
        until=date.fromisoformat(args.until) if args.until else None,
        write=args.write,
        fred=args.fred,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
