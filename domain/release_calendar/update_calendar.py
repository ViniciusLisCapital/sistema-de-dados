"""
Atualiza as datas de divulgacao do BCB em `calendar_2026.yaml` a partir dos feeds ICS.

Cobre so os grupos que tem bloco `ics:` no YAML (os 10 do BCB). Os outros — IBGE,
Tesouro, MTE, MDIC, CFTC, FOMC — nao tem feed equivalente e seguem manuais; o
relatorio lista quais foram pulados para isso ficar explicito.

Uso:

    # relatorio de drift, sem escrever nada (default)
    uv run python -m domain.release_calendar.update_calendar

    # aplica as mudancas no YAML (preserva comentarios e notas escritas a mao)
    uv run python -m domain.release_calendar.update_calendar --write

    # quais tabelas do banco nao tem grupo de calendario
    uv run python -m domain.release_calendar.update_calendar --coverage

    # enumera as 29 listas de calendario publicadas pelo BCB
    uv run python -m domain.release_calendar.update_calendar --listas

Por que dry-run e o default: o YAML e curado a mao (notas longas por grupo, avisos
de confiabilidade) e e a fonte de verdade de metadados. O script troca so as datas;
qualquer surpresa no diff merece olho humano antes de virar commit.

Notas de implementacao:
- Escrita via ruamel.yaml em round-trip. Verificado que um load+dump sem alteracao
  devolve o arquivo byte-identico (precisa de `indent(mapping=2, sequence=4, offset=2)`
  para casar o estilo do arquivo) — sem isso, PyYAML apagaria todos os comentarios.
- `reference_period` e derivado da regra `ics.ref` de cada grupo (mes ou trimestre,
  com lag), porque o feed traz so titulo e data. Grupo sem `ics.ref` (Copom, Focus)
  fica sem periodo, e datas novas sem correspondencia sao sinalizadas no relatorio
  como pendentes de preenchimento manual (o numero da reuniao do Copom, por exemplo,
  nao e derivavel do feed).
- Entradas com data anterior ao corte sao preservadas como estao, nunca apagadas.
"""

from __future__ import annotations

import argparse
import io
import os
import re
import sys
from datetime import date, timedelta
from pathlib import Path

from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedMap, CommentedSeq
from ruamel.yaml.scalarstring import DoubleQuotedScalarString

from connectors.bcb_agenda import BCBAgenda

_AQUI = Path(__file__).parent
_YAML_DEFAULT = _AQUI / "calendar_2026.yaml"

# Schemas varridos por --coverage.
_SCHEMAS = ("macro_brasil", "macro_international")


# --------------------------------------------------------------------- helpers


def _yaml() -> YAML:
    y = YAML()
    y.preserve_quotes = True
    y.width = 4096
    y.indent(mapping=2, sequence=4, offset=2)
    return y


def _add_months(d: date, n: int) -> date:
    """Soma (ou subtrai) meses mantendo o dia 1 — usado so para periodo de referencia."""
    total = (d.year * 12 + d.month - 1) + n
    return date(total // 12, total % 12 + 1, 1)


def _ref_period(d: date, unit: str, lag: int) -> str:
    """Periodo coberto por uma divulgacao publicada em `d`.

    unit="month", lag=1  -> divulgacao de agosto cobre "2026-07"
    unit="quarter", lag=1 -> divulgacao de agosto cobre "2026-Q2"
    unit="quarter", lag=0 -> divulgacao de setembro cobre "2026-Q3" (RPM)
    """
    if unit == "month":
        m = _add_months(d, -lag)
        return f"{m.year}-{m.month:02d}"
    if unit == "quarter":
        q_abs = (d.year * 4 + (d.month - 1) // 3) - lag
        return f"{q_abs // 4}-Q{q_abs % 4 + 1}"
    raise ValueError(f"ics.ref.unit desconhecido: {unit!r}")


def _pair_days(dates: list[date]) -> list[tuple[date | None, date]]:
    """Junta dias consecutivos num par (dia 1, dia 2).

    O feed do Copom emite os dois dias da reuniao como eventos separados; a decisao
    sai no fim do dia 2, que e a data que interessa. Dia isolado (sem vizinho)
    vira (None, dia) em vez de ser descartado.
    """
    out: list[tuple[date | None, date]] = []
    i = 0
    while i < len(dates):
        if i + 1 < len(dates) and dates[i + 1] - dates[i] == timedelta(days=1):
            out.append((dates[i], dates[i + 1]))
            i += 2
        else:
            out.append((None, dates[i]))
            i += 1
    return out


def _flow(mapping: dict) -> CommentedMap:
    """Entrada em flow style (`{date: "...", ...}`), com strings entre aspas duplas.

    As aspas sao explicitas de proposito: sem `DoubleQuotedScalarString`, o ruamel
    escreve `reference_period: 2026-06` sem aspas — que continua carregando como
    string, mas destoa do resto do arquivo e convida um leitor (ou um parser menos
    tolerante) a tratar como data.
    """
    m = CommentedMap(
        {k: (_dq(v) if isinstance(v, str) else v) for k, v in mapping.items()}
    )
    m.fa.set_flow_style()
    return m


def _dq(valor: str) -> DoubleQuotedScalarString:
    return DoubleQuotedScalarString(valor)


def _gravar_entries(group: CommentedMap, itens: list) -> None:
    """Substitui `entries` preservando a linha em branco que separa os grupos.

    Essa linha fica em `entries.ca.end` (rodape da sequencia), nao em `ca.items`.
    Duas tentativas anteriores falharam: mexer em `ca.items` (indice errado) e
    copiar `ca.end` para um CommentedSeq novo (o dumper ignora). O que funciona e
    NAO trocar o objeto: mutando a sequencia original via slice, a identidade — e
    com ela o `ca.end` — sobrevive, e os grupos continuam separados no arquivo.
    """
    alvo = group.get("entries")
    if isinstance(alvo, CommentedSeq):
        alvo[:] = itens
    else:
        group["entries"] = CommentedSeq(itens)


# ------------------------------------------------------------------- refresh


def _feed_entries(group: dict, agenda: BCBAgenda, cutoff: date, until: date) -> list[dict]:
    """Entradas que o feed implica para um grupo, no formato do YAML."""
    cfg = group["ics"]
    eventos = agenda.eventos(
        cfg["lista"],
        start=cutoff,
        end=until,
        summary_contains=cfg.get("summary_contains"),
    )
    datas = sorted({e["date"] for e in eventos})

    pares: list[tuple[date | None, date]]
    pares = _pair_days(datas) if cfg.get("pair_days") else [(None, d) for d in datas]

    ref = cfg.get("ref")
    out = []
    for inicio, d in pares:
        item: dict = {"date": d.isoformat()}
        if inicio is not None:
            item["date_start"] = inicio.isoformat()
        if ref:
            item["reference_period"] = _ref_period(d, ref["unit"], int(ref["lag"]))
        item["confirmed"] = True
        out.append(item)
    return out


def _diff(antigas: list[dict], novas: list[dict]) -> dict:
    """Compara entradas antigas e novas.

    Casa por DATA primeiro, e so depois usa `reference_period` para achar revisoes
    entre o que sobrou. A ordem importa: casar por periodo primeiro gera falso
    positivo em todo grupo cujo periodo nao e derivavel do feed (o Copom usa
    "281ª reunião", que o script nao inventa), e o par add+remove resultante
    apagaria a nota escrita a mao junto.
    """
    ant_por_data = {str(e["date"]): e for e in antigas}
    nov_por_data = {str(e["date"]): e for e in novas}

    iguais = [n for n in novas if str(n["date"]) in ant_por_data]
    sobra_nov = [n for n in novas if str(n["date"]) not in ant_por_data]
    sobra_ant = [a for a in antigas if str(a["date"]) not in nov_por_data]

    # mesmo periodo de referencia + data diferente = a fonte revisou a data
    ant_por_ref: dict[str, dict] = {}
    for a in sobra_ant:
        ref = a.get("reference_period")
        if ref:
            ant_por_ref.setdefault(str(ref), a)

    shifts, add, casados = [], [], set()
    for n in sobra_nov:
        ref = n.get("reference_period")
        a = ant_por_ref.get(str(ref)) if ref else None
        if a is not None and id(a) not in casados:
            shifts.append((a, n))
            casados.add(id(a))
        else:
            add.append(n)

    rem = [a for a in sobra_ant if id(a) not in casados]
    return {"iguais": iguais, "shifts": shifts, "add": add, "rem": rem}


def _em_escopo(entrada: dict, cutoff: date, until: date) -> bool:
    """A entrada cai na janela que o feed cobre nesta rodada?"""
    d = date.fromisoformat(str(entrada["date"]))
    return cutoff <= d <= until


def _merge(
    antigas: list[dict], novas: list[dict], cutoff: date, until: date
) -> tuple[list, list[str]]:
    """Monta a lista final de entradas, preservando o que foi escrito a mao.

    - entradas FORA da janela [cutoff, until] ficam intactas. Vale para os dois
      lados: o que ja passou (registro historico) e o que alguem tenha adicionado
      alem do fim do ano do arquivo. Sem essa guarda, uma entrada de 2027 num
      arquivo de 2026 seria apagada pelo --write por "nao estar no feed".
    - `note` escrita a mao e carregada para a entrada nova de mesma data e, se a
      fonte revisou a data, recuperada pelo `reference_period` — senao a revisao
      apagaria a nota em silencio. Nesse caso sai aviso, porque a nota pode ter
      sido escrita sobre a data antiga e nao valer mais.
    - `reference_period` existente vence quando o grupo nao tem regra para derivar
      (Copom: o numero da reuniao nao sai do feed).
    """
    por_data = {str(e["date"]): e for e in antigas}
    por_ref: dict[str, dict] = {}
    for e in antigas:
        ref = e.get("reference_period")
        if ref:
            por_ref.setdefault(str(ref), e)

    # Um grupo "usa periodo" se alguma entrada existente tem reference_period. Sem
    # isso o Focus — que legitimamente nunca tem periodo — geraria um aviso por
    # divulgacao nova, afogando os avisos que importam.
    usa_ref = any("reference_period" in e for e in antigas)

    avisos: list[str] = []
    itens: list = [e for e in antigas if not _em_escopo(e, cutoff, until)]

    for nova in novas:
        antiga = por_data.get(str(nova["date"]))
        item = dict(nova)

        if antiga is None and nova.get("reference_period"):
            candidata = por_ref.get(str(nova["reference_period"]))
            if candidata is not None and "note" in candidata:
                antiga = candidata
                avisos.append(
                    f"{nova['date']}: nota herdada de {candidata['date']} (data "
                    f"revisada pela fonte) — reconfirmar se ainda se aplica"
                )

        if antiga is not None:
            if "note" in antiga:
                item["note"] = antiga["note"]
            if "reference_period" not in item and "reference_period" in antiga:
                item["reference_period"] = antiga["reference_period"]
        elif usa_ref and "reference_period" not in item:
            avisos.append(
                f"{nova['date']}: entrada nova sem reference_period derivavel "
                f"— preencher a mao"
            )

        # ordem estavel das chaves, igual ao resto do arquivo
        ordem = ["date", "date_start", "reference_period", "confirmed", "note"]
        itens.append(_flow({k: item[k] for k in ordem if k in item}))

    itens.sort(key=lambda e: str(e["date"]))
    return itens, avisos


def refresh(
    path: Path | str = _YAML_DEFAULT,
    cutoff: date | None = None,
    until: date | None = None,
    write: bool = False,
) -> int:
    """Le o YAML, busca os feeds, reporta o drift e opcionalmente grava.

    Returns:
        int: numero de grupos com alguma mudanca.
    """
    path = Path(path)
    cutoff = cutoff or date.today()
    if until is None:
        # ano do nome do arquivo (calendar_2026.yaml -> 2026): impede que uma rodada
        # em 2026 escreva datas de 2027 num arquivo cujo escopo e 2026.
        m = re.search(r"(20\d{2})", path.name)
        ano = int(m.group(1)) if m else cutoff.year
        until = date(ano, 12, 31)

    y = _yaml()
    doc = y.load(path.read_text(encoding="utf-8"))
    agenda = BCBAgenda()

    print(f"calendario : {path.name}")
    print(f"janela     : {cutoff} -> {until}")
    print(f"modo       : {'ESCRITA' if write else 'dry-run (nada sera gravado)'}\n")

    manuais, mudados = [], 0

    for group in doc["groups"]:
        slug = group["group"]
        if "ics" not in group:
            manuais.append(slug)
            continue

        # sem list(): o CommentedSeq original carrega o `ca.end` com a linha em
        # branco que separa os grupos, e copiar para list() jogaria isso fora
        antigas = group.get("entries") or []
        novas = _feed_entries(group, agenda, cutoff, until)
        # diff so contra o que esta na janela: entrada fora dela nao "saiu do feed",
        # o feed simplesmente nao foi consultado ali
        d = _diff([e for e in antigas if _em_escopo(e, cutoff, until)], novas)

        tem_mudanca = bool(d["shifts"] or d["add"] or d["rem"])
        if tem_mudanca:
            mudados += 1

        marca = "*" if tem_mudanca else " "
        print(f"{marca} {slug}  [{group['ics']['lista']}]")
        for a, n in d["shifts"]:
            ref = n.get("reference_period", "")
            print(f"      ~ {a['date']} -> {n['date']}   {ref}   REVISAO DE DATA")
        for n in d["add"]:
            print(f"      + {n['date']}   {n.get('reference_period', '')}   nova")
        for a in d["rem"]:
            print(f"      - {a['date']}   {a.get('reference_period', '')}   saiu do feed")
        if not tem_mudanca:
            print(f"      = {len(d['iguais'])} entradas, sem mudanca")

        itens, avisos = _merge(antigas, novas, cutoff, until)
        for aviso in avisos:
            print(f"      ! {aviso}")
        if write:
            _gravar_entries(group, itens)

    if manuais:
        print(f"\nsem feed ICS (seguem manuais): {', '.join(manuais)}")

    if write:
        buf = io.StringIO()
        y.dump(doc, buf)
        path.write_text(buf.getvalue(), encoding="utf-8", newline="\n")
        print(f"\ngravado: {path}")
    elif mudados:
        print(f"\n{mudados} grupo(s) com drift — rode com --write para aplicar")
    else:
        print("\nnenhuma mudanca; o arquivo ja esta em dia")

    return mudados


# ------------------------------------------------------------------ coverage


def coverage(path: Path | str = _YAML_DEFAULT) -> dict:
    """Compara as tabelas do banco com as cobertas por algum grupo do calendario.

    Aponta as duas direcoes: tabela sem calendario (nao da para dizer quando o dado
    proximo sai) e nome no YAML que nao existe no banco (tipicamente typo ou tabela
    renomeada/removida).
    """
    import mysql.connector
    from dotenv import load_dotenv

    load_dotenv()
    path = Path(path)
    doc = _yaml().load(path.read_text(encoding="utf-8"))

    no_yaml: dict[str, list[str]] = {}
    for g in doc["groups"]:
        for t in g.get("tables") or []:
            no_yaml.setdefault(str(t), []).append(g["group"])

    conn = mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST", "localhost"),
        user=os.environ.get("MYSQL_USER", "root"),
        password=os.environ.get("MYSQL_PASSWORD", ""),
    )
    try:
        cur = conn.cursor()
        placeholders = ", ".join(["%s"] * len(_SCHEMAS))
        cur.execute(
            "SELECT table_schema, table_name FROM information_schema.tables "
            f"WHERE table_schema IN ({placeholders}) AND table_type = 'BASE TABLE'",
            _SCHEMAS,
        )
        no_banco = {t: s for s, t in cur.fetchall()}
        cur.close()
    finally:
        conn.close()

    sem_calendario = sorted(t for t in no_banco if t not in no_yaml)
    fantasmas = sorted(t for t in no_yaml if t not in no_banco)

    print(f"tabelas no banco ({', '.join(_SCHEMAS)}): {len(no_banco)}")
    print(f"tabelas cobertas por algum grupo        : {len(no_banco) - len(sem_calendario)}\n")

    print(f"SEM grupo de calendario ({len(sem_calendario)}):")
    for t in sem_calendario:
        print(f"    {no_banco[t]}.{t}")

    if fantasmas:
        print(f"\nNO YAML mas NAO no banco ({len(fantasmas)}) — typo ou tabela removida:")
        for t in fantasmas:
            print(f"    {t}   (grupos: {', '.join(no_yaml[t])})")

    return {"sem_calendario": sem_calendario, "fantasmas": fantasmas}


def horizonte(path: Path | str = _YAML_DEFAULT) -> list[dict]:
    """Mede ate onde cada feed ICS chega. Rodar ANTES de planejar um rollover de ano.

    Existe porque o horizonte foi documentado errado uma vez ("~18 meses para frente",
    quando a maioria das listas para em 31/12 do ano corrente) e a suposicao passou
    meses sem ser checada. Ver ROLLOVER.md, passo 0.
    """
    doc = _yaml().load(Path(path).read_text(encoding="utf-8"))
    agenda = BCBAgenda()
    hoje = date.today()
    out = []

    print(f"horizonte dos feeds ICS (hoje = {hoje}):\n")
    for g in doc["groups"]:
        if "ics" not in g:
            continue
        slug, lista = g["group"], g["ics"]["lista"]
        try:
            ev = agenda.eventos(lista, start=date(2020, 1, 1), end=date(2035, 12, 31))
        except Exception as exc:  # feed fora do ar nao deve derrubar o resto
            print(f"  {slug:28s} ERRO {type(exc).__name__}: {exc}")
            continue
        datas = sorted(e["date"] for e in ev)
        if not datas:
            print(f"  {slug:28s} 0 eventos")
            continue
        ultimo = datas[-1]
        meses = (ultimo.year - hoje.year) * 12 + (ultimo.month - hoje.month)
        print(f"  {slug:28s} {len(datas):3d} ev   {datas[0]} -> {ultimo}   (+{meses}m)")
        out.append({"grupo": slug, "lista": lista, "n": len(datas),
                    "primeiro": datas[0], "ultimo": ultimo, "meses": meses})

    if out:
        fim_ano = date(hoje.year, 12, 31)
        presos = [o["grupo"] for o in out if o["ultimo"] <= fim_ano]
        print(f"\n{len(presos)}/{len(out)} feeds param em {hoje.year} ou antes"
              f"{': ' + ', '.join(presos) if presos else ''}")
        print(f"maior horizonte: {max(o['ultimo'] for o in out)}")
    return out


def listar_listas() -> list[dict]:
    """Imprime as listas de calendario publicadas pelo BCB."""
    listas = BCBAgenda().listas()
    print(f"{len(listas)} listas publicadas pelo BCB:\n")
    for item in listas:
        tag = " (agenda de eventos)" if item["e_evento"] else ""
        print(f"  {item['lista']}{tag}")
    return listas


# ----------------------------------------------------------------------- cli


def run(**kwargs) -> int:
    """Entry point no padrao dos outros scripts do projeto."""
    return refresh(**kwargs)


def main(argv: list[str] | None = None) -> int:
    # o console do Windows abre em cp1252 e os nomes das listas tem acento/en-dash
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    p = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    p.add_argument("--yaml", default=str(_YAML_DEFAULT), help="caminho do calendario")
    p.add_argument("--write", action="store_true", help="grava as mudancas no YAML")
    p.add_argument("--from", dest="cutoff", metavar="YYYY-MM-DD",
                   help="data minima (default: hoje)")
    p.add_argument("--until", metavar="YYYY-MM-DD",
                   help="data maxima (default: 31/12 do ano no nome do arquivo)")
    p.add_argument("--coverage", action="store_true",
                   help="compara com as tabelas do banco e sai")
    p.add_argument("--listas", action="store_true",
                   help="enumera as listas de calendario do BCB e sai")
    p.add_argument("--horizonte", action="store_true",
                   help="mede ate onde cada feed ICS chega e sai (ver ROLLOVER.md)")
    args = p.parse_args(argv)

    if args.listas:
        listar_listas()
        return 0
    if args.horizonte:
        horizonte(args.yaml)
        return 0
    if args.coverage:
        coverage(args.yaml)
        return 0

    refresh(
        path=args.yaml,
        cutoff=date.fromisoformat(args.cutoff) if args.cutoff else None,
        until=date.fromisoformat(args.until) if args.until else None,
        write=args.write,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
