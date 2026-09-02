"""
CPS (Current Population Survey) -- o lado DOMICILIAR do Employment Situation.

    from domain.db.us.labor_market import mt_cps
    mt_cps.run()                # 1948 -> hoje (sao ~90 series, o historico e barato)

Escopo desta rodada, por decisao do usuario: **as manchetes**, nao os cruzamentos
demograficos. Concretamente, a Summary table A inteira, a tabela A-15 (as seis medidas
alternativas U-1 a U-6) e as taxas por grupo da A-1/A-2/A-3/A-4. Sao 43 conceitos.

A CPS completa tem **68.630 series** e 32 colunas de dimensao cruzada (raca x sexo x
idade x escolaridade x veterano x deficiencia x nativo x ocupacao x industria...), das
quais 20.071 sao mensais e apenas 1.241 dessazonalizadas. Carregar aquilo e um projeto
proprio, e o relatorio desta rodada nao consome nada disso.

--------------------------------------------------------------------------------
POR QUE A API E NAO O ARQUIVO (o inverso da CES e do JOLTS)
--------------------------------------------------------------------------------
`ln.data.1.AllData` traz as 68 mil series de uma vez. Para 90 series isso e baixar
duas ordens de grandeza a mais de dado do que se usa. Pela API sao 50 series por
requisicao e 20 anos por janela: 90 series x 4 janelas = **8 requisicoes**, contra uma
cota diaria de 500. A regra que este ramo segue e "o arquivo quando as series se
contam em centenas, a API quando se contam em dezenas".

--------------------------------------------------------------------------------
O series_id DA CPS, E COMO O PAR SA/NSA SE DERIVA
--------------------------------------------------------------------------------
    LNS 11 000000        LN + S/U + 2 digitos + 6 digitos
    ^^^  ^^ ^^^^^^
    |    |  \\-- o conceito
    |    \\----- 1x com ajuste sazonal, 0x sem
    \\---------- LNS = dessazonalizado, LNU = bruto

O par nao e "trocar S por U": o campo de 2 digitos muda junto (LNS**11** -> LNU**01**,
LNS**13** -> LNU**03**). `_par_nsa()` faz a conversao e `run()` **confere cada id
derivado contra o catalogo** antes de pedir -- um id inventado volta da API como serie
vazia, sem erro, e a linha simplesmente nao existiria.

`LNU00000000` (populacao) nao tem versao dessazonalizada, e isso e da fonte: o proprio
release marca a linha com "The population figures are not adjusted for seasonal
variation".

--------------------------------------------------------------------------------
OS TRES CONCEITOS QUE PARECEM O MESMO E NAO SAO (achados conferindo o release)
--------------------------------------------------------------------------------
1. **"Part time for noneconomic reasons" da Summary table A e AT WORK, nao USUALLY.**
   O cabecalho da secao e "Employed people *at work* part time", e o numero publicado
   (22.770 mil em jul/2026) e `LNS12005977` ("At Work 1-34 Hours, Usually Work Part
   Time Noneconomic Reasons"). A serie de nome mais obvio, `LNS12032200`
   ("Part-Time for Noneconomic Reasons, Nonagricultural Industries"), da **22.345** --
   425 mil de diferenca, e nada no nome avisa.
2. **"15 a 26 semanas" nao e `LNS13008516`**, que e "15 semanas *ou mais*" (2.929
   contra 1.157). A serie certa e `LNS13008876`.
3. **Marginalmente ligados e desalentados TEM versao dessazonalizada** (`LNS15026642`
   e `LNS15026645`), e e ela que a Summary table A imprime. Usar a `LNU` -- que e o
   que uma busca por nome encontra primeiro -- da 1.871 e 503 contra 1.806 e 476.

Os tres foram achados porque a carga confere cada serie contra o valor publicado
(`_VALIDACAO`), nao porque o nome estava errado. Sem essa conferencia as tres teriam
entrado silenciosamente com o conceito trocado.

--------------------------------------------------------------------------------
DDL
--------------------------------------------------------------------------------
    CREATE TABLE mt_cps (
        date        DATE          NOT NULL COMMENT 'primeiro dia do mes de referencia',
        categoria   VARCHAR(32)   NOT NULL COMMENT 'slug do conceito (ver _SERIES)',
        ajuste      VARCHAR(3)    NOT NULL COMMENT 'sa = dessazonalizado, nsa = bruto',
        valor       DECIMAL(14,3)     NULL COMMENT 'na unidade da categoria',
        grupo       VARCHAR(24)   NOT NULL COMMENT 'bloco do release: status, taxa_grupo, motivo, duracao, parcial, fora_forca, alternativa',
        unidade     VARCHAR(10)   NOT NULL COMMENT 'mil = milhares de pessoas, pct = por cento, semanas',
        series_id   VARCHAR(20)   NOT NULL COMMENT 'series_id do BLS',
        PRIMARY KEY (date, categoria, ajuste)
    ) COMMENT 'CPS/BLS: manchetes da pesquisa domiciliar (Summary table A, A-15 e as
               taxas por grupo). Ver domain/db/us/labor_market/mt_cps.py'
"""

from __future__ import annotations

import pandas as pd

from connectors.bls import BLS
from domain.db.us._gravar import gravar

_DATABASE = "macro_us"
_TABLE = "mt_cps"

# (series_id SA, slug, grupo, unidade)
# A ordem e a do release, e e ela que o relatorio usa para ordenar as linhas.
_SERIES: list[tuple[str, str, str, str]] = [
    # ── Summary table A: employment status ──────────────────────────────────
    ("LNU00000000", "populacao", "status", "mil"),
    ("LNS11000000", "forca_trabalho", "status", "mil"),
    ("LNS11300000", "participacao", "status", "pct"),
    ("LNS12000000", "ocupados", "status", "mil"),
    ("LNS12300000", "razao_emprego_pop", "status", "pct"),
    ("LNS13000000", "desocupados", "status", "mil"),
    ("LNS14000000", "taxa_desemprego", "status", "pct"),
    ("LNS15000000", "fora_forca", "status", "mil"),
    # ── taxas de desemprego por grupo (A-1 a A-4) ──────────────────────────
    ("LNS14000025", "taxa_homens_20", "taxa_grupo", "pct"),
    ("LNS14000026", "taxa_mulheres_20", "taxa_grupo", "pct"),
    ("LNS14000012", "taxa_16_19", "taxa_grupo", "pct"),
    ("LNS14000003", "taxa_brancos", "taxa_grupo", "pct"),
    ("LNS14000006", "taxa_negros", "taxa_grupo", "pct"),
    ("LNS14032183", "taxa_asiaticos", "taxa_grupo", "pct"),
    ("LNS14000009", "taxa_hispanicos", "taxa_grupo", "pct"),
    ("LNS14000048", "taxa_25_mais", "taxa_grupo", "pct"),
    ("LNS14027659", "taxa_sem_medio", "taxa_grupo", "pct"),
    ("LNS14027660", "taxa_medio", "taxa_grupo", "pct"),
    ("LNS14027689", "taxa_superior_incompleto", "taxa_grupo", "pct"),
    ("LNS14027662", "taxa_superior", "taxa_grupo", "pct"),
    # ── motivo do desemprego (A-11) ────────────────────────────────────────
    ("LNS13023621", "perderam_emprego", "motivo", "mil"),
    ("LNS13023705", "pediram_demissao", "motivo", "mil"),
    ("LNS13023557", "reentrantes", "motivo", "mil"),
    ("LNS13023569", "novos_entrantes", "motivo", "mil"),
    # ── duracao do desemprego (A-12) ───────────────────────────────────────
    ("LNS13008396", "dur_ate_5s", "duracao", "mil"),
    ("LNS13008756", "dur_5_14s", "duracao", "mil"),
    ("LNS13008876", "dur_15_26s", "duracao", "mil"),
    ("LNS13008636", "dur_27s_mais", "duracao", "mil"),
    ("LNS13008275", "dur_media", "duracao", "semanas"),
    ("LNS13008276", "dur_mediana", "duracao", "semanas"),
    # ── tempo parcial (A-8) ────────────────────────────────────────────────
    ("LNS12032194", "parcial_economico", "parcial", "mil"),
    ("LNS12032195", "parcial_falta_trabalho", "parcial", "mil"),
    ("LNS12032196", "parcial_so_achou_pt", "parcial", "mil"),
    ("LNS12005977", "parcial_nao_economico", "parcial", "mil"),
    # ── fora da forca de trabalho (A-1 / A-16) ─────────────────────────────
    ("LNS15026639", "quer_trabalhar", "fora_forca", "mil"),
    ("LNS15026642", "marginalmente_ligados", "fora_forca", "mil"),
    ("LNS15026645", "desalentados", "fora_forca", "mil"),
    # ── A-15: medidas alternativas de subutilizacao ────────────────────────
    ("LNS13025670", "u1", "alternativa", "pct"),
    ("LNS14023621", "u2", "alternativa", "pct"),
    ("LNS14000000", "u3", "alternativa", "pct"),
    ("LNS13327707", "u4", "alternativa", "pct"),
    ("LNS13327708", "u5", "alternativa", "pct"),
    ("LNS13327709", "u6", "alternativa", "pct"),
]

# O valor publicado no release de julho/2026 (divulgado 07/08/2026). E o que impede um
# `series_id` de nome plausivel e conceito errado de entrar em silencio -- foi assim
# que os tres achados do docstring apareceram.
_VALIDACAO = {
    "populacao": 275_282, "forca_trabalho": 169_094, "participacao": 61.4,
    "ocupados": 162_177, "razao_emprego_pop": 58.9, "desocupados": 6_916,
    "taxa_desemprego": 4.1, "fora_forca": 106_189,
    "taxa_homens_20": 3.9, "taxa_mulheres_20": 3.7, "taxa_16_19": 12.1,
    "taxa_brancos": 3.6, "taxa_negros": 6.3, "taxa_asiaticos": 4.0,
    "taxa_hispanicos": 4.6, "taxa_25_mais": 3.4, "taxa_sem_medio": 5.4,
    "taxa_medio": 4.0, "taxa_superior_incompleto": 3.6, "taxa_superior": 2.7,
    "perderam_emprego": 3_309, "pediram_demissao": 793, "reentrantes": 2_123,
    "novos_entrantes": 761,
    "dur_ate_5s": 1_960, "dur_5_14s": 2_049, "dur_15_26s": 1_157,
    "dur_27s_mais": 1_771,
    "parcial_economico": 4_804, "parcial_falta_trabalho": 3_019,
    "parcial_so_achou_pt": 1_428, "parcial_nao_economico": 22_770,
    "marginalmente_ligados": 1_806, "desalentados": 476,
    "u6": 7.9,
}
_MES_VALIDACAO = "2026-07-01"
_ANO_INICIAL = 1948          # a CPS mensal comeca aqui


def _par_nsa(sid: str) -> str | None:
    """O id sem ajuste sazonal do mesmo conceito, ou None se ja for um LNU."""
    if sid.startswith("LNU"):
        return None
    return "LNU0" + sid[4] + sid[5:]


def _catalogo(bls: BLS) -> dict[str, str]:
    cat = bls.read_flat_table("ln", "ln.series")
    cat.columns = [c.strip() for c in cat.columns]
    cat["series_id"] = cat["series_id"].astype(str).str.strip()
    cat["series_title"] = cat["series_title"].astype(str).str.strip()
    return dict(zip(cat["series_id"], cat["series_title"]))


def _plano(bls: BLS) -> pd.DataFrame:
    """Uma linha por (series_id, categoria, ajuste), conferida contra o catalogo."""
    tit = _catalogo(bls)
    linhas, sem_nsa = [], []
    for sid, slug, grupo, unidade in _SERIES:
        if sid not in tit:
            raise RuntimeError(
                f"{sid} ({slug}) nao esta em ln.series. O BLS descontinuou ou renumerou "
                f"a serie -- confira o titulo no catalogo antes de trocar o id, porque "
                f"um id parecido pode ser outro conceito (ver o docstring)."
            )
        ajuste = "nsa" if sid.startswith("LNU") else "sa"
        linhas.append({"series_id": sid, "categoria": slug, "grupo": grupo,
                       "unidade": unidade, "ajuste": ajuste, "titulo": tit[sid]})
        nsa = _par_nsa(sid)
        if nsa is None:
            continue
        if nsa in tit:
            linhas.append({"series_id": nsa, "categoria": slug, "grupo": grupo,
                           "unidade": unidade, "ajuste": "nsa", "titulo": tit[nsa]})
        else:
            sem_nsa.append(slug)
    if sem_nsa:
        print(f"  {len(sem_nsa)} conceitos sem par bruto no catalogo: "
              f"{', '.join(sem_nsa[:6])}{'...' if len(sem_nsa) > 6 else ''}")
    plano = pd.DataFrame(linhas)
    dup = plano.duplicated(subset=["categoria", "ajuste"]).sum()
    if dup:
        raise RuntimeError(f"{dup} pares (categoria, ajuste) repetidos no plano")
    return plano


def _validar(dados: pd.DataFrame) -> None:
    """Cada categoria com valor publicado tem de reproduzi-lo no mes de referencia."""
    alvo = dados[(dados["ajuste"] == "sa") & (dados["date"] == pd.Timestamp(_MES_VALIDACAO))]
    if alvo.empty:
        alvo = dados[(dados["ajuste"] == "nsa")
                     & (dados["date"] == pd.Timestamp(_MES_VALIDACAO))]
    obtido = dict(zip(alvo["categoria"], alvo["valor"]))
    # a populacao so existe em nsa
    nsa = dados[(dados["ajuste"] == "nsa") & (dados["date"] == pd.Timestamp(_MES_VALIDACAO))]
    for k, v in zip(nsa["categoria"], nsa["valor"]):
        obtido.setdefault(k, v)

    erros, conferidos = [], 0
    for slug, esperado in _VALIDACAO.items():
        v = obtido.get(slug)
        if v is None:
            erros.append(f"{slug}: sem valor em {_MES_VALIDACAO}")
            continue
        conferidos += 1
        tol = 0.051 if abs(esperado) < 200 else 1.0
        if abs(float(v) - esperado) > tol:
            erros.append(f"{slug}: {v} contra {esperado} publicado ({_MES_VALIDACAO})")
    if erros:
        raise RuntimeError(
            f"{len(erros)} categorias da CPS nao reproduzem o release de "
            f"{_MES_VALIDACAO}:\n  " + "\n  ".join(erros[:12])
            + "\nUm series_id de nome plausivel pode ser outro conceito -- e o que esta "
              "conferencia existe para pegar."
        )
    print(f"  validacao: {conferidos} categorias reproduzem o release de {_MES_VALIDACAO}")


def run(desde: int | None = None) -> pd.DataFrame:
    """Carrega as manchetes da CPS.

    Args:
        desde: primeiro ano. Default 1948, o inicio da serie mensal. Sao ~90 series,
               entao o historico inteiro custa 8 requisicoes -- nao ha motivo para
               janela curta na rotina.

    Returns:
        As linhas gravadas.
    """
    bls = BLS()
    print(f"{_TABLE}: {len(_SERIES)} conceitos da pesquisa domiciliar")
    plano = _plano(bls)
    print(f"  {len(plano)} series ({int((plano.ajuste == 'sa').sum())} sa, "
          f"{int((plano.ajuste == 'nsa').sum())} nsa)")

    ano0 = _ANO_INICIAL if desde is None else int(desde)
    bruto = bls.get_series(sorted(plano["series_id"].unique()),
                           start_year=ano0, end_year=pd.Timestamp.today().year)
    if bruto.empty:
        raise RuntimeError("a API do BLS nao devolveu nenhuma observacao da CPS")
    bruto["date"] = pd.to_datetime(bruto["date"])

    dados = bruto.merge(plano, on="series_id", how="inner")
    faltam = set(plano["series_id"]) - set(bruto["series_id"])
    if faltam:
        raise RuntimeError(
            f"{len(faltam)} series pedidas nao voltaram da API: {sorted(faltam)[:8]}. "
            "Uma serie vazia nao levanta erro na API -- a linha simplesmente nao existe."
        )
    dados = dados.rename(columns={"value": "valor"})
    dados = dados.dropna(subset=["valor"])
    _validar(dados)

    cols = ["date", "categoria", "ajuste", "valor", "grupo", "unidade", "series_id"]
    saida = (dados[cols]
             .drop_duplicates(subset=["date", "categoria", "ajuste"])
             .sort_values(["date", "grupo", "categoria", "ajuste"]))
    print(f"  {len(saida):,} linhas, {saida['date'].min().date()} -> "
          f"{saida['date'].max().date()}")
    gravar(_DATABASE, _TABLE, saida, sonda="categoria")
    return saida


if __name__ == "__main__":
    run()
