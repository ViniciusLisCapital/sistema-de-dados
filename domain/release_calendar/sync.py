"""
Confronta o calendario de divulgacoes com o que efetivamente esta no banco.

Responde a pergunta que `jobs/update_db.py` nao sabe responder: o script rodou sem
excecao, mas o dado chegou? Hoje um `46/46 OK` no log conviveria com uma fonte que
devolveu silenciosamente o mesmo dado da semana passada.

Como funciona (sem arquivo de estado, sem "quando foi a ultima execucao"):

    esperado  = periodo de referencia da divulgacao mais recente ja ocorrida
    observado = MAX(`date`) da tabela no banco
    veredito  = observado >= esperado ? OK : ATRASADO

E possivel ser stateless porque as duas pontas ja existem: o YAML diz qual PERIODO
cada divulgacao entrega (`reference_period`) e as 63 tabelas de dado publicado usam
a mesma coluna `date` na mesma convencao (inicio do mes para mensal, inicio do
trimestre para trimestral). Nao ha config por tabela, e um dia perdido nao gera
drift: a comparacao e sempre contra o estado atual, nao contra um marcador.

Uso:

    # relatorio completo (exit 1 se houver atraso)
    uv run python -m domain.release_calendar.sync

    # so o resumo, sem listar as tabelas OK
    uv run python -m domain.release_calendar.sync --quiet

    # tolera divulgacoes de hoje/ontem que talvez ainda nao tenham sido coletadas
    uv run python -m domain.release_calendar.sync --grace 1

    # simula outra data (util para testar contra o historico do YAML)
    uv run python -m domain.release_calendar.sync --as-of 2026-09-15

Rodar da raiz do projeto: a leitura do `.env` (credenciais MySQL) usa `load_dotenv()`
sem caminho explicito, mesmo padrao do `--coverage` do update_calendar.py.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import yaml

_AQUI = Path(__file__).parent
_YAML_DEFAULT = _AQUI / "calendar_2026.yaml"

_SCHEMAS = ("macro_brasil", "macro_international")

# Coluna de tempo comum a toda tabela de dado publicado. Remedido 2026-08-18:
# 68 das 69 tabelas dos dois schemas tem exatamente esta coluna, e a unica excecao
# (inflc_dim) e tabela de dimensao, nao serie divulgada. As outras duas excecoes de
# 2026-08-17 (pm_parametros, pm_hiato_seed) deixaram de existir com a remocao da
# replica do modelo do BCB.
_COL_DATA = "date"

# Vereditos
OK = "OK"
ATRASADO = "ATRASADO"
SEM_EXPECTATIVA = "SEM EXPECTATIVA"
SEM_CALENDARIO = "SEM CALENDARIO"
SEM_DIVULGACAO = "SEM DIVULGACAO"

_ORDEM = [ATRASADO, SEM_CALENDARIO, SEM_EXPECTATIVA, OK, SEM_DIVULGACAO]


# --------------------------------------------------------------- periodo -> data


_RE_MES = re.compile(r"^(\d{4})-(\d{2})$")
_RE_TRI = re.compile(r"^(\d{4})-Q([1-4])$", re.I)
_RE_DIA = re.compile(r"^(\d{4})-(\d{2})-(\d{2})$")


def periodo_para_data(ref: str | None) -> date | None:
    """Converte um `reference_period` do YAML no valor esperado de `MAX(date)`.

    O campo tem quatro formas no arquivo, e so tres sao datavel:

        "2026-08"          -> 2026-08-01   (mensal, convencao inicio do mes)
        "2026-Q2"          -> 2026-04-01   (trimestral, inicio do trimestre)
        "2026-08-11"       -> 2026-08-11   (CFTC: a terca-feira do snapshot de posicao)
        "281ª reunião"     -> None         (numero de reuniao do Copom)
        "Sep 2026 (SEP)"   -> None         (texto livre do FOMC)

    Devolver None para as duas ultimas e deliberado, nao uma lacuna: uma reuniao de
    Copom/FOMC nao entrega um periodo de dado, entao nao ha o que exigir do banco.
    E o que evita, por exemplo, cobrar de `diferenciais_juros` (mensal) um avanco a
    cada reuniao do FOMC (8x/ano) — o grupo `fomc` simplesmente nao gera expectativa.
    """
    if not ref:
        return None
    ref = ref.strip()

    # try/except em volta de tudo: o YAML e editado a mao, e um "2026-13" que casa
    # a regex mas nao existe como data nao pode derrubar a checagem inteira -- vale
    # mais tratar como periodo nao datavel (o mesmo caminho do Copom/FOMC).
    try:
        m = _RE_MES.match(ref)
        if m:
            return date(int(m.group(1)), int(m.group(2)), 1)

        m = _RE_TRI.match(ref)
        if m:
            return date(int(m.group(1)), (int(m.group(2)) - 1) * 3 + 1, 1)

        m = _RE_DIA.match(ref)
        if m:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None

    return None


def _divulgada_em(entrada: dict) -> date | None:
    """Data a partir da qual a divulgacao pode ser considerada ocorrida.

    Entradas com janela (`date`/`date_end`, usadas nas estimativas confirmed:false)
    contam so depois do fim da janela — cobrar o dado no primeiro dia de um intervalo
    de uma semana produziria atraso falso durante toda a janela.
    """
    bruto = entrada.get("date_end") or entrada.get("date")
    if isinstance(bruto, date):
        return bruto
    if isinstance(bruto, str):
        try:
            return datetime.strptime(bruto[:10], "%Y-%m-%d").date()
        except ValueError:
            return None
    return None


# ------------------------------------------------------------------ calendario


def carregar(path: Path | str = _YAML_DEFAULT) -> dict:
    """Le o YAML do calendario. Somente leitura — nao usa ruamel (nao reescreve nada)."""
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def tabelas_por_grupo(doc: dict) -> dict[str, list[str]]:
    return {g["group"]: [str(t) for t in (g.get("tables") or [])] for g in doc["groups"]}


def _menos_meses(d: date, n: int) -> date:
    total = (d.year * 12 + d.month - 1) - n
    return date(total // 12, total % 12 + 1, d.day)


def expectativas(
    doc: dict, as_of: date, grace: int = 0
) -> tuple[dict[str, dict], dict[str, str]]:
    """Para cada tabela, o periodo mais recente que o calendario diz que ja deveria estar la.

    Devolve (expectativas, motivos): o segundo dict explica, para cada tabela COBERTA
    por algum grupo mas sem expectativa, por que nao houve — a distincao importa, sao
    tres causas diferentes e so uma e um problema a resolver:

        "sem divulgacao passada no arquivo"  -> lacuna de backfill (IBGE/Tesouro/MTE/MDIC,
                                                cujos grupos so tem datas futuras)
        "periodo nao datavel"                -> por design (Copom "281ª reunião", FOMC)
        "override: ..."                      -> mapeamento corrigido a mao no YAML

    Uma tabela pode pertencer a varios grupos (`cred_inadimplencia_pj` esta em
    bcb_credit_note e bcb_copom; `expc_focus` em tres). Vale a expectativa MAIS ALTA
    entre os grupos — o grupo que exige menos nao pode absolver o que outro ja cobra.
    """
    corte = as_of - timedelta(days=grace)
    ovr = doc.get("expectation_overrides") or {}

    out: dict[str, dict] = {}
    motivos: dict[str, str] = {}
    tem_passada: set[str] = set()  # tabela cujo grupo tem >= 1 divulgacao ja ocorrida
    ultima_div: dict[str, tuple[date, str, str | None]] = {}  # tabela -> divulgacao mais recente

    for g in doc["groups"]:
        tabelas = [str(t) for t in (g.get("tables") or [])]
        if not tabelas:
            continue
        for e in g.get("entries") or []:
            quando = _divulgada_em(e)
            if quando is None or quando > corte:
                continue  # divulgacao futura (ou dentro do grace) — nada a exigir
            tem_passada.update(tabelas)
            for t in tabelas:
                if t not in ultima_div or quando > ultima_div[t][0]:
                    ultima_div[t] = (quando, g["group"], g.get("institution"))
            esperado = periodo_para_data(e.get("reference_period"))
            if esperado is None:
                continue
            for t in tabelas:
                atual = out.get(t)
                if atual is None or esperado > atual["esperado"]:
                    out[t] = {
                        "esperado": esperado,
                        "grupo": g["group"],
                        "institution": g.get("institution"),
                        "divulgado_em": quando,
                        "reference_period": e.get("reference_period"),
                    }

    # overrides: o vinculo grupo->tabela do YAML e de relevancia, nao sempre de entrega
    for tabela, regra in ovr.items():
        tabela = str(tabela)
        porque = " ".join((regra.get("why") or "").split())
        if regra.get("expect") == "none":
            out.pop(tabela, None)
            motivos[tabela] = f"override: {porque}"
        elif regra.get("lag_months") and tabela in out:
            n = int(regra["lag_months"])
            out[tabela]["esperado"] = _menos_meses(out[tabela]["esperado"], n)
            out[tabela]["override"] = f"-{n}m: {porque}"
        elif regra.get("release_minus_days") is not None:
            # ancora na DATA da divulgacao, nao no periodo de referencia: serve para
            # grupo de alta frequencia cujo feed nao traz periodo nenhum (Focus).
            n = int(regra["release_minus_days"])
            if tabela in ultima_div:
                quando, grupo, inst = ultima_div[tabela]
                out[tabela] = {
                    "esperado": quando - timedelta(days=n),
                    "grupo": grupo,
                    "institution": inst,
                    "divulgado_em": quando,
                    "reference_period": None,
                    "override": f"data da divulgacao -{n}d: {porque}",
                }

    # max_age_days: conteudo diario nao tem periodo de referencia para comparar, a
    # regra e "quao velho pode estar em relacao a HOJE". Vale a expectativa MAIS ALTA
    # entre esta e a do calendario -- uma serie diaria pendurada numa nota mensal
    # precisa satisfazer as duas, e era justamente a mensal (frouxa) que a absolvia.
    for tabela, dias in (doc.get("max_age_days") or {}).items():
        tabela = str(tabela)
        limite = corte - timedelta(days=int(dias))
        atual = out.get(tabela)
        if atual is None or limite > atual["esperado"]:
            out[tabela] = {
                "esperado": limite,
                "grupo": (atual or {}).get("grupo") or "(max_age_days)",
                "institution": (atual or {}).get("institution"),
                "divulgado_em": (atual or {}).get("divulgado_em"),
                "reference_period": None,
                "override": f"max {dias}d de atraso",
            }
        motivos.pop(tabela, None)

    todas = {t for g in doc["groups"] for t in (g.get("tables") or [])}
    for t in todas:
        t = str(t)
        if t in out or t in motivos:
            continue
        motivos[t] = ("periodo nao datavel" if t in tem_passada
                      else "sem divulgacao passada no arquivo")

    return out, motivos


def _no_release(doc: dict) -> dict[str, list[str]]:
    """Le `no_release:` aceitando as duas formas.

    Hoje e um mapa por motivo (`continuous:` / `not_a_series:`); a forma antiga era
    uma lista simples. Aceitar as duas evita que um YAML de outro ano (ou um
    calendar_2027.yaml copiado antes desta mudanca) quebre a checagem.
    """
    bruto = doc.get("no_release") or {}
    if isinstance(bruto, list):
        return {"continuous": [str(t) for t in bruto]}
    return {str(k): [str(t) for t in (v or [])] for k, v in bruto.items()}


def sem_divulgacao(doc: dict) -> set[str]:
    """Todas as tabelas sem evento de divulgacao, qualquer que seja o motivo.

    Serie continua de mercado (PTAX, DXY, Brent) e tabela que nao e serie divulgada
    (dimensao, parametro de modelo). Precisa ser declarado em vez de inferido: se
    "tabela sem grupo" virasse automaticamente "tabela sem divulgacao", uma lacuna
    real de cobertura ficaria indistinguivel de uma decisao consciente.
    """
    return {t for ts in _no_release(doc).values() for t in ts}


def continuas(doc: dict) -> list[str]:
    """O que `jobs/update_db.py --continuous` roda todo dia.

    Uniao de duas coisas, nao so de `no_release.continuous`:
      * as series sem evento de divulgacao (PTAX, DXY, Brent...)
      * toda tabela com `max_age_days`, que por definicao tem conteudo diario

    A segunda metade e o que traz `cmb_reservas_bc` e `cmb_cambio_contratado` para o
    passe diario: as duas TEM divulgacao mensal (a nota do setor externo), mas o
    conteudo diario delas fica semanas parado se so a nota disparar a atualizacao --
    foi exatamente o que aconteceu em 2026-08-19.

    Exclui `not_a_series` (dimensao/parametros), que nao entram em job diario.
    """
    nr = _no_release(doc)
    naoserie = set(nr.get("not_a_series") or [])
    alvos = set(nr.get("continuous") or []) | {
        str(t) for t in (doc.get("max_age_days") or {})
    }
    return sorted(alvos - naoserie)


# ----------------------------------------------------------------------- banco


def estado_banco(schemas: tuple[str, ...] = _SCHEMAS) -> dict[str, dict]:
    """{tabela: {schema, tem_data, max_date, linhas}} para os schemas informados.

    Um unico UNION ALL sobre as tabelas que tem a coluna `date`, em vez de 60+
    round-trips. Os nomes vem do information_schema (nao de input do usuario), mas
    vao entre backticks de todo jeito.
    """
    import mysql.connector
    from dotenv import load_dotenv

    load_dotenv()

    conn = mysql.connector.connect(
        host=os.environ.get("MYSQL_HOST", "localhost"),
        user=os.environ.get("MYSQL_USER", "root"),
        password=os.environ.get("MYSQL_PASSWORD", ""),
    )
    try:
        cur = conn.cursor()
        ph = ", ".join(["%s"] * len(schemas))

        cur.execute(
            "SELECT table_schema, table_name FROM information_schema.tables "
            f"WHERE table_schema IN ({ph}) AND table_type = 'BASE TABLE'",
            schemas,
        )
        tabelas = {t: s for s, t in cur.fetchall()}

        cur.execute(
            "SELECT table_schema, table_name FROM information_schema.columns "
            f"WHERE table_schema IN ({ph}) AND column_name = %s",
            (*schemas, _COL_DATA),
        )
        com_data = {t for _, t in cur.fetchall()}

        out = {
            t: {"schema": s, "tem_data": t in com_data, "max_date": None, "linhas": None}
            for t, s in tabelas.items()
        }

        alvos = sorted(t for t in tabelas if t in com_data)
        if alvos:
            partes = [
                f"SELECT '{t}' AS t, MAX(`{_COL_DATA}`) AS mx, COUNT(*) AS n "
                f"FROM `{tabelas[t]}`.`{t}`"
                for t in alvos
            ]
            cur.execute(" UNION ALL ".join(partes))
            for t, mx, n in cur.fetchall():
                out[t]["max_date"] = mx
                out[t]["linhas"] = n

        cur.close()
    finally:
        conn.close()

    return out


# --------------------------------------------------------------------- veredito


def status(
    path: Path | str = _YAML_DEFAULT,
    as_of: date | None = None,
    grace: int = 0,
) -> list[dict]:
    """Uma linha por tabela do banco, com veredito. Nao imprime nada."""
    as_of = as_of or date.today()
    doc = carregar(path)

    esperadas, motivos = expectativas(doc, as_of, grace)
    isentas = sem_divulgacao(doc)
    banco = estado_banco()
    no_yaml = {t for ts in tabelas_por_grupo(doc).values() for t in ts}

    linhas: list[dict] = []
    for tabela, info in sorted(banco.items()):
        exp = esperadas.get(tabela)
        obs = info["max_date"]

        # A expectativa vem primeiro de proposito: uma tabela de `no_release.continuous`
        # que tenha max_age_days DEVE ser checada, nao absolvida por "nao tem divulgacao".
        if exp is not None and info["tem_data"]:
            veredito = OK if (obs is not None and obs >= exp["esperado"]) else ATRASADO
        elif tabela in isentas:
            veredito = SEM_DIVULGACAO
        elif tabela not in no_yaml:
            veredito = SEM_CALENDARIO
        else:
            veredito = SEM_EXPECTATIVA

        linhas.append({
            "tabela": tabela,
            "schema": info["schema"],
            "veredito": veredito,
            "observado": obs,
            "linhas": info["linhas"],
            "esperado": exp["esperado"] if exp else None,
            "grupo": exp["grupo"] if exp else None,
            "institution": exp["institution"] if exp else None,
            "divulgado_em": exp["divulgado_em"] if exp else None,
            "reference_period": exp["reference_period"] if exp else None,
            # None quando a expectativa vem de max_age_days numa tabela sem
            # divulgacao nenhuma (serie continua) — nao ha release para contar desde.
            "dias": ((as_of - exp["divulgado_em"]).days
                     if exp and exp.get("divulgado_em") else None),
            "override": exp.get("override") if exp else None,
            "motivo": motivos.get(tabela),
        })

    # tabelas citadas no YAML que nao existem no banco (typo / tabela removida)
    for tabela in sorted(no_yaml - set(banco)):
        linhas.append({
            "tabela": tabela, "schema": None, "veredito": SEM_CALENDARIO,
            "observado": None, "linhas": None, "esperado": None,
            "grupo": None, "institution": None, "divulgado_em": None,
            "reference_period": None, "dias": None, "override": None,
            "motivo": None, "fantasma": True,
        })

    return linhas


def status_por_grupo(
    path: Path | str = _YAML_DEFAULT,
    as_of: date | None = None,
    grace: int = 0,
) -> dict[str, dict]:
    """Um veredito por GRUPO do calendario, para o botao "Atualizar" do relatorio.

    O relatorio HTML tem uma linha por divulgacao, nao por tabela, entao precisa de um
    estado agregado. Vale o pior veredito entre as tabelas do grupo — uma tabela
    atrasada ja justifica o botao, mesmo que as outras 11 estejam em dia.

    Estados: "atrasado" | "ok" | "indefinido" (nenhuma tabela verificavel — grupo sem
    periodo datavel, tipo Copom/FOMC) | "vazio" (grupo sem tabelas).
    """
    linhas = status(path, as_of, grace)
    por_tabela = {r["tabela"]: r for r in linhas}

    out: dict[str, dict] = {}
    for slug, tabelas in tabelas_por_grupo(carregar(path)).items():
        rows = [por_tabela[t] for t in tabelas if t in por_tabela]
        vereditos = {r["veredito"] for r in rows}
        if not rows:
            estado = "vazio"
        elif ATRASADO in vereditos:
            estado = "atrasado"
        elif OK in vereditos:
            estado = "ok"
        else:
            estado = "indefinido"
        out[slug] = {
            "estado": estado,
            "tabelas": [
                {
                    "tabela": r["tabela"],
                    "veredito": r["veredito"],
                    "observado": str(r["observado"]) if r["observado"] else None,
                    "esperado": str(r["esperado"]) if r["esperado"] else None,
                }
                for r in rows
            ],
        }
    return out


def grupos_atrasados(
    path: Path | str = _YAML_DEFAULT,
    as_of: date | None = None,
    grace: int = 0,
) -> dict[str, list[str]]:
    """{grupo: [tabelas atrasadas]} — o que um `--due` no update_db.py precisaria rodar.

    Exposto aqui (e nao no job) porque e a mesma conta do relatorio; o job e o botao
    do relatorio HTML consomem isto em vez de reimplementar a comparacao.
    """
    out: dict[str, list[str]] = {}
    for r in status(path, as_of, grace):
        if r["veredito"] == ATRASADO:
            out.setdefault(r["grupo"], []).append(r["tabela"])
    return out


# -------------------------------------------------------------------- relatorio


def report(
    path: Path | str = _YAML_DEFAULT,
    as_of: date | None = None,
    grace: int = 0,
    quiet: bool = False,
) -> list[dict]:
    as_of = as_of or date.today()
    linhas = status(path, as_of, grace)

    por_veredito: dict[str, list[dict]] = {}
    for r in linhas:
        por_veredito.setdefault(r["veredito"], []).append(r)

    print(f"freshness do banco vs. calendario  (as_of = {as_of}, grace = {grace}d)\n")
    resumo = "   ".join(
        f"{v}: {len(por_veredito.get(v, []))}" for v in _ORDEM if por_veredito.get(v)
    )
    print(f"  {len(linhas)} tabelas   |   {resumo}\n")

    for veredito in _ORDEM:
        grupo = por_veredito.get(veredito)
        if not grupo:
            continue
        if quiet and veredito in (OK, SEM_DIVULGACAO):
            continue

        print(f"{veredito} ({len(grupo)}):")
        for r in grupo:
            if veredito == ATRASADO:
                # serie continua nao tem divulgacao para citar: mostra a regra de idade
                if r["divulgado_em"]:
                    origem = f"{r['grupo']} div. {r['divulgado_em']:%d/%m} ({r['dias']}d)"
                else:
                    origem = f"{r['grupo']} {r['override'] or ''}".strip()
                print(f"    {r['tabela']:34s} esperado >= {r['esperado']}   "
                      f"no banco {r['observado'] or '(vazia)'}   {origem}")
            elif veredito == OK:
                marca = "  [lag]" if r["override"] else ""
                print(f"    {r['tabela']:34s} {r['observado']}   "
                      f">= {r['esperado']}   {r['grupo']}{marca}")
            elif veredito == SEM_EXPECTATIVA:
                motivo = r["motivo"] or "sem grupo com periodo datavel"
                if len(motivo) > 78:
                    motivo = motivo[:75] + "..."
                # str() antes do :12s de proposito -- date.__format__ trata o format
                # spec como padrao de strftime, entao "{data:12s}" imprime "12s".
                obs = str(r["observado"] or "(sem coluna date)")
                print(f"    {r['tabela']:34s} {obs:12s}  — {motivo}")
            elif veredito == SEM_CALENDARIO:
                marca = "  (no YAML, ausente do banco)" if r.get("fantasma") else ""
                print(f"    {r['tabela']:34s} {r['observado'] or '-'}{marca}")
            else:
                print(f"    {r['tabela']:34s} {r['observado'] or '-'}")
        print()

    atrasadas = por_veredito.get(ATRASADO, [])
    if atrasadas:
        grupos = sorted({r["grupo"] for r in atrasadas})
        print(f"{len(atrasadas)} tabela(s) atrasada(s) em {len(grupos)} grupo(s): "
              f"{', '.join(grupos)}")
    else:
        print("nenhuma tabela atrasada.")

    return linhas


def run(**kwargs) -> list[dict]:
    """Entry point no padrao dos outros scripts do projeto."""
    return report(**kwargs)


def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    p = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    p.add_argument("--yaml", default=str(_YAML_DEFAULT), help="caminho do calendario")
    p.add_argument("--as-of", metavar="YYYY-MM-DD",
                   help="data de referencia (default: hoje)")
    p.add_argument("--grace", type=int, default=0, metavar="N",
                   help="ignora divulgacoes dos ultimos N dias (default: 0)")
    p.add_argument("--quiet", action="store_true",
                   help="omite as listas OK e SEM DIVULGACAO")
    args = p.parse_args(argv)

    as_of = (datetime.strptime(args.as_of, "%Y-%m-%d").date() if args.as_of
             else date.today())

    linhas = report(args.yaml, as_of=as_of, grace=args.grace, quiet=args.quiet)
    return 1 if any(r["veredito"] == ATRASADO for r in linhas) else 0


if __name__ == "__main__":
    sys.exit(main())
