"""Testes de dados das curvas de juros extraidas do TaxaSwap.txt da B3.

Nasceu da auditoria de 2026-09-02, que achou dois defeitos com anos de idade em
`base_mercado.interest_rates` -- ambos produzidos por
`scipy.interp1d(fill_value="extrapolate")` sobre os titulos ofertados no Tesouro
Direto, sem limite de extrapolacao:

  (a) PREJS @ 120M/240M em 14 pregoes de 2010, com -30,09% no 20 anos, causado por
      uma cotacao placeholder da fonte (NTN-F 2021, `Taxa Compra = 0,00`) no vertice
      mais longo, alavancada 2,3x pela extrapolacao;
  (b) NTNBJS de 1M a 24M a partir de 17/08/2026, quando a NTN-B 2026-08-15 venceu e
      o pool passou a comecar em 1.448 dias -- a curva curta virou reta esticada para
      tras e no dia 17 saiu com 8,200 identico em sete vertices.

Nenhum dos dois levantou excecao, nenhum apareceu em tela e o (a) sobreviveu 16 anos.
Dai este arquivo: `problemas_do_pregao()` e o guarda que a extracao diaria deve
chamar, e os testes provam que ele pega os dois defeitos usando os dados REAIS de
antes da correcao como controle positivo -- nao mutante sintetico.

Os limiares nao foram escolhidos, foram MEDIDOS na serie de 5.157 pregoes
(2006-01-02 a 2026-09-01) reconstruida da B3. Cada constante abaixo traz o extremo
observado ao lado, para que a proxima pessoa saiba de quanta folga dispoe.

Como rodar:
    uv run pytest tests/test_curvas_juros_b3.py -v

O historico completo so e exercitado se o CSV de staging estiver disponivel (ver
`_STAGING`); sem ele os controles positivos continuam rodando, porque estao
embutidos no proprio arquivo.
"""

import os

import pytest

# O guarda NAO vive aqui: ele e chamado pela extracao diaria, entao mora no ETL
# e este arquivo so o exercita. Duplicar os limiares aqui os faria divergir do
# que roda em producao no primeiro ajuste -- que e exatamente o modo de falha
# que este arquivo existe para evitar.
#
# Os limiares foram MEDIDOS na serie de 5.115 pregoes (2006-01-02 a 2026-09-02)
# reconstruida da B3, nao escolhidos; cada constante em
# domain/db/brasil/b3/br_interest_rate.py traz o extremo observado ao lado.
from connectors.b3_curvas import DIAS_POR_MES, VERTICES  # noqa: F401
from domain.db.brasil.b3.br_interest_rate import (
    _BANDA_BREAKEVEN,
    _PISO_NOMINAL,
    _PISO_REAL,
    _PISO_VERTICES,
    _SALTO_MAX,
    _TETO,
    problemas_do_pregao,
)

SPEC = {c: VERTICES[c] for c in VERTICES}
MESES = {f"{m}M": m for v in VERTICES.values() for m in v}


def test_a_spec_e_a_que_foi_acordada():
    """Se alguem mudar a grade de uma curva, este teste diz -- e os limiares
    de breakeven e de salto abaixo passam a valer para outra coisa."""
    assert SPEC["DIPRE"] == [1, 3, 6, 9, 12, 24, 60, 120, 240]
    assert SPEC["PREJS"] == [6, 9, 12, 24, 60, 120]
    assert SPEC["NTNBJS"] == [3, 6, 9, 12, 24, 60, 120, 240]
    assert DIAS_POR_MES == 30.44


def test_a_curva_real_tem_piso_proprio():
    """A NTN-B curta vai a -5,42 de verdade (marco/2021). Um piso positivo nela
    reprovaria dado correto -- foi medido, nao suposto."""
    assert _PISO_REAL < 0 < _PISO_NOMINAL
    assert _PISO_REAL <= -5.423
    assert _PISO_NOMINAL <= 1.866 and _TETO >= 21.079


def test_a_banda_de_breakeven_afrouxa_na_ponta_curta():
    """Breakeven curto negativo EXISTE: em maio/2020 o 9M deu -1,00% com dado
    bom. A banda tem de aceitar isso no curto e apertar no longo."""
    assert _BANDA_BREAKEVEN["3M"][0] < _BANDA_BREAKEVEN["12M"][0]
    assert _BANDA_BREAKEVEN["9M"][0] <= -1.00
    assert _BANDA_BREAKEVEN["240M"][0] > 0


# ---------------------------------------------------------------------------
# Controles positivos: os dois defeitos reais, com os numeros que estavam no banco
# ---------------------------------------------------------------------------

# 22/01/2010, PREJS. Grade da fonte naquele dia (dias corridos, taxa) -- a ultima
# cotacao e o placeholder: NTN-F 2021-01-01 com Compra 0,00 e Venda 0,06.
GRADE_PREJS_20100122 = [
    (160, 9.145), (344, 10.390), (709, 11.905), (1075, 12.520),
    (1440, 12.860), (2536, 13.330), (3997, 0.030),
]
# O que o conector antigo gravou (o 120M interpolado sobre o placeholder e o 240M
# extrapolado 3.308 dias alem do ultimo ponto).
PUBLICADO_PREJS_20100122 = {
    ("PREJS", "6M"): 9.2982, ("PREJS", "9M"): 9.9161, ("PREJS", "12M"): 10.4783,
    ("PREJS", "24M"): 11.9412, ("PREJS", "60M"): 13.0257,
    ("PREJS", "120M"): 3.1634,
}

# 17/08/2026, NTNBJS. A NTN-B 2026-08-15 venceu no fim de semana e o pool passou a
# comecar em 1.448 dias corridos.
GRADE_NTNBJS_20260817 = [
    (1459, 8.20), (2190, 8.20), (3193, 8.07), (3924, 7.87), (5112, 7.79),
    (6846, 7.65), (8764, 7.60), (10498, 7.51), (12417, 7.50),
]
PUBLICADO_NTNBJS_20260817 = {
    ("NTNBJS", "3M"): 8.200, ("NTNBJS", "6M"): 8.200, ("NTNBJS", "9M"): 8.200,
    ("NTNBJS", "12M"): 8.200, ("NTNBJS", "24M"): 8.200, ("NTNBJS", "60M"): 8.200,
    ("NTNBJS", "120M"): 7.944, ("NTNBJS", "240M"): 7.638,
}


def test_pega_o_bug_de_2010_no_prejs():
    """O -30% do 20 anos e o 3,16% do 10 anos tinham de ter sido barrados."""
    grades = {"PREJS": GRADE_PREJS_20100122}
    pub = dict(PUBLICADO_PREJS_20100122)
    pub[("PREJS", "240M")] = -30.0894          # o valor que ficou 16 anos no banco

    probs = problemas_do_pregao(grades, pub)

    # o 240M cai fora da grade (7.305d contra maximo de 3.997d)
    assert any("240M" in x and "fora da grade" in x for x in probs), probs
    # e o valor negativo tambem e barrado, por outra via
    assert any("240M" in x and "fora de [1.0" in x for x in probs), probs
    # o 120M estava DENTRO da grade -- so a cotacao placeholder da fonte o estraga.
    # Este e o limite honesto do guarda: a checagem de grade nao pega este caso.
    assert not any("120M" in x and "fora da grade" in x for x in probs), probs


def test_placeholder_da_fonte_e_pego_pelo_piso():
    """A cotacao de 0,03% do NTN-F 2021 nao pode passar por taxa."""
    grades = {"PREJS": GRADE_PREJS_20100122}
    pub = {("PREJS", "120M"): 0.030}
    probs = problemas_do_pregao(grades, pub)
    assert any("120M" in x and "fora de [1.0" in x for x in probs), probs


def test_pega_a_quebra_da_ntnb_em_agosto_2026():
    """Os seis vertices curtos a 8,200 tinham de ter sido barrados, e por dois
    caminhos independentes: grade e degeneracao."""
    grades = {"NTNBJS": GRADE_NTNBJS_20260817}
    probs = problemas_do_pregao(grades, dict(PUBLICADO_NTNBJS_20260817))

    for t in ["3M", "6M", "9M", "12M", "24M"]:
        assert any(f"@{t}:" in x and "fora da grade" in x for x in probs), (t, probs)
    assert any("degenerada" in x for x in probs), probs
    # o 60M (1.826d) esta DENTRO da grade e e interpolacao legitima
    assert not any("@60M:" in x and "fora da grade" in x for x in probs), probs


def test_pega_o_salto_do_24m_na_virada_de_17_08():
    """De 10,783 para 8,200 num pregao: 2,58 p.p., acima do limite de 2,0 da
    curva real (maximo observado em 20 anos: 1,208)."""
    grades = {"NTNBJS": GRADE_NTNBJS_20260817}
    probs = problemas_do_pregao(
        grades,
        {("NTNBJS", "24M"): 8.200, ("NTNBJS", "120M"): 7.944},
        anterior={("NTNBJS", "24M"): 10.783, ("NTNBJS", "120M"): 7.941},
        dias_desde_anterior=3,
    )
    assert any("@24M:" in x and "salto" in x for x in probs), probs
    assert not any("@120M:" in x and "salto" in x for x in probs), probs


def test_feriado_longo_nao_acusa_salto():
    """Gap acima de 4 dias omite a checagem -- senao a virada de ano acusa."""
    grades = {"NTNBJS": GRADE_NTNBJS_20260817}
    probs = problemas_do_pregao(
        grades, {("NTNBJS", "24M"): 8.200},
        anterior={("NTNBJS", "24M"): 10.783}, dias_desde_anterior=10)
    assert not any("salto" in x for x in probs), probs


def test_breakeven_negativo_curto_nao_e_reprovado():
    """Maio/2020: o 9M deu -1,00% com dado bom e o IPCA deflacionou de verdade.
    A banda curta tem de aceitar isso, ou o guarda reprova dado correto."""
    grades = {"DIPRE": [(1, 2.0), (8000, 8.0)], "NTNBJS": [(1, 3.0), (8000, 6.0)]}
    probs = problemas_do_pregao(grades, {("DIPRE", "9M"): 2.512,
                                         ("NTNBJS", "9M"): 3.199})
    assert not any("breakeven" in x for x in probs), probs


def test_breakeven_de_12m_negativo_e_reprovado():
    """No 12M o dado bom nunca desceu de +0,73 em 5.113 pregoes. O -3,12 que a
    serie antiga produzia em 08/05/2020 e barrado."""
    grades = {"DIPRE": [(1, 2.0), (8000, 8.0)], "NTNBJS": [(1, 3.0), (8000, 6.0)]}
    probs = problemas_do_pregao(grades, {("DIPRE", "12M"): 2.623,
                                         ("NTNBJS", "12M"): 5.933})
    assert any("breakeven@12M" in x for x in probs), probs


def test_parse_parcial_e_pego():
    """Resposta throttled que parseia meia grade nao pode virar dado."""
    probs = problemas_do_pregao({"DIPRE": [(1, 13.0), (100, 13.5)]},
                                {("DIPRE", "1M"): 13.2})
    assert any("vertices na fonte" in x for x in probs), probs


def test_pregao_bom_passa_limpo():
    """28/08/2026, os tres primeiros vertices reais da NTN-B, sem nada publicado
    fora da grade."""
    grades = {"NTNBJS": [(80, 6.2566), (171, 6.4872), (262, 6.7300),
                         (718, 7.9520), (1448, 8.0800), (3182, 7.9049),
                         (12407, 7.3784)]}
    # a grade acima tem 7 vertices, abaixo do piso de 60 -- entao este teste
    # exercita so as checagens que nao dependem do piso
    probs = [x for x in problemas_do_pregao(
        grades, {("NTNBJS", "9M"): 6.98, ("NTNBJS", "12M"): 7.42,
                 ("NTNBJS", "24M"): 8.05})
        if "vertices na fonte" not in x]
    assert probs == [], probs


# ---------------------------------------------------------------------------
# Historico completo: o guarda nao pode reprovar a serie que foi gravada
# ---------------------------------------------------------------------------
# Le o banco em vez de um CSV de staging: o que interessa e se o guarda aprova o
# que EFETIVAMENTE esta na tabela, nao um arquivo intermediario que pode ter
# divergido dela. Pula quando nao ha MySQL alcancavel (CI sem banco).


def _serie_do_banco():
    from connectors.mysql import MySQLDataRequester
    req = MySQLDataRequester("macro_brasil", "br_interest_rate")
    req.connect()
    df = req.request_data()
    req.close_connection()
    return df


@pytest.fixture(scope="module")
def serie():
    try:
        S = _serie_do_banco()
    except Exception as exc:                                       # noqa: BLE001
        pytest.skip(f"MySQL indisponivel: {exc}")
    if S is None or not len(S):
        pytest.skip("macro_brasil.br_interest_rate vazia")
    import pandas as pd
    S["date"] = pd.to_datetime(S["date"])
    S["value"] = S["value"].astype(float)
    return S


@pytest.fixture(scope="module")
def curvas_b3(serie):
    """So as tres curvas que vem do TaxaSwap da B3.

    A tabela tambem hospeda `POLICY` desde 2026-09-03 -- a meta Selic, que nao
    e interpolada de grade nenhuma e por isso nao passa pelo guarda nem pelos
    limiares medidos aqui. Filtrar por lista explicita e nao por "tudo menos
    POLICY" de proposito: uma curva nova entrando na tabela tem de reprovar o
    teste de composicao abaixo, nao escorregar para dentro dos testes de grade.
    """
    return serie[serie.curve.isin(SPEC)]


def test_a_serie_gravada_cobre_o_que_a_spec_promete(curvas_b3):
    """Cada curva da B3 tem exatamente os vertices da spec, e nenhum a mais."""
    for curva, meses in SPEC.items():
        tem = set(curvas_b3[curvas_b3.curve == curva].tenor)
        assert tem == {f"{m}M" for m in meses}, (curva, sorted(tem))


def test_a_tabela_hospeda_exatamente_quatro_curvas(serie):
    """As 3 da B3 mais a POLICY. Se uma quinta aparecer, este teste diz -- e o
    resto do arquivo passa a nao cobri-la, que e o motivo de afirmar aqui."""
    assert set(serie.curve) == set(SPEC) | {"POLICY"}, sorted(set(serie.curve))


def test_a_policy_e_a_meta_do_bc_no_vertice_de_um_dia(serie):
    """A POLICY existe por pedido do usuario ("centralizar os dados de juros na
    mesma tabela, independente se e curva ou dado definido pelo BC"). Tres
    coisas a afirmar, e a terceira e a que pega o erro plausivel: `tenor_years`
    NAO pode ser zero, senao qualquer interpolacao ancorada no vertice curto
    quebra."""
    p = serie[serie.curve == "POLICY"]
    assert set(p.tenor) == {"1d"}, sorted(set(p.tenor))
    # A meta vigora em dia corrido, entao ela TEM de ter mais datas que as
    # curvas da B3, que só existem em pregao.
    assert p.date.nunique() > serie[serie.curve == "DIPRE"].date.nunique()
    ty = set(p.tenor_years.astype(float).round(6))
    assert ty == {round(1 / 252, 6)}, ty
    # Selic meta: 2,00 no piso da pandemia e 173,23 nos primeiros meses do Real.
    assert p.value.min() == 2.0
    assert 173.0 < p.value.max() < 174.0


def test_nenhum_valor_fora_do_piso_e_teto(curvas_b3):
    piso = {"NTNBJS": _PISO_REAL}
    fora = curvas_b3[curvas_b3.apply(lambda r: not (piso.get(r.curve, _PISO_NOMINAL)
                                            <= r.value <= _TETO), axis=1)]
    assert fora.empty, fora.head(10).to_string()


def test_breakeven_dentro_da_banda_em_toda_a_serie(curvas_b3):
    D = curvas_b3[curvas_b3.curve == "DIPRE"].pivot(index="date", columns="tenor", values="value")
    N = curvas_b3[curvas_b3.curve == "NTNBJS"].pivot(index="date", columns="tenor", values="value")
    testados = 0
    for tenor, (lo, hi) in _BANDA_BREAKEVEN.items():
        if tenor in D and tenor in N:
            be = ((1 + D[tenor] / 100) / (1 + N[tenor] / 100) - 1).mul(100).dropna()
            ruins = be[(be < lo) | (be > hi)]
            assert ruins.empty, f"breakeven@{tenor}: {ruins.head().round(2).to_dict()}"
            testados += 1
    assert testados >= 7, testados


def test_nenhum_salto_acima_do_limite_em_toda_a_serie(curvas_b3):
    """So vertices de 24M+, e so entre pregoes a <= 4 dias -- feriado longo nao
    e distorcao. E a mesma regra que o guarda aplica no dia."""
    for curva, lim in _SALTO_MAX.items():
        p = curvas_b3[curvas_b3.curve == curva].pivot(index="date", columns="tenor", values="value")
        for tenor in [t for t in ["24M", "60M", "120M", "240M"] if t in p]:
            s = p[tenor].dropna()
            gap = s.index.to_series().diff().dt.days
            d = s.diff().abs()[gap <= 4].dropna()
            assert d.max() <= lim, f"{curva}@{tenor}: salto de {d.max():.3f} > {lim}"


def test_nenhuma_grade_degenerada_em_toda_a_serie(curvas_b3):
    """A quebra de 17/08/2026 saiu com seis vertices curtos identicos. Nenhum
    pregao da serie nova pode ter tres ou mais iguais."""
    curtos = ["3M", "6M", "9M", "12M", "24M", "60M"]
    for curva in SPEC:
        p = curvas_b3[curvas_b3.curve == curva].pivot(index="date", columns="tenor", values="value")
        cols = [c for c in curtos if c in p]
        if len(cols) < 3:
            continue
        r = p[cols].round(3)
        iguais = r[r.nunique(axis=1) == 1].dropna(how="all")
        assert iguais.empty, f"{curva}: {iguais.head().to_string()}"


# ---------------------------------------------------------------------------
# A duplicacao do policy rate nao pode voltar (2026-09-03, 2a rodada)
# ---------------------------------------------------------------------------
# `macro_international.cmb_policy_rates` era o ETL do BIS e foi removida quando
# se mediu que nao guardava nada que as tabelas de juros nao tivessem: as
# 53.663 linhas dela eram reproduzidas exatamente (dif maxima 0,0, zero orfas
# dos dois lados) pela curva POLICY de `br_interest_rate` mais a de
# `inter_interest_rate`. O que sustenta a propriedade "nenhum numero gravado
# duas vezes" e a DISJUNCAO por pais, e ela nao tem sintoma nenhum se quebrar:
# gravar BR nas duas tabelas nao levanta erro, nao viola chave (as chaves sao
# de tabelas diferentes) e nao muda nenhum grafico -- so recria a duplicacao.


def test_cmb_policy_rates_nao_voltou_ao_registry():
    """A tabela saiu do registry junto com o script. Um arquivo novo que a
    declare de volta reintroduz a duplicacao sem nenhum outro sintoma."""
    from domain.db import registry

    assert "cmb_policy_rates" not in registry.tabelas()


def test_nenhum_modulo_le_cmb_policy_rates():
    """Le o codigo, nao o banco: a tabela pode continuar existindo no MySQL
    (dropar e decisao separada) e mesmo assim ninguem deve mais consultar."""
    import pathlib
    import re

    raiz = pathlib.Path(__file__).resolve().parents[1]
    # Aspas de proposito: casa a tabela sendo NOMEADA em codigo, nao a palavra
    # aparecendo em prosa de docstring/CLAUDE.md, que e historico legitimo.
    padrao = re.compile(r'["\']cmb_policy_rates["\']')
    culpados = []
    for py in sorted(raiz.rglob("*.py")):
        # `tests/` fica de fora porque e onde este proprio arquivo nomeia a
        # tabela para poder proibi-la -- incluir-se seria auto-reprovacao.
        if set(py.parts) & {".venv", "not_in_production", "tests"}:
            continue
        if padrao.search(py.read_text(encoding="utf-8", errors="replace")):
            culpados.append(str(py.relative_to(raiz)))
    assert not culpados, f"ainda consultam a tabela removida: {culpados}"


def test_a_policy_do_brasil_nao_aparece_na_tabela_internacional():
    """A disjuncao por pais e o que garante que nenhum numero mora duas vezes.
    BR tem schema proprio; duplica-lo no international daria duas linhas para o
    mesmo fato, com chaves diferentes e nenhum erro."""
    from connectors.mysql import MySQLDataRequester

    try:
        req = MySQLDataRequester("macro_international", "inter_interest_rate")
        req.connect()
        df = req.request_data()
        req.close_connection()
    except Exception as exc:                                       # noqa: BLE001
        pytest.skip(f"MySQL indisponivel: {exc}")

    paises = set(df[df["curve"] == "POLICY"]["country_code"].unique())
    assert "BR" not in paises, paises
    assert "US" not in paises, paises
    assert paises == {"MX", "CL", "CO", "PE", "AR"}, paises


# ---------------------------------------------------------------------------
# O cache nao pode gravar ausencia para o dia corrente
# ---------------------------------------------------------------------------
# A B3 solta o arquivo do pregao DEPOIS do fechamento. Pedido antes disso, o
# endpoint devolve um zip valido e vazio -- que e exatamente o que devolve num
# feriado estadual, e portanto passa pelo guarda de `sem_sessao`. Cachear esse
# vazio congela aquele pregao para sempre, porque a janela retroativa de `run()`
# le o cache e nunca rebusca.
#
# Nao e hipotese: medido em 2026-09-23. A tarefa agendada roda as 09:30 e
# envenenava o proprio dia todo dia, entao a curva ficou parada em 2026-09-14
# por 6 pregoes -- os seis com ~420 vertices na fonte o tempo todo. Nenhum erro,
# nenhuma excecao, e o log dizia "pregao sem arquivo na B3", que e a mensagem de
# uma ausencia legitima. O unico sintoma possivel era a data parar de andar.


def _grades_com_cache_falso(tmp_path, data, monkeypatch):
    """Roda grades() com CACHE isolado e a fonte devolvendo zip vazio."""
    from connectors import b3_curvas

    monkeypatch.setattr(b3_curvas, "CACHE", str(tmp_path))
    monkeypatch.setattr(b3_curvas, "_baixar_com_retry",
                        lambda yymmdd, tentativas=4: (None, True))
    out = b3_curvas.grades(data)
    return out, sorted(os.listdir(tmp_path))


def test_vazio_do_dia_corrente_nao_vai_para_o_cache(tmp_path, monkeypatch):
    import pandas as pd

    hoje = pd.Timestamp.today().normalize()
    out, arquivos = _grades_com_cache_falso(tmp_path, hoje, monkeypatch)
    assert out is None
    assert arquivos == [], (
        "gravou ausencia para o dia corrente: a proxima passagem leria este "
        f"arquivo e o pregao nunca mais seria rebuscado ({arquivos})")


def test_vazio_de_data_futura_tambem_nao_vai(tmp_path, monkeypatch):
    """A janela retroativa e por dia util, entao um feriado no meio pode fazer
    `bdate_range` alcancar amanha. Mesma regra, mesmo motivo."""
    import pandas as pd

    amanha = pd.Timestamp.today().normalize() + pd.Timedelta(days=1)
    out, arquivos = _grades_com_cache_falso(tmp_path, amanha, monkeypatch)
    assert out is None
    assert arquivos == []


def test_vazio_de_pregao_passado_CONTINUA_indo_para_o_cache(tmp_path, monkeypatch):
    """A metade que o guarda nao pode quebrar: os 43 feriados estaduais de SP
    sao ausencia de verdade, e cachea-los e o que evita 43 requisicoes por
    passe. 2026-09-07 (Independencia) e um deles."""
    import pandas as pd

    out, arquivos = _grades_com_cache_falso(
        tmp_path, pd.Timestamp("2026-09-07"), monkeypatch)
    assert out is None
    assert arquivos == ["260907.csv"]
