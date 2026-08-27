"""Sincronizacao e parsing dos comunicados do Copom.

Modulo compartilhado, no padrao de `_rpm_hiato.py`/`_focus_core.py`: nao tem `run()` e nao escreve
no banco. Duas responsabilidades:

1. **`sincronizar()`** — baixa os comunicados via `connectors/bcb_copom.py` e grava um `.md` por
   reuniao em `repository/monetary_policy/raw_md/central_bank_comunication/`. O `.md` e a trilha de
   auditoria: e dele que o parsing le, nao da API, para a carga do banco ser reproduzivel offline.

2. **`parse()`** — extrai do texto as projecoes de inflacao do Copom e os condicionantes do cenario.

## O que da para extrair, por regime

O comunicado mudou de forma varias vezes. Ver `copom_comunicados.md` nesta pasta para o levantamento
completo; o resumo que importa para o parser:

| Reunioes | Datas | Projecoes no comunicado |
|---|---|---|
| 48-~150 | 2000-2010 | nenhuma — um paragrafo curto, as vezes "sem declaracao" |
| ~151-218 | 2010-2018 | prosa, cenario "de referencia" (Selic Focus) e/ou "de mercado", anos civis |
| 219-263 | 2019-2024-06 | prosa, cenario de referencia + alternativo (Selic constante), anos civis. De 2022 em diante aparece tambem a frase do horizonte suavizado (6 trimestres) |
| 264 | 2024-07-31 | prosa, primeira vez com o HR de 6 trimestres como conceito oficial (Decreto 12.079/2024) |
| 265-hoje | 2024-09-18 → | **Tabela 1 em HTML** — IPCA, livres e administrados por coluna de periodo |

O parser cobre os tres ultimos regimes. Para 265+ a Tabela 1 e a fonte primaria e a prosa serve de
conferencia cruzada (`validar()`); antes disso so ha prosa.

## Horizonte relevante (HR)

Desde o Decreto 12.079/2024 o HR e fixo em **6 trimestres a frente** da reuniao, e e a projecao que
o Copom declara estar perseguindo. Na Tabela 1 e sempre a **ultima coluna**; quando cai num 4o
trimestre o BCB rotula so com o ano ("2026"), porque o acumulado em quatro trimestres ali e o ano
civil fechado — normalizado para `2026Q4` do mesmo jeito.

Antes de 2024 o conceito era outro (o ano-calendario da meta), e de 2022 a 2024 conviveu com uma
frase de "horizonte suavizado" que ja era 6 trimestres. As linhas pre-264 ficam marcadas com
`regime='ano_calendario'` para nao serem comparadas com as de hoje sem ressalva.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

from connectors import bcb_copom

_RAIZ = Path(__file__).resolve().parents[4]
DIRETORIO_MD = _RAIZ / "repository" / "monetary_policy" / "raw_md" / "central_bank_comunication"

ORDINAL_PROSA = {"primeiro": 1, "segundo": 2, "terceiro": 3, "quarto": 4}
_MESES = {
    "janeiro": 1, "fevereiro": 2, "marco": 3, "abril": 4, "maio": 5, "junho": 6,
    "julho": 7, "agosto": 8, "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12,
}


# ------------------------------------------------------------------ utilidades de texto


def sem_acento(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def num(s: str | None) -> float | None:
    """'3,2' -> 3.2 ; '-3,9' -> -3.9 ; lixo -> None."""
    if s is None:
        return None
    s = s.strip().replace("%", "").replace("\u2212", "-").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


# ------------------------------------------------------------------------ sincronizacao


def sincronizar(
    inicio: int = bcb_copom.PRIMEIRA_REUNIAO,
    fim: int | None = None,
    destino: Path | str = DIRETORIO_MD,
    sobrescrever: bool = False,
    verbose: bool = True,
) -> dict:
    """Baixa os comunicados e grava um `.md` por reuniao.

    Por default nao rebaixa o que ja esta em disco (`sobrescrever=False`) — o texto de um comunicado
    passado nao muda, entao a rotina normal e barata: so as reunioes novas batem no servidor.

    Returns:
        {'novos': [...], 'existentes': [...], 'vazios': [...], 'erros': {nro: msg}}
    """
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)

    if fim is None:
        fim = bcb_copom.ultima_reuniao()

    ja_em_disco = {
        int(p.name.split("_")[1]): p for p in destino.glob("copom_*_comunicado_*.md")
    }
    r = {"novos": [], "existentes": [], "vazios": [], "erros": {}}

    for nro in range(inicio, fim + 1):
        if nro in ja_em_disco and not sobrescrever:
            r["existentes"].append(nro)
            continue
        try:
            c = bcb_copom.comunicado(nro)
        except Exception as e:
            r["erros"][nro] = str(e)
            if verbose:
                print(f"  {nro}: ERRO {e}")
            continue
        if c is None:
            r["vazios"].append(nro)
            continue
        arq = destino / c.nome_arquivo()
        if nro in ja_em_disco and ja_em_disco[nro] != arq:
            ja_em_disco[nro].unlink()  # data de referencia corrigida pelo BCB
        arq.write_text(c.markdown(), encoding="utf-8")
        r["novos"].append(nro)
        if verbose:
            print(f"  {nro} {c.data_referencia} -> {arq.name}")

    if verbose:
        print(
            f"sincronizar: {len(r['novos'])} baixados, {len(r['existentes'])} ja em disco, "
            f"{len(r['vazios'])} sem conteudo na API, {len(r['erros'])} erros."
        )
    return r


def arquivos(diretorio: Path | str = DIRETORIO_MD) -> list[Path]:
    return sorted(
        Path(diretorio).glob("copom_*_comunicado_*.md"),
        key=lambda p: int(p.name.split("_")[1]),
    )


# ------------------------------------------------------------------------- estruturas


@dataclass
class Periodo:
    """Um periodo de projecao: ano civil ou trimestre."""

    label: str
    ano: int
    trimestre: int | None  # None = ano civil fechado

    @property
    def norm(self) -> str:
        """Chave canonica. Ano civil acumulado == 4o trimestre daquele ano."""
        return f"{self.ano}Q{self.trimestre or 4}"

    @property
    def tipo(self) -> str:
        return "trimestre" if self.trimestre else "ano"


@dataclass
class Projecao:
    indice: str  # ipca | ipca_livres | ipca_administrados
    cenario: str  # juros_esperado | juros_constante (pelo CONDICIONAMENTO, ver _ROTULOS)
    periodo: Periodo
    valor: float
    fonte: str  # tabela | prosa
    cenario_publicado: str | None = None  # o rotulo que o BCB usou naquela reuniao


@dataclass
class Comunicado:
    arquivo: str
    nro_reuniao: int
    data_reuniao: str
    titulo: str
    selic_decidida: float | None = None
    decisao: str | None = None  # reducao | elevacao | manutencao

    projecoes: list[Projecao] = field(default_factory=list)
    periodos_tabela: list[Periodo] = field(default_factory=list)

    # horizonte declarado na prosa (fonte independente da Tabela 1)
    hr_prosa: Periodo | None = None
    hr_prosa_valor: float | None = None
    hr_alternativo_valor: float | None = None  # so na 264a, que publicou os dois cenarios na frase
    hr_ano_calendario: int | None = None  # regime antigo: "horizonte relevante, que inclui 2024"

    # condicionantes do cenario
    juros_constante_nivel: float | None = None  # ver _JUROS_CONSTANTE_NIVEL
    cambio_inicial: float | None = None
    bandeira_tarifaria: str | None = None
    focus: dict[int, float] = field(default_factory=dict)

    @property
    def regime(self) -> str:
        """Qual conceito de horizonte esta por tras do `horizonte_relevante` desta reuniao.

        hr_6_trimestres      264+ -- HR oficial de 6 trimestres (Decreto 12.079/2024)
        horizonte_suavizado  248-263 -- o BCB publicava um ponto de 6 trimestres a frente "que
                             suaviza o efeito ano-calendario", mas a meta ainda era anual
        ano_calendario       antes disso -- o horizonte era o ano civil da meta
        """
        if self.nro_reuniao >= 264:
            return "hr_6_trimestres"
        if self.hr_prosa is not None:
            return "horizonte_suavizado"
        return "ano_calendario"

    @property
    def hr(self) -> Periodo | None:
        """O horizonte desta reuniao: ultima coluna da Tabela 1, ou o que a prosa declarou."""
        if self.periodos_tabela:
            return self.periodos_tabela[-1]
        if self.hr_prosa:
            return self.hr_prosa
        if self.hr_ano_calendario:
            return Periodo(str(self.hr_ano_calendario), self.hr_ano_calendario, None)
        return None

    def horizonte_relevante_norms(self) -> set[str]:
        """Os periodos a marcar com horizonte_relevante=1. Um por reuniao, quando ha."""
        hr = self.hr
        return {hr.norm} if hr else set()

    def trimestres_a_frente(self, p: Periodo | None = None) -> int | None:
        p = p or self.hr
        if p is None or not self.data_reuniao:
            return None
        ano, mes = int(self.data_reuniao[:4]), int(self.data_reuniao[5:7])
        return (p.ano - ano) * 4 + ((p.trimestre or 4) - ((mes - 1) // 3 + 1))


# ---------------------------------------------------------------------------- parsing


def _periodo_de_label(label: str) -> Periodo | None:
    """Cabecalho de coluna da Tabela 1: '2026' ou '1o tri 2028'."""
    raw = label.strip()
    flat = sem_acento(raw).lower().replace("º", "o").replace("°", "o")
    m = re.match(r"^([1-4])\s*o?\.?\s*tri(?:mestre)?\s*(?:de\s*)?(\d{4})$", flat)
    if m:
        return Periodo(raw, int(m.group(2)), int(m.group(1)))
    m = re.match(r"^(\d{4})$", flat)
    if m:
        return Periodo(raw, int(m.group(1)), None)
    return None


def _periodo_de_prosa(ordinal: str | None, ano: str) -> Periodo:
    if ordinal:
        tri = ORDINAL_PROSA[sem_acento(ordinal).lower()]
        return Periodo(f"{ordinal} trimestre de {ano}", int(ano), tri)
    return Periodo(str(ano), int(ano), None)


_IND_TABELA = {
    "ipca": "ipca",
    "ipca livres": "ipca_livres",
    "ipca precos livres": "ipca_livres",
    "ipca administrados": "ipca_administrados",
    "ipca precos administrados": "ipca_administrados",
}


def _parse_tabela(texto: str, c: Comunicado) -> None:
    """Tabela 1 em markdown (reunioes 265+). Fonte primaria quando existe."""
    linhas = [l.strip() for l in texto.splitlines() if l.strip().startswith("|")]
    linhas = [l for l in linhas if not re.match(r"^\|[\s\-:|]+\|$", l)]
    if not linhas:
        return

    def celulas(l: str) -> list[str]:
        return [x.strip() for x in l.strip().strip("|").split("|")]

    cab = celulas(linhas[0])
    c.periodos_tabela = [p for p in (_periodo_de_label(x) for x in cab[1:]) if p]
    for linha in linhas[1:]:
        cel = celulas(linha)
        chave = sem_acento(cel[0]).lower().replace("*", "").strip()
        indice = _IND_TABELA.get(chave)
        if indice is None:
            continue
        for p, bruto in zip(c.periodos_tabela, cel[1:]):
            v = num(bruto)
            if v is not None:
                # a Tabela 1 e sempre o cenario de referencia (juros da Focus, cambio por PPC)
                c.projecoes.append(
                    Projecao(indice, "juros_esperado", p, v, "tabela", "cenario de referencia")
                )


# "3,9% para 2019 e 4,0% para 2020" / "5,8% para 2022, 4,8% para 2023 e 2,9% para 2024"
# "4,7% em 2023, 3,6% em 2024 e 3,2% em 2025"
_PAR_VALOR_ANO = re.compile(r"(-?[\d]+,[\d]+)\s*%\s*(?:para|em|no ano de)\s*(\d{4})", re.I)
# "4,6% para 2022 e 2023" -- um valor para dois anos
_VALOR_DOIS_ANOS = re.compile(r"(-?[\d]+,[\d]+)\s*%\s*(?:para|em)\s*(\d{4})\s*e\s*(\d{4})\b", re.I)
# "4,0% e 3,4% para 2017 e 2018, respectivamente"
_DOIS_VALORES_DOIS_ANOS = re.compile(
    r"(-?[\d]+,[\d]+)\s*%\s*e\s*(-?[\d]+,[\d]+)\s*%\s*para\s*(\d{4})\s*e\s*(\d{4})", re.I
)


def _pares_valor_ano(frase: str) -> list[tuple[float, int]]:
    pares = [(num(v), int(a)) for v, a in _PAR_VALOR_ANO.findall(frase)]
    for v, a1, a2 in _VALOR_DOIS_ANOS.findall(frase):
        pares.append((num(v), int(a2)))
    for v1, v2, a1, a2 in _DOIS_VALORES_DOIS_ANOS.findall(frase):
        pares += [(num(v1), int(a1)), (num(v2), int(a2))]
    vistos, saida = set(), []
    for v, a in pares:
        if v is None or not (1999 <= a <= 2040) or (v, a) in vistos:
            continue
        vistos.add((v, a))
        saida.append((v, a))
    return saida


def _frases(texto: str) -> list[str]:
    corpo = texto.split("\n---\n", 1)[-1]
    corpo = re.sub(r"\s+", " ", corpo)
    return [s.strip() for s in re.split(r"(?<=[.;])\s+", corpo) if s.strip()]


# --- cenarios ---------------------------------------------------------------------------
#
# O NOME que o BCB da ao cenario mudou de significado no meio da serie: em 2016-2017 "cenario de
# referencia" era o de Selic e cambio CONSTANTES e "cenario de mercado" o com trajetorias da Focus;
# de 2020 em diante "cenario de referencia" e justamente o com trajetoria da Focus. Guardar o rotulo
# publicado como se fosse a mesma coisa produziria uma serie silenciosamente errada, por isso
# `cenario` classifica pelo CONDICIONAMENTO e o rotulo original vai para `cenario_publicado`.
#
#   juros_esperado   trajetoria de juros esperada pelo mercado. Nos comunicados e sempre a mediana
#                    da pesquisa Focus; no RPM/RI antigo era a precificacao de futuros e swaps de
#                    DI -- condicionam o modelo do mesmo jeito, e qual das duas e o caso fica em
#                    `cenario_publicado`. Rotulos: "cenario de mercado" (2016-2017), "cenario com
#                    trajetorias ... da pesquisa Focus" (2017-2020), "cenario hibrido" (2020),
#                    "cenario basico" (2020-2022), "cenario de referencia" (2022 em diante).
#   juros_constante  Selic mantida no nivel corrente ao longo do horizonte. Rotulos: "cenario de
#                    referencia" (2016-2017, sentido invertido), "cenario com juros constantes"
#                    (2017-2020), "cenario alternativo" (2023-2024).
#
# A definicao do par referencia/mercado de 2016-2017 vem da convencao do Relatorio de Inflacao da
# epoca, nao de uma frase do proprio comunicado -- os comunicados daquele periodo nao explicitam o
# condicionamento. Por isso, e porque ali duas projecoes de cenarios diferentes dividem a mesma
# frase ("nos cenarios de referencia e mercado, ... 4,4% e 4,7%, respectivamente"), as reunioes
# <= 205 ficam FORA da carga -- ver `PRIMEIRA_REUNIAO_CARGA`.
PRIMEIRA_REUNIAO_CARGA = 206

_ROTULOS = [
    ("juros_constante", "cenario alternativo"),
    ("juros_constante", "juros constante"),
    ("juros_constante", "selic e mantida constante"),
    ("juros_constante", "selic constante"),
    ("juros_esperado", "extraida da pesquisa focus"),
    ("juros_esperado", "extraidas da pesquisa focus"),
    ("juros_esperado", "cenario hibrido"),
    ("juros_esperado", "cenario basico"),
    ("juros_esperado", "cenario de mercado"),
    ("juros_esperado", "cenario de referencia"),
]


def _detecta_cenario(frase_sem_acento: str) -> tuple[str, str] | None:
    """(cenario, rotulo_publicado) quando a frase nomeia ou define um cenario; None se nao."""
    for cenario, chave in _ROTULOS:
        if chave in frase_sem_acento:
            return cenario, chave
    return None


def _indice_da_frase(frase_sem_acento: str) -> str:
    if "administrados" in frase_sem_acento:
        return "ipca_administrados"
    if "livres" in frase_sem_acento:
        return "ipca_livres"
    return "ipca"


def _e_frase_de_projecao(fl: str) -> bool:
    if "expectativas de inflacao" in fl and "apuradas pela pesquisa focus" in fl:
        return False  # e o Focus, nao a projecao do Copom
    if "trajetoria de juros" in fl or "trajetoria para a taxa de juros que" in fl:
        return False  # e a hipotese de Selic do cenario, nao projecao de inflacao
    if "a.a." in fl and "projec" not in fl:
        return False
    return "projec" in fl or "situa" in fl or "encontram-se em torno" in fl


# --- horizonte de seis trimestres -------------------------------------------------------
# 264 em diante: "atual horizonte relevante de politica monetaria" (Decreto 12.079/2024)
_HR_ATUAL = re.compile(
    r"proje[çc][ãa]o de infla[çc][ãa]o (?:do Copom )?para o (?:"
    r"(primeiro|segundo|terceiro|quarto)\s+trimestre\s+de\s+(\d{4})|ano\s+de\s+(\d{4}))"
    r"[^.]{0,80}?atual horizonte relevante[^.]*?situa-se em\s*(-?[\d]+,[\d]+)\s*%",
    re.I | re.S,
)
# 264: primeira reuniao do regime novo, com os dois cenarios na mesma frase
_HR_264 = re.compile(
    r"proje[çc][õoã]es de infla[çc][ãa]o do Copom para o "
    r"(primeiro|segundo|terceiro|quarto)\s+trimestre de (\d{4})\s*\**\s*"
    r"situam-se em\s*(-?[\d]+,[\d]+)\s*%\s*no cen[áa]rio de refer[êe]ncia"
    r"(?:\s*e\s*(-?[\d]+,[\d]+)\s*%\s*em cen[áa]rio alternativo)?",
    re.I | re.S,
)
# 248-253: o "horizonte de seis trimestres a frente, que suaviza o efeito ano-calendario"
_HR_SUAVIZADO = re.compile(
    r"(?:seis trimestres [àa] frente|nesse horizonte)[^.]{0,200}?"
    r"referente ao (primeiro|segundo|terceiro|quarto) trimestre de (\d{4})"
    r"[^.]{0,200}?situa-se em\s*(-?[\d]+,[\d]+)\s*%",
    re.I | re.S,
)
# 248: mesma ideia, mas sem nomear o trimestre -- calculado como reuniao + 6 trimestres
_HR_SUAVIZADO_SEM_TRI = re.compile(
    r"horizonte de seis trimestres [àa] frente[^.]{0,300}?situa-se em\s*(-?[\d]+,[\d]+)\s*%",
    re.I | re.S,
)
# horizonte relevante do regime antigo: o ano-calendario nomeado pelo proprio comunicado
_HR_ANO_CALENDARIO = re.compile(
    r"horizonte relevante,? que inclui ([^.]{0,140})", re.I
)


def _seis_trimestres_a_frente(data_reuniao: str) -> Periodo:
    ano, mes = int(data_reuniao[:4]), int(data_reuniao[5:7])
    tri = (mes - 1) // 3 + 1 + 6
    return Periodo("seis trimestres a frente", ano + (tri - 1) // 4, (tri - 1) % 4 + 1)


def _parse_horizonte(texto: str, c: Comunicado) -> None:
    """Acha a projecao do horizonte que o proprio comunicado diz estar perseguindo."""
    m = _HR_ATUAL.search(texto)
    if m:
        c.hr_prosa = _periodo_de_prosa(m.group(1), m.group(2) or m.group(3))
        c.hr_prosa_valor = num(m.group(4))
        return

    m = _HR_264.search(texto)
    if m:
        c.hr_prosa = _periodo_de_prosa(m.group(1), m.group(2))
        c.hr_prosa_valor = num(m.group(3))
        c.hr_alternativo_valor = num(m.group(4))
        return

    m = _HR_SUAVIZADO.search(texto)
    if m:
        c.hr_prosa = _periodo_de_prosa(m.group(1), m.group(2))
        c.hr_prosa_valor = num(m.group(3))
        return

    m = _HR_SUAVIZADO_SEM_TRI.search(texto)
    if m:
        c.hr_prosa = _seis_trimestres_a_frente(c.data_reuniao)
        c.hr_prosa_valor = num(m.group(1))
        return

    m = _HR_ANO_CALENDARIO.search(texto)
    if m:
        anos = re.findall(r"\b(20\d\d)\b", m.group(1))
        if anos:  # o ultimo ano citado e a ponta do horizonte
            c.hr_ano_calendario = int(anos[-1])


def _parse_prosa(texto: str, c: Comunicado) -> None:
    """Projecoes declaradas em prosa. Unica fonte antes da 265a reuniao."""
    _parse_horizonte(texto, c)

    # O cenario e definido numa frase e referenciado nas seguintes ("Nesse cenario, as projecoes
    # para administrados..."), entao o rotulo corrente tem de ser carregado frase a frase.
    cenario, rotulo = "juros_esperado", None
    for f in _frases(texto):
        fl = sem_acento(f).lower()
        achado = _detecta_cenario(fl)
        if achado:
            cenario, rotulo = achado
        if not _e_frase_de_projecao(fl):
            continue
        indice = _indice_da_frase(fl)
        for valor, ano in _pares_valor_ano(f):
            c.projecoes.append(
                Projecao(indice, cenario, Periodo(str(ano), ano, None), valor, "prosa", rotulo)
            )

    # o ponto do horizonte de seis trimestres nao e um ano civil, entra separado
    if c.hr_prosa and c.hr_prosa_valor is not None and not c.periodos_tabela:
        c.projecoes.append(
            Projecao(
                "ipca", "juros_esperado", c.hr_prosa, c.hr_prosa_valor, "prosa",
                "cenario de referencia",
            )
        )
        if c.hr_alternativo_valor is not None:
            c.projecoes.append(
                Projecao(
                    "ipca", "juros_constante", c.hr_prosa, c.hr_alternativo_valor, "prosa",
                    "cenario alternativo",
                )
            )


# Nivel em que o cenario de juros constantes segura a Selic. Ancorado em "juros" de proposito: a
# MESMA frase declara "taxa de cambio constante a R$4,75/US$", e um padrao solto pegaria o cambio.
# Medido nos 75 comunicados carregados: nivel unico em 20 das 26 reunioes com cenario constante,
# zero ambiguidade, zero falso positivo nas 49 sem. As 6 sem nivel sao de 2022-2024, que dizem
# "a taxa Selic e mantida constante ao longo de todo o horizonte relevante" sem nomear o valor.
# ATENCAO: o nivel e a Selic VIGENTE, nao a decidida na reuniao -- na 229a o cenario constante e a
# 4,25% e a reuniao cortou para 3,75%. E o contrafactual de "nao fazer nada", nao o resultado.
_JUROS_CONSTANTE_NIVEL = r"juros\s+constantes?\s+(?:a|em|de)\s+(\d{1,2},\d{2})\s*%"

_CAMBIO = [
    r"c[âa]mbio (?:parte|partindo) de\s*R\$\s*([\d,]+)\s*/?\s*US\$",      # 2021+ (R$5,10/US$)
    r"c[âa]mbio (?:parte|partindo) de\s*USD/BRL\s*([\d,]+)",              # 2021-2022 (USD/BRL 5,15)
    r"c[âa]mbio\s+constante\s+a\s*R\$\s*([\d,]+)\s*/\s*US\$",            # 2020 (R$4,95/US$)
    r"c[âa]mbio\s+constante\s+a\s*R\$\s*/\s*US\$\s*([\d,]+)",            # 2017-2019 (R$/US$ 3,70)
    r"c[âa]mbio\s+observada\s+.*?([\d]+,[\d]+)",                          # nota de rodape
]


def _parse_condicionantes(texto: str, c: Comunicado) -> None:
    m = re.search(_JUROS_CONSTANTE_NIVEL, texto, re.I)
    if m:
        c.juros_constante_nivel = num(m.group(1))

    for padrao in _CAMBIO:
        m = re.search(padrao, texto, re.I)
        if m:
            c.cambio_inicial = num(m.group(1))
            break

    m = re.search(r"bandeira tarif[áa]ria\s*[“\"']?\s*([a-zA-Zçãé ]+?)\s*[”\"']", texto, re.I)
    if m:
        c.bandeira_tarifaria = m.group(1).strip()

    m = re.search(
        r"expectativas de infla[çc][ãa]o para (\d{4})(?:,\s*(\d{4}))?(?:\s*e\s*(\d{4}))?"
        r"[^.]*?apuradas pela pesquisa Focus[^.]*?"
        r"([\d]+,[\d]+)\s*%(?:\s*,\s*([\d]+,[\d]+)\s*%)?(?:\s*e\s*([\d]+,[\d]+)\s*%)?",
        texto,
        re.I | re.S,
    )
    if m:
        anos = [g for g in m.group(1, 2, 3) if g]
        vals = [g for g in m.group(4, 5, 6) if g]
        for a, v in zip(anos, vals):
            val = num(v)
            if val is not None:
                c.focus[int(a)] = val


def parse(texto: str, arquivo: str = "") -> Comunicado:
    """Le o `.md` de um comunicado e devolve o que deu para extrair."""
    m = re.search(r"^Reuni[ãa]o:\s*(\d+)", texto, re.M)
    nro = int(m.group(1)) if m else -1
    m = re.search(r"^Data de refer[êe]ncia:\s*(\d{4}-\d{2}-\d{2})", texto, re.M)
    data = m.group(1) if m else ""
    m = re.search(r"^T[íi]tulo:\s*(.+)$", texto, re.M)
    titulo = m.group(1).strip() if m else ""

    c = Comunicado(arquivo=arquivo, nro_reuniao=nro, data_reuniao=data, titulo=titulo)

    m = re.search(
        r"(reduz|eleva|mant[éêe]m)\s+a\s+(?:meta\s+da\s+)?taxa\s+Selic\s+(?:para|em)\s+([\d,]+)\s*%",
        titulo,
        re.I,
    )
    if m:
        verbo = sem_acento(m.group(1)).lower()
        c.decisao = {"reduz": "reducao", "eleva": "elevacao", "mantem": "manutencao"}[verbo]
        c.selic_decidida = num(m.group(2))

    _parse_tabela(texto, c)
    _parse_prosa(texto, c)
    _parse_condicionantes(texto, c)
    return c


def validar(c: Comunicado) -> list[str]:
    """Conferencia cruzada prosa x Tabela 1. Lista vazia = nada a apontar."""
    p: list[str] = []
    if not c.periodos_tabela and c.nro_reuniao >= 265:
        p.append("sem Tabela 1 numa reuniao que deveria ter")
    if c.periodos_tabela and c.hr_prosa:
        if c.periodos_tabela[-1].norm != c.hr_prosa.norm:
            p.append(f"HR divergente: tabela={c.periodos_tabela[-1].norm} prosa={c.hr_prosa.norm}")
        else:
            na_tabela = [
                x.valor for x in c.projecoes
                if x.fonte == "tabela" and x.indice == "ipca" and x.periodo.norm == c.hr_prosa.norm
                and x.cenario == "juros_esperado"
            ]
            if not na_tabela:
                p.append("IPCA ausente na coluna do HR")
            elif c.hr_prosa_valor is not None and abs(na_tabela[0] - c.hr_prosa_valor) > 1e-9:
                p.append(f"valor divergente: tabela={na_tabela[0]} prosa={c.hr_prosa_valor}")
    if c.nro_reuniao >= 264:
        n = c.trimestres_a_frente()
        if n is not None and not (5 <= n <= 7):
            p.append(f"HR a {n} trimestres da reuniao (esperado 6)")
    return p
