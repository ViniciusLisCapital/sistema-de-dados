"""
Parser da planilha de resultados do Questionario Pre-Copom (QPC) -> linhas longas.

Usado por `expc_qpc.py`. Separado para o parser poder ser exercitado sem banco.

## A aba e reconhecida pelo TITULO, nunca pelo numero

O numero da questao anda entre edicoes: a "Questao 6" e mercado de trabalho na 260a e
fiscal na 281a, e o hiato ja foi 6a, 6, 7 e 7a. Nas edicoes de 2021 o titulo da
aba e o da questao-mae ("3 - Informe suas projecoes para o IPCA...") e a subquestao
vem na linha 2. Por isso `classificar()` le o texto das tres primeiras linhas.

## Blocos lidos (os que o usuario avaliou em 2026-09-29)

    bloco                      forma          o que e
    copom_decisao              contagem       fara / deveria fazer, por faixa em p.b., 1 ou 3 reunioes
    vies_ipca, vies_pib        fracao         risco de baixa / equilibrado / de alta, por ano
    ambiente_externo           fracao         menos favoravel / sem mudanca / mais favoravel desde o ultimo Copom
    situacao_fiscal            fracao         piorou / sem mudanca / melhorou desde o ultimo Copom
    ipca_curto_prazo           percentis      IPCA, servicos subjacentes e media dos nucleos, var. mensal
    pib_trimestral             percentis      PIB trimestral, YoY e QoQ dessazonalizado
    hiato                      percentis      hiato do produto, 2-3 trimestres
    ipca_horizonte_relevante   percentis      IPCA 4 tri no horizonte relevante + probabilidade de
                                              desvio em relacao a PROPRIA projecao (so desde a 281a)
    juro_real_neutro           percentis      juro real neutro, curto prazo / 2 anos / 5 anos
    pib_potencial              percentis      crescimento do PIB potencial, mesmos horizontes
    nairu                      percentis      desemprego que nao acelera a inflacao (desde a 271a)

Os tres ultimos saem da MESMA aba, semestral (jun e dez desde a 251a; antes, 240a e 243a),
e por isso `classificar()` devolve para ela o tipo de aba `estruturais`, nao um bloco: e
`_estruturais()` que reparte as linhas nos tres blocos pelo subtitulo de cada tabela.

Fora de proposito: projecoes anuais (3a, 4a, 5a/b, 6a), bandeira, credito, perguntas
pontuais (El Nino, ICMS, Oriente Medio) e o "em que trimestre fecha o hiato" (sai em 2022).

## Tres formatos antigos que o parser absorve

- **Questao 1 ate a 254a**: uma reuniao so, contagem e % na mesma linha
  (`[faixa, fara_n, deveria_n, fara_%, deveria_%]`), sem rotulo "Copom NNN" -- a
  reuniao-alvo e a propria edicao. Da 255a em diante: 3 reunioes, % num bloco abaixo.
- **Vies 240a-243a**: duas linhas por ano, `Copom <anterior>` e `Copom <atual>`. So a
  da edicao atual e lida -- a outra ja esta no arquivo dela.
- **Situacao fiscal a partir da 247a**: a aba e a tabela de evolucao inteira, uma linha
  por reuniao. So a linha da edicao e lida, pelo mesmo motivo.

E um formato que ele NAO absorve, de proposito: o curto prazo de 238a-241a (medianas
por componente, sem percentis, com cambio/Selic/Brent misturados como colunas).
`ipca_curto_prazo` comeca na 254a; entre 242a e 253a a pergunta nao existe.
"""

from __future__ import annotations

import datetime as dt
import logging
import re
import unicodedata

import openpyxl

logger = logging.getLogger(__name__)

_MES_ABREV = {"jan": 1, "fev": 2, "mar": 3, "abr": 4, "mai": 5, "jun": 6,
              "jul": 7, "ago": 8, "set": 9, "out": 10, "nov": 11, "dez": 12}

_STAT = {"percentil 75": "p75", "percentil 25": "p25", "mediana": "mediana",
         "média": "media", "media": "media"}

def _slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", s).strip("_")


def _linhas(ws) -> list[list]:
    """Linhas nao vazias, sem celulas vazias, strings com espacos colapsados."""
    out = []
    for row in ws.iter_rows(values_only=True):
        cel = []
        for v in row:
            if v is None:
                continue
            if isinstance(v, str):
                v = re.sub(r"\s+", " ", v).strip()
                if not v:
                    continue
            cel.append(v)
        if cel:
            out.append(cel)
    return out


def _num(v) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _stat(v) -> str | None:
    """Rotulo de linha de estatistica, por IGUALDADE: 'Média dos núcleos' e subtitulo, nao 'Média'."""
    if not isinstance(v, str):
        return None
    t = v.lower().strip()
    if re.match(r"n[º°.]\s*(de\s*)?resp", t):
        return "n_respostas"
    return _STAT.get(t)


def classificar(ws) -> str | None:
    # O Indice repete os titulos de todas as questoes nas primeiras linhas.
    if not ws.title.lower().startswith("quest"):
        return None
    t =" ".join(str(c) for r in _linhas(ws)[:3] for c in r if isinstance(c, str)).lower()
    if "copom fará" in t:
        return "copom_decisao"
    if "juros real neutra" in t:
        # 243a: "sua estimativa ... mudou desde o QPC de agosto?" -- pergunta de uma vez so
        return None if "mudou" in t else "estruturais"
    if "horizonte relevante" in t:
        return "ipca_horizonte_relevante"
    if "viés" in t:
        if "econom" in t:            # vies do PIB/inflacao de China-EUA-Europa (2022)
            return None
        if "para o ipca" in t:
            return "vies_ipca"
        if "para o pib" in t:
            return "vies_pib"
        return None
    if "ambiente externo desde" in t:
        return "ambiente_externo"
    if "situação fiscal desde" in t:
        return "situacao_fiscal"
    if "trimestrais do pib" in t:
        return "pib_trimestral"
    if "hiato" in t and "fechamento" not in t:
        return "hiato"
    if "curto prazo" in t and "juros" not in t:
        return "ipca_curto_prazo"
    return None


# ------------------------------------------------------------------ periodos

def periodo(rotulo: str) -> tuple[str, dt.date]:
    """Rotulo publicado -> (referencia, ref_date = 1o dia do periodo)."""
    s = str(rotulo).strip()
    m = re.fullmatch(r"([A-Za-zç]{3})/(\d{2})", s)
    if m and m.group(1).lower() in _MES_ABREV:
        a, mes = 2000 + int(m.group(2)), _MES_ABREV[m.group(1).lower()]
        return f"{a}-{mes:02d}", dt.date(a, mes, 1)
    m = re.fullmatch(r"(\d{2})T([1-4])", s)
    if m:
        a, q = 2000 + int(m.group(1)), int(m.group(2))
        return f"{a}T{q}", dt.date(a, 3 * q - 2, 1)
    m = re.fullmatch(r"([1-4])\s*[º°o]?\s*tri\.?\s*(\d{4})", s, flags=re.I)
    if m:
        a, q = int(m.group(2)), int(m.group(1))
        return f"{a}T{q}", dt.date(a, 3 * q - 2, 1)
    m = re.search(r"(\d{4})$", s)
    if m:
        a = int(m.group(1))
        return str(a), dt.date(a, 1, 1)
    raise ValueError(f"periodo nao reconhecido: {rotulo!r}")


def _linha(n, bloco, variavel, referencia, categoria, estatistica, valor, ref_date):
    return {"nro_reuniao": n, "bloco": bloco, "variavel": variavel, "referencia": referencia,
            "categoria": categoria, "estatistica": estatistica, "valor": float(valor),
            "ref_date": ref_date}


# ------------------------------------------------------------------ questao 1

_RE_REUNIAO = re.compile(r"Copom (\d+) \((\w{3})(?:/(\d{2}))?\)")


def _copom_decisao(linhas, n, data_reuniao: dt.date) -> list[dict]:
    reunioes: list[tuple[int, dt.date]] = []
    for r in linhas:
        for c in r:
            m = _RE_REUNIAO.fullmatch(str(c))
            if m and int(m.group(1)) not in [x[0] for x in reunioes]:
                mes = _MES_ABREV[m.group(2).lower()]
                if m.group(3):
                    a = 2000 + int(m.group(3))
                else:
                    # 255a-2xx: "Copom 256 (Ago)", sem ano. A reuniao-alvo nunca esta mais
                    # de um ano a frente, entao um mes antes do da edicao e do ano seguinte.
                    a = data_reuniao.year + (1 if mes < data_reuniao.month else 0)
                reunioes.append((int(m.group(1)), dt.date(a, mes, 1)))
    antigo = not reunioes
    if antigo:
        reunioes = [(n, data_reuniao.replace(day=1))]
    if reunioes[0][0] != n:
        raise ValueError(f"questao 1: primeira reuniao-alvo e {reunioes[0][0]}, esperado {n}")
    k = len(reunioes)

    blocos: list[list[list]] = []        # [contagens, percentuais]
    atual: list[list] | None = None
    for r in linhas:
        if _num(r[0]):
            if atual is None:
                atual = []
                blocos.append(atual)
            atual.append(r)
        else:
            atual = None
    if antigo:
        if len(blocos) != 1 or any(len(r) != 5 for r in blocos[0]):
            raise ValueError("questao 1 (formato antigo): esperado um bloco de 5 colunas")
        cont = [[r[0], r[1], r[2]] for r in blocos[0]]
        pct = [[r[0], r[3], r[4]] for r in blocos[0]]
    else:
        if len(blocos) != 2 or any(len(r) != 1 + 2 * k for b in blocos for r in b):
            raise ValueError(f"questao 1: esperados 2 blocos de {1 + 2 * k} colunas")
        cont, pct = blocos

    out = []
    for j, (reuniao, ref) in enumerate(reunioes):
        for lado, off in (("fara", 1), ("deveria", 2)):
            col = 2 * j + off
            total = sum(r[col] for r in cont)
            # O % publicado e conferido contra a contagem, e a divergencia AVISA em vez de
            # parar: vem arredondado a 2 casas em edicoes de 2021-2022, e na 240a e 241a o
            # "deveria" foi dividido por uma base diferente da soma das contagens (102
            # respostas somadas, % que fecha em 100). A contagem e o dado primario e e ela
            # que fica.
            dif = max((abs(rc[col] / total - rp[col]) for rc, rp in zip(cont, pct)),
                      default=0) if total else 0
            if dif > 0.005 + 1e-9:
                logger.warning("QPC %d, questao 1: %% publicado de R%d %s difere da contagem "
                               "em ate %.3f (soma das contagens %d)", n, reuniao, lado, dif, total)
            for rc in cont:
                out.append(_linha(n, "copom_decisao", lado, f"R{reuniao}", str(int(rc[0])),
                                  "respostas", rc[col], ref))
    return out


# ------------------------------------------------------------------ fracoes

def _variavel_categorica(bloco: str, rotulo: str) -> tuple[str, str, dt.date | None]:
    if bloco in ("vies_ipca", "vies_pib"):
        ref, d = periodo(rotulo)
        return bloco.split("_")[1], ref, d
    return bloco, "", None


def _categorico(linhas, n, bloco) -> list[dict]:
    i_hdr = next((i for i, r in enumerate(linhas)
                  if all(isinstance(c, str) for c in r) and "respostas" in r[-1].lower()), None)
    if i_hdr is None:
        raise ValueError(f"{bloco}: cabecalho de categorias nao encontrado")
    hdr = linhas[i_hdr][:-1]
    evolucao = hdr[0].lower() == "copom"
    cats = [_slug(c) for c in (hdr[1:] if evolucao else hdr)]
    out, rotulo = [], None
    for r in linhas[i_hdr + 1:]:
        if not _num(r[-1]):
            continue
        texto = [c for c in r if isinstance(c, str)]
        vals = [c for c in r if _num(c)]
        if evolucao:
            # "268 (jan/25)" ou "Copom 242", conforme a edicao
            m = re.search(r"(\d+)", texto[0] if texto else "")
            if not m or int(m.group(1)) != n:
                continue
            rot = bloco
        else:
            copom = [c for c in texto if re.fullmatch(r"Copom \d+", c)]
            outros = [c for c in texto if c not in copom]
            if outros:
                rotulo = outros[0]
            if copom and copom[0] != f"Copom {n}":
                continue
            rot = rotulo
        if len(vals) != len(cats) + 1:
            raise ValueError(f"{bloco}: {len(vals)} valores para {len(cats)} categorias em {r}")
        variavel, ref, d = _variavel_categorica(bloco, rot)
        soma = sum(vals[:-1])
        if abs(soma - 1) > 0.005:
            raise ValueError(f"{bloco} {rot}: fracoes somam {soma:.4f}")
        for c, v in zip(cats, vals[:-1]):
            out.append(_linha(n, bloco, variavel, ref, c, "fracao", v, d))
        out.append(_linha(n, bloco, variavel, ref, "", "n_respostas", vals[-1], d))
    if not out:
        raise ValueError(f"{bloco}: nenhuma linha da edicao {n}")
    return out


# ------------------------------------------------------------------ percentis

def _grupos_percentis(linhas):
    """Gera (subtitulo, cabecalho, {estatistica: valores}) para cada tabela de percentis."""
    strings: list[list] = []
    grupo = None
    for r in linhas[1:]:
        st = _stat(r[0])
        if st:
            if grupo is None:
                hdr = strings[-1] if strings else []
                sub = strings[-2][0] if len(strings) >= 2 else ""
                grupo = (sub, hdr, {})
            grupo[2][st] = r[1:]
            continue
        if grupo is not None:
            yield grupo
            grupo, strings = None, []
        if all(isinstance(c, str) for c in r):
            strings.append(r)
    if grupo is not None:
        yield grupo


_CURTO = [("ipca", "ipca"), ("serviços subjacentes", "servicos_subjacentes"),
          ("média dos núcleos", "media_nucleos")]


def _percentis(linhas, n, bloco) -> list[dict]:
    out = []
    for sub, hdr, stats in _grupos_percentis(linhas):
        if any(len(v) != len(hdr) for v in stats.values()):
            raise ValueError(f"{bloco} '{sub}': {len(hdr)} colunas e valores desalinhados")
        if not {"p25", "mediana", "p75"} <= set(stats):
            raise ValueError(f"{bloco} '{sub}': faltam percentis ({sorted(stats)})")
        s = sub.lower()
        if bloco == "ipca_curto_prazo":
            variavel = next((v for k, v in _CURTO if s.startswith(k)), None)
            if variavel is None:
                raise ValueError(f"ipca_curto_prazo: subtitulo nao reconhecido {sub!r}")
        elif bloco == "pib_trimestral":
            variavel = "qoq_sa" if "qoqsa" in s else "yoy" if "yoy" in s else None
            if variavel is None:
                raise ValueError(f"pib_trimestral: subtitulo nao reconhecido {sub!r}")
        elif bloco == "hiato":
            variavel = "hiato"
        else:                                   # ipca_horizonte_relevante
            variavel = None
        ref0 = periodo(hdr[0]) if bloco == "ipca_horizonte_relevante" else None
        for j, col in enumerate(hdr):
            if ref0 is not None:
                ref, d = ref0
                if j == 0:
                    var, cat = "ipca_4t", ""
                else:
                    var = "prob_desvio"
                    c = col.lower()
                    cat = ("abaixo_0_5pp" if c.startswith("inferior") else
                           "acima_0_5pp" if c.startswith("superior") else
                           "entre_0_5pp" if c.startswith("entre") else None)
                    if cat is None:
                        raise ValueError(f"horizonte relevante: faixa nao reconhecida {col!r}")
            else:
                (ref, d), var, cat = periodo(col), variavel, ""
            for st, vals in stats.items():
                if _num(vals[j]):
                    out.append(_linha(n, bloco, var, ref, cat, st, vals[j], d))
            p25, med, p75 = (stats[k][j] for k in ("p25", "mediana", "p75"))
            if all(_num(x) for x in (p25, med, p75)) and not p25 - 1e-9 <= med <= p75 + 1e-9:
                raise ValueError(f"{bloco} {var} {ref}: percentis fora de ordem {p25}/{med}/{p75}")
    return out


def _ipca_curto_prazo(linhas, n, bloco) -> list[dict]:
    # Formato de 238a-241a (medianas por componente, sem percentis): fora, ver docstring.
    if not any(_stat(r[0]) in ("p25", "p75") for r in linhas):
        return []
    return _percentis(linhas, n, bloco)


_ESTRUTURAIS = [("taxa de juros real neutra", "juro_real_neutro"),
                ("taxa de crescimento do pib potencial", "pib_potencial"),
                ("nairu", "nairu")]
_HORIZONTE = {"curto prazo": "curto_prazo", "2 anos": "2a", "5 anos": "5a"}


def _estruturais(linhas, n, _tipo) -> list[dict]:
    """Juro real neutro, PIB potencial e Nairu: tres blocos numa aba so.

    O horizonte nao e um periodo do calendario, entao `referencia` e o rotulo dele
    (curto_prazo | 2a | 5a) e `ref_date` fica nulo. As tabelas de "Evolucao" da mesma
    aba nao tem linha de estatistica e nao sao lidas -- cada edicao ja esta no arquivo dela.
    """
    out = []
    for sub, hdr, stats in _grupos_percentis(linhas):
        s = sub.lower()
        bloco = next((b for k, b in _ESTRUTURAIS if s.startswith(k)), None)
        if bloco is None:
            raise ValueError(f"estruturais: subtitulo nao reconhecido {sub!r}")
        if any(len(v) != len(hdr) for v in stats.values()):
            raise ValueError(f"{bloco}: {len(hdr)} colunas e valores desalinhados")
        for j, col in enumerate(hdr):
            ref = _HORIZONTE.get(str(col).lower())
            if ref is None:
                raise ValueError(f"{bloco}: horizonte nao reconhecido {col!r}")
            for st, vals in stats.items():
                if _num(vals[j]):
                    out.append(_linha(n, bloco, bloco, ref, "", st, vals[j], None))
            p25, med, p75 = (stats[k][j] for k in ("p25", "mediana", "p75"))
            if not p25 - 1e-9 <= med <= p75 + 1e-9:
                raise ValueError(f"{bloco} {ref}: percentis fora de ordem {p25}/{med}/{p75}")
    if not any(r["bloco"] == "juro_real_neutro" for r in out):
        raise ValueError("estruturais: aba sem a tabela do juro real neutro")
    return out


_PARSERS = {
    "estruturais": _estruturais,
    "vies_ipca": _categorico, "vies_pib": _categorico,
    "ambiente_externo": _categorico, "situacao_fiscal": _categorico,
    "ipca_curto_prazo": _ipca_curto_prazo,
    "pib_trimestral": _percentis, "hiato": _percentis, "ipca_horizonte_relevante": _percentis,
}


def parse(wb: openpyxl.Workbook, n: int, data_reuniao: dt.date) -> list[dict]:
    """Todas as linhas dos blocos lidos numa edicao. Levanta se um tipo de aba aparecer duas vezes."""
    vistos: dict[str, str] = {}
    out: list[dict] = []
    for ws in wb.worksheets:
        bloco = classificar(ws)
        if bloco is None:
            continue
        if bloco in vistos:
            raise ValueError(f"edicao {n}: bloco {bloco} em duas abas ({vistos[bloco]}, {ws.title})")
        vistos[bloco] = ws.title
        linhas = _linhas(ws)
        if bloco == "copom_decisao":
            out += _copom_decisao(linhas, n, data_reuniao)
        else:
            out += _PARSERS[bloco](linhas, n, bloco)
    return out
