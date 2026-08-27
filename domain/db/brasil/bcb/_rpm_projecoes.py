"""
Projecoes de inflacao publicadas no Relatorio de Politica Monetaria (RPM, ex-Relatorio de Inflacao).

Contrapartida do `_copom_texto.py`: o comunicado de decisao publica 2 ou 3 numeros; o relatorio,
que sai 7 a 28 dias depois da mesma reuniao, publica o CAMINHO TRIMESTRAL CONTIGUO inteiro. E o que
torna a leitura de horizonte relevante uma serie continua desde 1999 -- os comunicados so a dao de
2020 em diante.

Fonte: `connectors.bcb_rpm.edicoes()` (109 edicoes, 1999-06 a 2026-06, sem buraco) + o PDF de cada
uma. O texto das paginas de projecao fica em `repository/monetary_policy/raw_md/
relatorio_politica_monetaria/` antes do parsing, e o parsing le de la -- carga reproduzivel offline e
trilha de auditoria, mesmo padrao dos comunicados.

Levantamento da fonte, com os formatos por era: `relatorio_politica_monetaria.md` nesta pasta.

## Duas extracoes por pagina, de proposito

O relatorio e de 2 colunas, e as duas extracoes possiveis perdem casos diferentes:

- pagina inteira: uma linha de tabela na coluna DIREITA sai com a prosa da esquerda colada na
  frente, e qualquer regex ancorado no inicio da linha a perde;
- dividida na calha: uma tabela LARGA, que atravessa o centro (todas as de 2025-2026), e cortada
  no meio e perde metade das colunas.

Entao o `.md` guarda as duas variantes e o parser varre as duas, deduplicando por (periodo, cenario).

## A coluna central muda de lugar

A tabela do leque tem 7 numeros por linha. Ate ~2016 sao 6 limites e a projecao central no FIM; de
~2017 em diante sao 3 limites, a central, e 3 limites -- central no MEIO. Ler a posicao errada nao
levanta excecao nenhuma: devolve um limite do leque como se fosse a projecao (no RI de jun/2019
daria 3,4% e 4,2% no lugar de 3,0% e 3,6%, e a prosa da propria edicao diz 3,0 e 3,6).

`_convencao()` decide por SIMETRIA do leque em torno do candidato, e decide UMA VEZ POR TABELA, nao
linha a linha: por linha as margens sao de 0,05 contra 0,15 p.p. e um arredondamento inverte a
escolha; pela tabela inteira a separacao medida no corpus e de 0,00-0,03 contra 0,15-0,60.
"""

from __future__ import annotations

import datetime as dt
import pathlib
import re
import unicodedata
from dataclasses import dataclass, field

from connectors import bcb_rpm

_RAIZ = pathlib.Path(__file__).resolve().parents[4]
DIRETORIO_PDF = _RAIZ / "repository" / "monetary_policy" / "raw_pdf" / "relatorio_politica_monetaria"
DIRETORIO_MD = _RAIZ / "repository" / "monetary_policy" / "raw_md" / "relatorio_politica_monetaria"

# Palavras que marcam uma pagina como candidata a conter tabela de projecao.
_CHAVE_PAGINA = re.compile(
    r"proje[cç][õo]es de infla[cç][ãa]o|previs[ãa]o d[ae] infla[cç][ãa]o|leque de infla[cç][ãa]o"
    r"|proje[cç][ãa]o d[ae] infla[cç][ãa]o|cen[áa]rio de refer[êe]ncia|cen[áa]rio de mercado"
    r"|intervalo de (?:confian|probabilidade)",
    re.I,
)

# Linha do leque: ano, trimestre, 6 limites e 1 central -- em ordem que depende da era, ver
# _convencao(). O separador ano/trimestre varia entre as edicoes e nao ha nenhum aviso quando muda:
# espaco ("2000 2"), NADA ("20102"), dois-pontos ("2002:3"); e o trimestre e arabe ate ~2016 e
# romano depois ("2019 II").
_LINHA_LEQUE = re.compile(
    r"^((?:19|20)\d{2})\s*[:./-]?\s*(IV|III|II|I|[1-4])\s+"
    r"((?:-?\d+,\d{1,2}\s+){6})(-?\d+,\d{1,2})(?:\s|$)"
)

_ROMANO = {"I": 1, "II": 2, "III": 3, "IV": 4}


def sem_acento(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def num(s: str) -> float:
    return float(s.replace(",", "."))


# --------------------------------------------------------------------------- estruturas


@dataclass(frozen=True)
class Periodo:
    ano: int
    trimestre: int

    @property
    def norm(self) -> str:
        return f"{self.ano}Q{self.trimestre}"

    @property
    def indice(self) -> int:
        """Trimestre absoluto, para ordenar e medir distancia."""
        return self.ano * 4 + self.trimestre

    @property
    def primeiro_mes(self) -> dt.date:
        return dt.date(self.ano, 3 * (self.trimestre - 1) + 1, 1)


@dataclass
class Projecao:
    indice: str  # ipca | ipca_livres | ipca_administrados
    cenario: str  # juros_esperado | juros_constante
    periodo: Periodo
    valor: float
    input_juros: str | None  # focus | di_swaps | constante
    cenario_publicado: str | None
    fonte: str = "tabela"


@dataclass
class EdicaoParseada:
    ano_mes: str
    vintage: dt.date
    nro_reuniao: int | None = None
    data_reuniao: str | None = None
    projecoes: list[Projecao] = field(default_factory=list)
    convencoes: list[str] = field(default_factory=list)  # 'fim'/'meio' por tabela lida
    avisos: list[str] = field(default_factory=list)

    @property
    def periodos(self) -> list[Periodo]:
        return sorted({p.periodo for p in self.projecoes}, key=lambda p: p.indice)


# --------------------------------------------------------------------------- sincronizacao


def _paginas_candidatas(caminho_pdf: pathlib.Path) -> list[tuple[int, str, str | None]]:
    """(numero, texto da pagina inteira, texto dividido por coluna) das paginas de projecao."""
    import pdfplumber

    out: list[tuple[int, str, str | None]] = []
    with pdfplumber.open(caminho_pdf) as pdf:
        for i, pg in enumerate(pdf.pages):
            cheio = pg.extract_text() or ""
            if not _CHAVE_PAGINA.search(cheio):
                continue
            out.append((i + 1, cheio, _texto_por_coluna(pg)))
    return out


def _texto_por_coluna(pg, margem: float = 12.0) -> str | None:
    """Texto respeitando as 2 colunas, ou None se a pagina nao for de 2 colunas.

    Duas colunas = quase nenhuma palavra atravessa a calha central E os dois lados tem volume
    comparavel de texto. Uma tabela larga atravessa a calha, entao a pagina que a contem cai no
    caso None -- e o motivo de guardar tambem o texto da pagina inteira.
    """
    palavras = pg.extract_words()
    if not palavras:
        return None
    meio = (pg.bbox[0] + pg.bbox[2]) / 2
    cruzam = [w for w in palavras if w["x0"] < meio - margem and w["x1"] > meio + margem]
    esq = [w for w in palavras if w["x1"] <= meio]
    dire = [w for w in palavras if w["x0"] >= meio]
    if len(cruzam) > max(2, 0.02 * len(palavras)):
        return None
    if min(len(esq), len(dire)) < 0.25 * len(palavras):
        return None
    partes = []
    for x0, x1 in ((pg.bbox[0], meio), (meio, pg.bbox[2])):
        partes.append(pg.crop((x0, pg.bbox[1], x1, pg.bbox[3])).extract_text() or "")
    return "\n".join(p for p in partes if p.strip())


def sincronizar(*, sobrescrever: bool = False, verbose: bool = True) -> dict:
    """Baixa os PDFs que faltam e grava as paginas de projecao em `raw_md/`.

    Guarda so as paginas candidatas, nao o relatorio inteiro: sao ~10 kB por edicao em vez de
    ~300 kB, e o resto do relatorio nao alimenta tabela nenhuma.
    """
    DIRETORIO_PDF.mkdir(parents=True, exist_ok=True)
    DIRETORIO_MD.mkdir(parents=True, exist_ok=True)
    r = {"baixados": [], "extraidos": [], "existentes": [], "erros": []}

    for ed in bcb_rpm.edicoes():
        pdf = DIRETORIO_PDF / ed.nome_arquivo
        md = DIRETORIO_MD / (pdf.stem + ".md")
        if md.exists() and md.stat().st_size > 500 and not sobrescrever:
            r["existentes"].append(ed.ano_mes)
            continue
        try:
            if not pdf.exists() or pdf.stat().st_size < 10_000:
                pdf.write_bytes(bcb_rpm.baixar_pdf(ed))
                r["baixados"].append(ed.ano_mes)
            md.write_text(_montar_md(ed, pdf), encoding="utf-8")
            r["extraidos"].append(ed.ano_mes)
            if verbose:
                print(f"  {ed.ano_mes}: {md.stat().st_size / 1000:.0f} kB", flush=True)
        except Exception as err:  # noqa: BLE001
            r["erros"].append((ed.ano_mes, str(err)))
    return r


def _montar_md(ed: bcb_rpm.Edicao, caminho_pdf: pathlib.Path) -> str:
    partes = [
        f"# RPM {ed.ano_mes}",
        f"Publicado em: {ed.vintage:%Y-%m-%d}",
        f"Origem: {ed.url_pdf}",
        "",
    ]
    for n, cheio, colunas in _paginas_candidatas(caminho_pdf):
        # A palavra-chave marca a pagina como candidata, mas o que justifica guardar e ter LINHA de
        # tabela. Sem este segundo filtro entram as ~20 paginas por edicao que so mencionam
        # "projecoes de inflacao" na prosa, e o raw_md do corpus vai de ~1 MB para 7 MB.
        if not _tem_tabela(cheio) and not (colunas and _tem_tabela(colunas)):
            continue
        partes.append(f"\n<<<PAG {n} INTEIRA>>>\n{cheio}")
        if colunas:
            partes.append(f"\n<<<PAG {n} COLUNAS>>>\n{colunas}")
    return "\n".join(partes)


def _tem_tabela(texto: str) -> bool:
    """A pagina tem linha de tabela de projecao, em qualquer dos tres formatos?"""
    if len(_linhas_leque(texto)) >= _MIN_LINHAS_TABELA:
        return True
    if len(_linhas_revisao(texto)) >= _MIN_LINHAS_TABELA:
        return True
    return bool(_parse_matriz(texto)[0])


def arquivos(diretorio: pathlib.Path = DIRETORIO_MD) -> list[pathlib.Path]:
    return sorted(diretorio.glob("rpm_*.md"))


# --------------------------------------------------------------------------- parsing


def _convencao(linhas: list[list[float]]) -> tuple[str, float]:
    """('fim'|'meio', erro medio) -- onde esta a central nas linhas de UMA tabela.

    O leque publicado e simetrico em torno da projecao central, entao a posicao certa e a que
    minimiza |media(limite inferior, limite superior) - candidato| somada na tabela inteira.
    """

    def erro(vals: list[float], pos: str) -> float:
        central = vals[6] if pos == "fim" else vals[3]
        limites = vals[0:6] if pos == "fim" else vals[0:3] + vals[4:7]
        return abs((min(limites) + max(limites)) / 2 - central)

    e_fim = sum(erro(v, "fim") for v in linhas) / len(linhas)
    e_meio = sum(erro(v, "meio") for v in linhas) / len(linhas)
    return ("fim", e_fim) if e_fim <= e_meio else ("meio", e_meio)


def _linhas_leque(texto: str) -> list[tuple[Periodo, list[float], int]]:
    """(periodo, os 7 numeros, indice da linha no texto) de toda linha de leque do texto."""
    out = []
    for i, ln in enumerate(texto.split("\n")):
        m = _LINHA_LEQUE.match(ln.strip())
        if not m:
            continue
        tri = m.group(2)
        tri = _ROMANO[tri] if tri in _ROMANO else int(tri)
        vals = [num(x) for x in m.group(3).split()] + [num(m.group(4))]
        out.append((Periodo(int(m.group(1)), tri), vals, i))
    return out


def _segmentar(linhas: list[tuple[Periodo, list[float], int]]) -> list[list[tuple]]:
    """Quebra a lista de linhas em tabelas.

    Uma tabela e cronologica; quando o periodo nao avanca, comecou outra. E o que separa a tabela
    do cenario de juros constantes da do cenario de mercado, que na mesma pagina repetem os mesmos
    trimestres.
    """
    tabelas: list[list[tuple]] = []
    atual: list[tuple] = []
    for item in linhas:
        if atual and item[0].indice <= atual[-1][0].indice:
            tabelas.append(atual)
            atual = []
        atual.append(item)
    if atual:
        tabelas.append(atual)
    return tabelas


# --------------------------------------------------------------------------- cenario


# Como o relatorio descreve o condicionamento de juros de cada tabela, por ordem de
# especificidade. Levantado varrendo as legendas das 109 edicoes -- ver
# `relatorio_politica_monetaria.md`. Classifica pelo CONDICIONAMENTO, nunca por "referencia":
# ate ~2020 "cenario de referencia" era o de juros CONSTANTES, de 2021 em diante e o de juros da
# Focus, ou seja o rotulo trocou de significado (mesma armadilha documentada em
# `copom_comunicados.md`).
_ROTULOS_RPM: list[tuple[str, str]] = [
    ("juros_constante", r"juros (?:fixos|constantes?)"),
    ("juros_constante", r"selic constante"),
    # "IPCA com juros de 17,5% a.a." (1999-2005): nomear o nivel E dizer que e constante
    ("juros_constante", r"juros de \d{1,2}(?:,\d{1,2})?%"),
    ("juros_decrescente", r"juros decrescentes"),
    ("juros_esperado", r"expectativas de mercado"),
    ("juros_esperado", r"juros de mercado"),
    # a legenda quebra em duas linhas e a prosa da coluna vizinha entra no meio, entao "expectativas
    # de mercado" nem sempre fica contiguo -- estes sao os pedacos que ficam, medidos no corpus
    ("juros_esperado", r"mercado para as (?:taxas|trajet[óo]rias)"),
    ("juros_esperado", r"esperad\w+ pelo mercado"),
    ("juros_esperado", r"expectativas de juros"),
    # a Gerin (depois Gerin/Depep) era quem rodava a pesquisa de expectativas; "Fonte: Gerin" sob a
    # tabela e o unico marcador legivel do cenario de mercado em algumas edicoes de 2003-2004
    ("juros_esperado", r"fonte:\s*gerin"),
    ("juros_esperado", r"pesquisa focus"),
    ("juros_esperado", r"cen[áa]rio de mercado"),
    ("juros_esperado", r"trajet[óo]ria (?:de|das) (?:taxas? de )?juros.{0,40}focus"),
    # "Cenario com Selic Focus e cambio PPC" (2022-2024). Padrao amplo de proposito e seguro aqui:
    # a palavra Focus so aparece no relatorio se referindo a pesquisa, e a escolha e pela legenda
    # MAIS PROXIMA da tabela, entao um "juros constantes" mais perto continua ganhando.
    ("juros_esperado", r"\bfocus\b"),
]

# De onde veio a trajetoria esperada. O RI dos anos 2000 usava a curva de futuros e swaps de DI
# ("as taxas medias embutidas nos contratos futuros e de swaps"); mais tarde passou a mediana da
# Focus. Sao coisas diferentes -- preco com dinheiro em risco contra estimativa de economista -- e
# por isso viram valores distintos de `input_juros` em vez de um so rotulo "mercado".
_INPUT_JUROS = [
    ("di_swaps", r"futuros|swaps?"),
    ("focus", r"focus|gerin|pesquisa"),
]

_LINHAS_DE_LEGENDA = 16  # quantas linhas antes da tabela procurar a legenda; medido no corpus


# Como classificar o cenario de uma tabela: isolar a LEGENDA e olhar o CONJUNTO de qualificadores
# que ela usa. Regra de conjunto e nao de posicao porque a frase muda de ordem e de marcador entre
# eras -- "taxa de cambio e juros constantes", "Selic e cambio da pesquisa Focus", "taxa de cambio
# constante e expectativas de mercado para a taxa de juros" -- e ler "o qualificador depois da
# palavra Selic" erra sempre que a ordem inverte.
#
# As edicoes de 2016-2020 publicam a grade 2x2 de {juros constantes, juros de mercado} x {cambio
# constante, cambio de mercado}: quatro tabelas com os MESMOS trimestres. As duas PURAS (tudo
# constante, tudo de mercado) sao as que tem contrapartida no vocabulario da coluna `cenario`, que
# classifica so o juro; as duas MISTAS cairiam na mesma chave de uma pura e a sobrescreveriam. Uma
# legenda que usa qualificador dos DOIS tipos e, por construcao, uma das mistas.
_QUALIFICADORES = {
    "constante": ("constante", "constantes", "fixo", "fixos"),
    "esperado": ("mercado", "focus", "futuros", "swaps", "gerin"),
    "decrescente": ("decrescente", "decrescentes"),
}

# Inicio de legenda de tabela ou grafico de projecao. A legenda pode continuar na linha seguinte.
_INICIO_LEGENDA = re.compile(
    r"^\s*(?:tabela|grafico|quadro)\s*[\d.]*\s*[-]?|^\s*inflacao do ipca"
    r"|^\s*projecao d[ae] inflacao|^\s*ipca com|^\s*cenario\b",
    re.I,
)

_CENARIO_DE = {"constante": "juros_constante", "esperado": "juros_esperado",
               "decrescente": "juros_decrescente"}


def _legenda(linhas: list[str]) -> str | None:
    """A legenda mais proxima da tabela (a ultima do contexto), com a continuacao junto."""
    for i in range(len(linhas) - 1, -1, -1):
        if not _INICIO_LEGENDA.match(sem_acento(linhas[i]).lower()):
            continue
        partes = [linhas[i].strip()]
        for j in (i + 1, i + 2):
            if j >= len(linhas):
                break
            prox = linhas[j].strip()
            if not prox or len(prox) > 70 or not re.search(r"[a-zA-Z]{3}", prox):
                break
            if re.match(r"^(?:19|20)[0-9]{2}|^[0-9,.%\s]+$|^(?:ano|periodo|central|obs|fonte)",
                        sem_acento(prox), re.I):
                break
            partes.append(prox)
        return re.sub(r"\s+", " ", " ".join(partes)).strip()[:120] or None
    return None


def _tipos_na_legenda(legenda_norm: str) -> set[str]:
    return {
        tipo
        for tipo, palavras in _QUALIFICADORES.items()
        if any(re.search(r"\b" + pal, legenda_norm) for pal in palavras)
    }


def _input_de(texto_norm: str) -> str | None:
    """De onde veio a trajetoria esperada, quando o texto diz."""
    for nome, padrao in _INPUT_JUROS:
        if re.search(padrao, texto_norm):
            return nome
    return None


def _classificar(contexto: str) -> tuple[str | None, str | None, str | None]:
    """(cenario, input_juros, rotulo publicado) a partir do texto que antecede a tabela.

    `cenario` None com rotulo comecando em "MISTO" = legenda lida e tabela recusada de proposito;
    None com rotulo None = nao deu para ler a legenda.
    """
    linhas = contexto.splitlines()
    legenda = _legenda(linhas)
    if legenda:
        norm = sem_acento(legenda).lower()
        tipos = _tipos_na_legenda(norm)
        if {"constante", "esperado"} <= tipos:
            return None, None, f"MISTO {legenda}"
        if len(tipos) == 1:
            tipo = tipos.pop()
            inp = "constante" if tipo == "constante" else _input_de(norm)
            return _CENARIO_DE[tipo], inp, legenda

    # Sem legenda legivel, ou legenda sem qualificador ("IPCA com juros de 17,5% a.a."): cai nos
    # padroes do contexto inteiro, vencendo o que estiver MAIS PROXIMO da tabela.
    limpo = sem_acento(contexto).lower()
    achados = [
        (m.start(), nome)
        for nome, padrao in _ROTULOS_RPM
        for m in re.finditer(sem_acento(padrao).lower(), limpo)
    ]
    if not achados:
        return None, None, None
    inicio, cenario = max(achados, key=lambda a: a[0])
    # sem legenda: o rotulo passa a ser a propria linha onde o padrao casou
    idx = limpo[:inicio].count(chr(10))
    bruta = linhas[idx] if idx < len(linhas) else ""
    rotulo = legenda or (re.sub(r"\s+", " ", bruta).strip()[:120] or None)
    if cenario == "juros_constante":
        return cenario, "constante", rotulo
    return cenario, _input_de(limpo), rotulo


# Varias edicoes de 1999-2004 desenham o TITULO das tabelas e graficos com uma fonte de subconjunto
# de encoding proprio: o pdfplumber devolve os codigos de glifo, nao o texto. E um deslocamento fixo
# no ASCII, com o espaco virando `(cid:3)` -- ",QIODomR(cid:3)GR(cid:3),3&$" e "Inflacao do IPCA"
# deslocado 29. A PROSA da mesma pagina usa fonte normal e sai legivel; so os titulos quebram, e o
# titulo e justamente onde vive a identificacao do cenario. Sem isso, ~40% das edicoes ficam sem
# cenario identificado e a carga perde metade das tabelas sem levantar erro nenhum.
_CID = re.compile(r"\(cid:(\d+)\)")

# Palavras que provam que o deslocamento tentado e o certo. O deslocamento NAO e o mesmo em todas as
# edicoes (29 em 2000-2002, outro em 2003-09), e nao ha nada no arquivo que o declare -- entao ele e
# descoberto por busca: tenta cada deslocamento e aceita o que produz uma destas palavras. Se nenhum
# produzir, a linha fica sem decodificar e a tabela entra em `avisos` em vez de ser classificada
# errado.
_PALAVRAS_ANCORA = ("juros", "ipca", "mercado", "constante", "expectativa", "projec", "inflac")


def _aplicar_deslocamento(linha: str, off: int) -> str:
    def desloca(s: str) -> str:
        return "".join(chr(ord(c) + off) if 33 <= ord(c) <= 126 - off else c for c in s)

    # UMA passada: os tokens (cid:N) e o texto solto sofrem o mesmo deslocamento, mas aplicar os
    # dois em sequencia deslocaria o resultado do primeiro de novo ("de 15" saia "de NR").
    out, pos = [], 0
    for m in _CID.finditer(linha):
        out.append(desloca(linha[pos:m.start()]))
        cod = int(m.group(1)) + off
        out.append(chr(cod) if 32 <= cod <= 126 else " ")
        pos = m.end()
    out.append(desloca(linha[pos:]))
    return "".join(out)


def _decodificar_cid(linha: str) -> str | None:
    """Devolve a linha decodificada, ou None se nenhum deslocamento produzir palavra reconhecivel."""
    if "(cid:" not in linha:
        return None
    for off in range(1, 96):
        cand = _aplicar_deslocamento(linha, off)
        baixa = cand.lower()
        if any(k in baixa for k in _PALAVRAS_ANCORA):
            return cand
    return None


def _contexto(corpo: str, linha_idx: int) -> str:
    """As N linhas antes da tabela, MAIS a versao decodificada das que estao na fonte quebrada.

    Acrescenta em vez de substituir: se o deslocamento nao se aplicar a alguma linha, a original
    continua ali e o classificador ve as duas.
    """
    linhas = corpo.splitlines()[max(0, linha_idx - _LINHAS_DE_LEGENDA):linha_idx]
    extra = [d for ln in linhas if (d := _decodificar_cid(ln))]
    return chr(10).join(linhas + extra)


# --------------------------------------------------------------------------- formato revisao


# Terceiro formato, das edicoes de 2021-2024: a tabela compara a edicao ANTERIOR com a atual --
# "Ano | Trim. | Meta | RI de marco | RI de junho | Diferenca (p.p.)", 3 ou 4 numeros por linha
# (a coluna Meta so aparece no 4o trimestre). O valor desta edicao e o PENULTIMO numero; o ultimo e
# a diferenca e o antepenultimo e a projecao da edicao passada -- ler a coluna errada gravaria a
# projecao de tres meses atras com a data de hoje.
#
# A propria linha valida a identificacao: a diferenca publicada tem que ser atual - anterior. Com
# uma casa decimal em cada numero, o arredondamento permite ate 0,1 p.p. de folga.
_LINHA_REVISAO = re.compile(
    r"^((?:19|20)\d{2})\s+(IV|III|II|I)\s+((?:-?\d+,\d{1,2}\s+){2,3})(-?\d+,\d{1,2})(?:\s|$)"
)
_FOLGA_REVISAO = 0.15


def _linhas_revisao(texto: str) -> list[tuple[Periodo, float, int]]:
    """(periodo, projecao DESTA edicao, indice da linha) das linhas do formato de revisao."""
    out = []
    for i, ln in enumerate(texto.splitlines()):
        m = _LINHA_REVISAO.match(ln.strip())
        if not m:
            continue
        vals = [num(x) for x in m.group(3).split()] + [num(m.group(4))]
        dif, atual, anterior = vals[-1], vals[-2], vals[-3]
        if abs(dif - (atual - anterior)) > _FOLGA_REVISAO:
            continue
        out.append((Periodo(int(m.group(1)), _ROMANO[m.group(2)]), atual, i))
    return out


# --------------------------------------------------------------------------- formato matriz


# Formato das edicoes de 2025-2026: uma matriz indice x trimestre, igual a Tabela 1 do comunicado,
# em vez das duas tabelas de leque. Nao tem leque numerico no PDF (virou grafico), entao
# `_convencao()` nao se aplica -- o valor publicado e o unico numero da celula.
_ANOS_MATRIZ = re.compile(r"^\s*((?:19|20)\d{2})(?:\s+((?:19|20)\d{2}))*\s*$")
_CABEC_TRI = re.compile(r"^\s*[ÍI]ndice de pre[çc]os\s+((?:(?:IV|III|II|I)\s*)+)$", re.I)
_LINHA_MATRIZ = re.compile(
    r"^\s*(IPCA(?:\s+Livres|\s+Administrados)?)\s+((?:-?\d+,\d\s+)*-?\d+,\d)\s*$", re.I
)

_INDICE_MATRIZ = {
    "ipca": "ipca",
    "ipca livres": "ipca_livres",
    "ipca administrados": "ipca_administrados",
}


def _parse_matriz(corpo: str) -> tuple[list[tuple[str, Periodo, float]], str | None]:
    """(indice, periodo, valor) da matriz indice x trimestre, e o rotulo do cenario.

    Reconstroi os periodos a partir do PRIMEIRO ano da linha de anos e da sequencia de trimestres
    romanos do cabecalho, andando um trimestre por coluna -- a linha de anos nao esta alinhada
    coluna a coluna com os valores (um ano cobre 1 a 4 colunas), entao alinhar por ela seria
    adivinhar. A sequencia de trimestres, sim, e contigua por construcao.
    """
    linhas = corpo.splitlines()
    out: list[tuple[str, Periodo, float]] = []
    rotulo = None
    for i, ln in enumerate(linhas):
        m = _CABEC_TRI.match(ln)
        if not m:
            continue
        romanos = m.group(1).split()
        # o ano de partida e o primeiro da linha de anos imediatamente acima
        ano0 = None
        for k in range(i - 1, max(-1, i - 4), -1):
            ma = _ANOS_MATRIZ.match(linhas[k])
            if ma:
                ano0 = int(ma.group(1))
                break
        if ano0 is None:
            continue
        periodos = []
        ano, tri = ano0, _ROMANO[romanos[0]]
        for _ in romanos:
            periodos.append(Periodo(ano, tri))
            tri += 1
            if tri > 4:
                ano, tri = ano + 1, 1
        # o rotulo do cenario esta no titulo da tabela, acima da linha de anos
        for k in range(max(0, i - 6), i):
            if re.search(r"proje[çc][õo]es de infla[çc][ãa]o", linhas[k], re.I):
                rotulo = re.sub(r"\s+", " ", linhas[k]).strip()[:80]
        for ln2 in linhas[i + 1 : i + 12]:
            if "Diferen" in ln2:
                continue
            mm = _LINHA_MATRIZ.match(ln2)
            if not mm:
                continue
            nome = _INDICE_MATRIZ.get(re.sub(r"\s+", " ", mm.group(1)).strip().lower())
            vals = [num(x) for x in mm.group(2).split()]
            if nome is None or len(vals) != len(periodos):
                continue
            out.extend((nome, p, v) for p, v in zip(periodos, vals))
    return out, rotulo


# --------------------------------------------------------------------------- parse


_BLOCO = re.compile(r"<<<PAG (\d+) (INTEIRA|COLUNAS)>>>")

_MIN_LINHAS_TABELA = 3  # tabelas reais tem 5+; 1-2 linhas sao rotulos de grafico lidos como tabela


def parse(texto: str, ano_mes: str, vintage: dt.date) -> EdicaoParseada:
    """Le o `.md` de uma edicao e devolve as projecoes que deu para extrair.

    Varre as duas variantes de cada pagina (inteira e por coluna) e deduplica por
    (indice, cenario, periodo): as variantes se sobrepoem de proposito, e a mesma celula lida duas
    vezes tem que dar o mesmo numero -- se der diferente, o aviso registra em vez de escolher uma.
    """
    ed = EdicaoParseada(ano_mes=ano_mes, vintage=vintage)
    vistos: dict[tuple[str, str, str], Projecao] = {}

    partes = _BLOCO.split(texto)

    # --- formato leque (1999-2024). Duas passadas: primeiro coleta TODAS as tabelas da edicao na
    # ordem do documento, so depois classifica -- a segunda passada precisa da ordem para o
    # fallback de `_atribuir_por_ordem()`.
    tabelas: list[dict] = []
    paginas_com_colunas = {int(partes[k]) for k in range(1, len(partes), 3) if partes[k + 1] == "COLUNAS"}
    for k in range(1, len(partes), 3):
        pag, variante, corpo = int(partes[k]), partes[k + 1], partes[k + 2]
        # onde as duas variantes existem, ler as duas contaria a mesma tabela duas vezes na ordem
        if variante == "INTEIRA" and pag in paginas_com_colunas:
            continue
        for tab in _segmentar(_linhas_leque(corpo)):
            if len(tab) < _MIN_LINHAS_TABELA:
                continue
            cenario, inp, rotulo = _classificar(_contexto(corpo, tab[0][2]))
            tabelas.append({
                "pagina": pag, "linhas": tab, "cenario": cenario,
                "input_juros": inp, "rotulo": rotulo,
                "faixa": f"{tab[0][0].norm}..{tab[-1][0].norm}",
            })

    _atribuir_por_ordem(tabelas, ed)
    _desempatar(tabelas, ed)

    for t in tabelas:
        if t["cenario"] is None:
            motivo = t["rotulo"] if (t["rotulo"] or "").startswith("MISTO") else "sem cenario identificado"
            ed.avisos.append(f"tabela {t['faixa']} (pag {t['pagina']}) {motivo}")
            continue
        pos, _ = _convencao([v for _, v, _ in t["linhas"]])
        ed.convencoes.append(pos)
        for periodo, vals, _ in t["linhas"]:
            _guardar(vistos, ed, Projecao(
                indice="ipca", cenario=t["cenario"], periodo=periodo,
                valor=vals[6] if pos == "fim" else vals[3],
                input_juros=t["input_juros"], cenario_publicado=t["rotulo"],
            ))

    for k in range(1, len(partes), 3):
        corpo = partes[k + 2]

        # --- formato revisao (2021-2024). Onde a edicao tambem tem tabela de leque, isto releitura
        #     da mesma celula por outro caminho: `_guardar()` exige que os dois valores batam.
        for tab in _segmentar_revisao(_linhas_revisao(corpo)):
            if len(tab) < _MIN_LINHAS_TABELA:
                continue
            cenario, inp, rotulo = _classificar(_contexto(corpo, tab[0][2]))
            if cenario is None:
                continue
            for periodo, valor, _ in tab:
                _guardar(vistos, ed, Projecao(
                    indice="ipca", cenario=cenario, periodo=periodo, valor=valor,
                    input_juros=inp, cenario_publicado=rotulo,
                ))

        # --- formato matriz (2025-2026)
        celulas, rotulo = _parse_matriz(corpo)
        if celulas:
            cenario, inp, rot2 = _classificar(corpo[:4000])
            for indice, periodo, valor in celulas:
                _guardar(vistos, ed, Projecao(
                    indice=indice, cenario=cenario or "juros_esperado", periodo=periodo,
                    valor=valor, input_juros=inp or "focus",
                    cenario_publicado=rotulo or rot2,
                ))

    ed.projecoes = sorted(vistos.values(), key=lambda p: (p.cenario, p.indice, p.periodo.indice))
    return ed


def _atribuir_por_ordem(tabelas: list[dict], ed: EdicaoParseada) -> None:
    """Classifica por ORDEM as tabelas cuja legenda nao deu para ler.

    Vale para o par de tabelas que cobre a MESMA faixa de trimestres -- as duas versoes da mesma
    projecao, uma por cenario. Nessas, a de juros constantes vem primeiro no documento: medido nas
    17 edicoes em que as duas legendas sao legiveis, 17 acertos e nenhuma violacao.

    Faz falta porque em algumas edicoes de 2001-2004 o titulo da tabela esta numa fonte de
    subconjunto com cmap proprio (nao um simples deslocamento, ver `_decodificar_cid()`) e nao ha
    nenhum caminho para o texto. As linhas atribuidas assim ficam com `cenario_publicado` nulo, para
    a procedencia mostrar que o rotulo nao foi lido, e a atribuicao entra em `avisos`.
    """
    por_faixa: dict[str, list[dict]] = {}
    for t in tabelas:
        por_faixa.setdefault(t["faixa"], []).append(t)

    for faixa, grupo in por_faixa.items():
        if len(grupo) != 2 or all(t["cenario"] for t in grupo):
            continue
        # tabela recusada por ser cenario MISTO (Selic de um lado, cambio do outro) nao entra no
        # fallback: a legenda dela foi lida, e o que ela diz e que a tabela nao cabe na coluna
        if any((t["rotulo"] or "").startswith("MISTO") for t in grupo):
            continue
        ordem = ("juros_constante", "juros_esperado")
        # se uma das duas foi classificada, ela tem que estar na posicao que a ordem preve --
        # se nao estiver, a premissa nao vale aqui e e melhor nao atribuir nada
        if any(t["cenario"] and t["cenario"] != ordem[i] for i, t in enumerate(grupo)):
            continue
        for i, t in enumerate(grupo):
            if t["cenario"]:
                continue
            t["cenario"] = ordem[i]
            t["input_juros"] = "constante" if i == 0 else None
            t["rotulo"] = None
            ed.avisos.append(f"tabela {faixa} classificada como {ordem[i]} por ORDEM, sem legenda")


def _segmentar_revisao(linhas: list[tuple[Periodo, float, int]]) -> list[list[tuple]]:
    """Mesma quebra de `_segmentar()`, para as linhas do formato de revisao."""
    tabelas, atual = [], []
    for item in linhas:
        if atual and item[0].indice <= atual[-1][0].indice:
            tabelas.append(atual)
            atual = []
        atual.append(item)
    if atual:
        tabelas.append(atual)
    return tabelas


def _desempatar(tabelas: list[dict], ed: EdicaoParseada) -> None:
    """Quando duas tabelas caem no MESMO cenario e periodo, escolhe uma e descarta a outra.

    Acontece quando o relatorio publica dois cenarios que diferem em algo que a coluna `cenario` nao
    representa: o RI de dez/2002 e mar/2003 trazem "juros constantes de 25% a.a. (Cenario Basico)" e
    "juros constantes de 25% a.a. (Cenario Alternativo)" -- mesmo juro, premissas de risco/cambio
    diferentes. Sem desempate, o dedup por chave guardava a primeira e enchia `avisos` de conflito.

    Preferencia: a que NAO diz "alternativo" na legenda. Se as duas dizem, ou nenhuma, fica a
    primeira do documento -- e o descarte entra em `avisos` com a legenda, para nao virar silencio.
    """
    grupos: dict[tuple[str, str], list[dict]] = {}
    for t in tabelas:
        if t["cenario"]:
            grupos.setdefault((t["cenario"], t["faixa"]), []).append(t)

    for (cenario, faixa), grupo in grupos.items():
        if len(grupo) < 2:
            continue
        def alternativo(t: dict) -> int:
            return 1 if "alternativ" in sem_acento(t["rotulo"] or "").lower() else 0
        preferida = min(grupo, key=lambda t: (alternativo(t), t["pagina"]))
        for t in grupo:
            if t is preferida:
                continue
            t["cenario"] = None
            ed.avisos.append(
                f"tabela {faixa} descartada: mesmo cenario {cenario} da mantida "
                f"(pag {preferida['pagina']}) -- {t['rotulo']}"
            )


def _guardar(vistos: dict, ed: EdicaoParseada, p: Projecao) -> None:
    chave = (p.indice, p.cenario, p.periodo.norm)
    anterior = vistos.get(chave)
    if anterior is None:
        vistos[chave] = p
    elif abs(anterior.valor - p.valor) > 1e-9:
        ed.avisos.append(
            f"{chave} lido duas vezes com valores diferentes: {anterior.valor} e {p.valor}"
        )


# --------------------------------------------------------------------------- reuniao que condiciona


# A primeira reuniao com o HR de 6 trimestres como conceito OFICIAL (meta continua, Decreto
# 12.079/2024). Antes disso o horizonte publicado era o ano-calendario da meta, e o ponto a 6
# trimestres e aproximacao nossa -- e o que a coluna `regime` distingue.
PRIMEIRA_REUNIAO_HR_OFICIAL = 264

_cache_calendario: dict[int, str] | None = None


def calendario() -> dict[int, str]:
    """{numero da reuniao: data ISO}, da 21a a mais recente. Uma chamada de rede, memoizada."""
    global _cache_calendario
    if _cache_calendario is None:
        from connectors import bcb_copom

        _cache_calendario = bcb_copom.calendario_reunioes()
    return _cache_calendario


def casar_reuniao(vintage: dt.date, cal: dict[int, str] | None = None) -> tuple[int, str] | None:
    """A reuniao que condiciona uma edicao: a ULTIMA anterior ou igual a data de publicacao.

    Nao e heuristica de proximidade -- o relatorio declara o vinculo no proprio texto ("a taxa
    basica de juros permanecera inalterada em 17,5% a.a., valor decidido pelo Copom em sua ultima
    reuniao, nos dias 19 e 20 de junho"). Medido nas 109 edicoes: a distancia e sempre de 7 a 28
    dias, sem nenhum caso ambiguo.
    """
    cal = cal or calendario()
    anteriores = [(n, d) for n, d in cal.items() if d <= vintage.isoformat()]
    if not anteriores:
        return None
    return max(anteriores, key=lambda nd: nd[1])


def horizonte_relevante(data_reuniao: str) -> Periodo:
    """O periodo a exatamente 6 trimestres do trimestre da reuniao."""
    d = dt.date.fromisoformat(data_reuniao)
    tri = (d.month - 1) // 3 + 1
    total = (d.year * 4 + tri) + 6
    ano, resto = divmod(total - 1, 4)
    return Periodo(ano, resto + 1)


def carregar(inicio: str | None = None, fim: str | None = None) -> list[EdicaoParseada]:
    """Parseia os `.md` em disco, ja com a reuniao casada. `inicio`/`fim` no formato 'YYYYMM'."""
    cal = calendario()
    out = []
    for caminho in arquivos():
        ano_mes = caminho.stem.split("_")[1]
        if (inicio and ano_mes < inicio) or (fim and ano_mes > fim):
            continue
        texto = caminho.read_text(encoding="utf-8")
        m = re.search(r"Publicado em: (\d{4}-\d{2}-\d{2})", texto)
        if not m:
            continue
        vintage = dt.date.fromisoformat(m.group(1))
        ed = parse(texto, ano_mes, vintage)
        casado = casar_reuniao(vintage, cal)
        if casado:
            ed.nro_reuniao, ed.data_reuniao = casado
        out.append(ed)
    return out
