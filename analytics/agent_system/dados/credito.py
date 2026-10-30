"""
As tabelas do agente de crédito (SISTEMA_AGENTES.md V.IX) e o F de cada uma.

A lista (quais tabelas) é decidida com o usuário e vive no SISTEMA_AGENTES.md; o gerador
levanta se esta declaração divergir dela. O tratamento (quais séries, que leitura) é do
sistema (IV.iv) e se ajusta pela qualidade do report.

Quatro coisas que valem para o arquivo inteiro:

  - As 11 `cred_*` que eram TWA na política monetária, na atividade e no fiscal nascem da
    declaração da política monetária (`de(pm, ...)`): a consulta e o arquivo de A são os mesmos
    e só as séries mudam (mais séries, a leitura que o mapa pede). Enquanto os outros agentes
    ainda as declaram, é isso que mantém `conferir_consultas` quieto; quando migrarem para
    `de(credito, ...)`, a declaração passa a ter dono. As três que ninguém declara
    (`cred_credito_porte`, `cred_credito_atividade_economica`, `cred_credito_tipo_cliente`) são
    declaradas aqui.
  - Tabela de outro agente sai da declaração do dono (`de` e `so`, do motor), trocando só as
    séries: a política monetária para a Selic e a curva, a atividade para o que ela declara, o
    mercado de trabalho para a `mt_*`, o fiscal para a `fisc_*`, a inflação para o IPCA, a
    expectativas para a Focus da Selic. O A do ciclo, que é compartilhado, serve a todos.
  - Profundidade (PRINCIPIOS I.II.vii): só o grupo "Endógeno" ganha a leitura completa. A
    `cred_credito_atividade_economica` e a `cred_credito_tipo_cliente` estão nele mas a lista as
    quer em leitura enxuta; o motor decide pelo nome do grupo, então elas levam um `especial`
    que a desliga.
  - A `cred_ptc` diz "−2 a +2", que é a escala do banco (COMMENT da coluna); a política monetária
    e a atividade ainda a rotulam "−1 a 1".

Quatro leituras combinadas respondem o que nenhuma tabela sozinha dá (mapa, 2.7 e 2.2): o
impulso de crédito pelo estoque (a variação do saldo sobre o PIB, contra a mesma conta um ano
antes); o impulso no conceito do BC, o fluxo financeiro contra o de 12 meses antes (que está
parado: o F diz até quando); as concessões em termos reais (o trimestre contra o mesmo
trimestre de um ano antes, deflacionadas pelo IPCA); e a contribuição de cada recurso e
segmento (livre/direcionado × PF/PJ) ao crescimento de 12 meses do saldo total. Mais uma, da
PTC: a surpresa, o que os bancos relataram contra o que esperavam no trimestre anterior (2.1).
"""

from __future__ import annotations

import dataclasses

import pandas as pd

from analytics.agent_system.dados import cambio, expectativas, fiscal, inflacao, mercado_trabalho
from analytics.agent_system.dados import politica_monetaria as pm
from analytics.agent_system.dados.motor import (Ctx, Serie, Tabela, antes, bloco_generico, de,
                                                fdata, fmt, md_tabela, so)

SECAO = ("## (V.IX) Agente de crédito", "*Fim das listas por agente.*")
PIB = None   # o PIB do impulso é o `pib_acum_12m` mensal, lido direto; não há fluxo em dólar aqui

_BI = 1000.0  # R$ milhões -> bilhões


def _s(chave, rotulo, unidade, leitura, **kw) -> Serie:
    return Serie(chave, rotulo, unidade, leitura, **kw)


def _enxuta(nome: str):
    """F genérico, mas na leitura enxuta: a lista quer assim para duas tabelas do grupo
    "Endógeno", que o motor leria por inteiro."""
    def f(df: pd.DataFrame, ctx: Ctx) -> list[str]:
        t = next(t for t in ctx.tabelas if t.nome == nome)
        return bloco_generico(t, df, dataclasses.replace(ctx, completo=False))
    f.__name__ = f"enxuta_{nome}"
    return f


# ── as séries ─────────────────────────────────────────────────────────────────
_RECURSOS = (("total", "total"), ("livre", "livre"), ("direcionado", "direcionado"))
_SEGMENTOS = (("total", None), ("pf", "PF"), ("pj", "PJ"))


def _resumo() -> tuple[Serie, ...]:
    """As 84 séries da `cred_credito_resumo`: recurso (total, livre, direcionado) × segmento
    (total, PF, PJ) para oito grandezas, mais o corte não rotativo de juros e spread."""
    def rot(base, rec, seg):
        nome = dict(_RECURSOS)[rec]
        return f"{base}: {nome}" + (f" {seg}" if seg else "")

    grandezas = (  # prefixo, rótulo, unidade, leitura, extras
        ("saldo", "Saldo", "R$ bi", "pct", {"escala": _BI, "casas": 0}),
        ("pct_pib", "Saldo em % do PIB", "% do PIB", "dif", {"casas": 1}),
        ("concessao", "Concessões", "R$ bi", "fluxo", {"escala": _BI, "casas": 1}),
        ("concessao_sa", "Concessões dessaz.", "R$ bi", "fluxo", {"escala": _BI, "casas": 1}),
        ("taxa_juros", "Taxa de juros", "% a.a.", "dif", {}),
        ("spread", "Spread", "p.p.", "dif", {}),
        ("icc", "Custo do crédito (ICC)", "% a.a.", "dif", {}),
        ("inadimplencia", "Inadimplência", "% da carteira", "dif", {}),
    )
    out = []
    for pre, base, unid, leit, kw in grandezas:
        for rec, _ in _RECURSOS:
            for seg, seg_rot in _SEGMENTOS:
                out.append(_s(f"{pre}_{rec}_{seg}", rot(base, rec, seg_rot), unid, leit, **kw))
    # o corte não rotativo (sem cartão rotativo e cheque especial): só juros e spread
    for pre, base, unid in (("taxa_juros", "Taxa de juros", "% a.a."), ("spread", "Spread", "p.p.")):
        for rec_chave, rec_rot in (("nao_rotativo", "total, não rotativo"),
                                   ("livre_nao_rotativo", "livre, não rotativo")):
            for seg, seg_rot in _SEGMENTOS:
                out.append(_s(f"{pre}_{rec_chave}_{seg}", f"{base}: {rec_rot}" + (f" {seg_rot}" if seg_rot else ""),
                              unid, "dif"))
    return tuple(out)


_RESUMO = _resumo()

_M4 = ("saldo", "concessao", "taxa_media", "inadimplencia")
_M2 = ("saldo", "concessao")
_M3_CARTAO_PJ = ("saldo", "concessao", "taxa_media")


def _mods(itens) -> tuple[Serie, ...]:
    """(modalidade, rótulo, métricas) -> séries, no formato da política monetária."""
    return pm._modalidade(tuple((mod, met, rot) for mod, rot, mets in itens for met in mets))


_LIVRE_PF = _mods((
    ("credito_pessoal_consignado_total", "Consignado", _M4),
    ("credito_pessoal_consignado_beneficiarios_do_inss", "Consignado INSS", _M4),
    ("credito_pessoal_consignado_servidores_publicos", "Consignado servidores", _M4),
    ("credito_pessoal_consignado_trabalhadores_setor_privado", "Consignado setor privado", _M4),
    ("credito_pessoal_nao_consignado_total", "Pessoal não consignado", _M4),
    ("aquisicao_de_veiculos", "Veículos", _M4),
    ("cartao_de_credito_a_vista", "Cartão à vista", _M2),
    ("cartao_de_credito_parcelado", "Cartão parcelado", _M4),
    ("cartao_de_credito_rotativo", "Cartão rotativo", _M4),
    ("cheque_especial", "Cheque especial", _M4),
    ("composicao_de_dividas", "Composição de dívidas", _M4),
))

_LIVRE_PJ = _mods((
    ("capital_de_giro_total", "Capital de giro", _M4),
    ("capital_de_giro_prazo_menor_365_dias", "Capital de giro até 365 dias", _M4),
    ("capital_de_giro_prazo_maior_365_dias", "Capital de giro acima de 365 dias", _M4),
    ("desconto_de_duplicatas_e_recebiveis", "Desconto de duplicatas e recebíveis", _M4),
    ("conta_garantida", "Conta garantida", _M4),
    ("acc", "ACC", _M4),
    ("financiamento_exportacoes", "Financiamento de exportações", _M4),
    ("financiamento_importacoes", "Financiamento de importações", _M4),
    ("cartao_de_credito_total", "Cartão", _M3_CARTAO_PJ),
    ("cheque_especial", "Cheque especial", _M4),
))

_DIRECIONADO_PF = _mods((
    ("financiamentos_imobiliarios_total", "Imobiliário", _M4),
    ("financiamentos_imobiliarios_taxas_de_mercado", "Imobiliário, taxas de mercado", _M4),
    ("financiamentos_imobiliarios_taxas_reguladas", "Imobiliário, taxas reguladas", _M4),
    ("credito_rural_total", "Rural", _M4),
    ("credito_rural_taxas_de_mercado", "Rural, taxas de mercado", _M4),
    ("credito_rural_taxas_reguladas", "Rural, taxas reguladas", _M4),
    ("credito_com_recursos_do_bndes_total", "BNDES", _M4),
    ("microcredito", "Microcrédito", _M4),
))

_DIRECIONADO_PJ = _mods((
    ("credito_com_recursos_do_bndes_total", "BNDES", _M4),
    ("credito_com_recursos_do_bndes_capital_de_giro", "BNDES, capital de giro", _M4),
    ("credito_com_recursos_do_bndes_financiamento_a_investimentos", "BNDES, investimento", _M4),
    ("credito_com_recursos_do_bndes_financiamento_agroindustrial", "BNDES, agroindustrial", _M4),
    ("credito_rural_total", "Rural", _M4),
    ("credito_rural_taxas_de_mercado", "Rural, taxas de mercado", _M4),
    ("credito_rural_taxas_reguladas", "Rural, taxas reguladas", _M4),
    ("financiamentos_imobiliarios_total", "Imobiliário", _M4),
    ("financiamentos_imobiliarios_taxas_de_mercado", "Imobiliário, taxas de mercado", _M4),
    ("financiamentos_imobiliarios_taxas_reguladas", "Imobiliário, taxas reguladas", _M4),
    ("programas_mpme", "Programas para MPME", _M4),
))

_CONTROLES = (("publicas", "bancos públicos"), ("privadas_nacionais", "privados nacionais"),
              ("estrangeiras", "estrangeiros"))
_CONTROLE_CAPITAL = (
    *[_s(f"{k}|saldo", f"Saldo: {rot}", "R$ bi", "pct", escala=_BI, casas=0) for k, rot in _CONTROLES],
    *[_s(f"{k}|inadimplencia", f"Inadimplência: {rot}", "% da carteira", "dif") for k, rot in _CONTROLES],
    *[_s(f"{k}|provisoes", f"Provisões: {rot}", "% da carteira", "dif") for k, rot in _CONTROLES],
)

_PORTE = (
    _s("grande|saldo", "Saldo: grandes empresas", "R$ bi", "pct", escala=_BI, casas=0),
    _s("mpme|saldo", "Saldo: MPME", "R$ bi", "pct", escala=_BI, casas=0),
    _s("grande|inadimplencia", "Inadimplência: grandes empresas", "% da carteira", "dif"),
    _s("mpme|inadimplencia", "Inadimplência: MPME", "% da carteira", "dif"),
    # quebra metodológica (Res. CMN 4.966): duas séries, sem sobreposição
    *[_s(f"{k}|saldo_maior_risco", f"Saldo de maior risco até 2024-12: {rot}", "% do saldo", "dif")
      for k, rot in (("total", "PJ"), ("grande", "grandes empresas"), ("mpme", "MPME"))],
    *[_s(f"{k}|saldo_maior_risco_res4966", f"Saldo de maior risco desde 2025-01: {rot}", "% do saldo", "dif")
      for k, rot in (("total", "PJ"), ("grande", "grandes empresas"), ("mpme", "MPME"))],
)

_ATIVIDADE = (
    ("agropecuaria", "Agropecuária"),
    ("industria_total", "Indústria, total"), ("industria_acucar", "Indústria: açúcar"),
    ("industria_alimentos", "Indústria: alimentos"), ("industria_automobilistica", "Indústria: automobilística"),
    ("industria_bens_capital", "Indústria: bens de capital"),
    ("industria_bens_consumo_nao_duraveis", "Indústria: bens de consumo não duráveis"),
    ("industria_construcao", "Indústria: construção"), ("industria_embalagens", "Indústria: embalagens"),
    ("industria_metalurgia_siderurgia", "Indústria: metalurgia e siderurgia"),
    ("industria_mineracao", "Indústria: mineração"),
    ("industria_obras_infraestrutura", "Indústria: obras de infraestrutura"),
    ("industria_outros_bens_consumo_duraveis", "Indústria: outros bens de consumo duráveis"),
    ("industria_papel_celulose", "Indústria: papel e celulose"),
    ("industria_petroleo_gas_alcool", "Indústria: petróleo, gás e álcool"),
    ("industria_quimica_farmaceutica", "Indústria: química e farmacêutica"),
    ("industria_siup", "Indústria: eletricidade, gás e água (SIUP)"),
    ("industria_textil_vestuario_couro_calcados", "Indústria: têxtil, vestuário, couro e calçados"),
    ("servicos_total", "Serviços, total"), ("servicos_administracao_publica", "Serviços: administração pública"),
    ("servicos_comercio", "Serviços: comércio"),
    ("servicos_comercio_atacado_bens_duraveis_nao_duraveis", "Serviços: comércio, atacado"),
    ("servicos_comercio_geral_bens_capital", "Serviços: comércio, bens de capital"),
    ("servicos_comercio_geral_bens_intermediarios", "Serviços: comércio, bens intermediários"),
    ("servicos_comercio_geral_veiculos_automotores", "Serviços: comércio, veículos"),
    ("servicos_comercio_varejo_bens_duraveis", "Serviços: comércio, varejo de duráveis"),
    ("servicos_comercio_varejo_bens_nao_duraveis", "Serviços: comércio, varejo de não duráveis"),
    ("servicos_demais_prestados_empresas", "Serviços: demais prestados a empresas"),
    ("servicos_demais_prestados_familias", "Serviços: demais prestados a famílias"),
    ("servicos_financeiros", "Serviços: financeiros"), ("servicos_imobiliarios", "Serviços: imobiliários"),
    ("servicos_informacao_comunicacao", "Serviços: informação e comunicação"),
    ("servicos_outros", "Serviços: outros"),
    ("servicos_transportes_dutoviario", "Serviços: transporte dutoviário"),
    ("servicos_transportes_meios_aquaviario_aereo", "Serviços: transporte aquaviário e aéreo"),
    ("servicos_transportes_total", "Serviços: transportes, total"),
    ("servicos_transportes_via_terrestre_carga_passageiro", "Serviços: transporte terrestre"),
    ("outros", "Outras atividades"),
)

_TIPO_CLIENTE = (
    ("total", "Total"), ("setor_privado_total", "Setor privado"), ("setor_privado_pf", "Setor privado: PF"),
    ("setor_privado_pj", "Setor privado: PJ"), ("setor_publico_total", "Setor público"),
    ("setor_publico_governo_federal", "Setor público: governo federal"),
    ("setor_publico_governos_estaduais_municipais", "Setor público: estados e municípios"),
)

_AMPLO = (
    ("emp_emprestimos_sfn", "Empresas: empréstimos do SFN"),
    ("emp_emprestimos_osf", "Empresas: empréstimos de outras instituições"),
    ("emp_emprestimos_fundos_gov", "Empresas: empréstimos de fundos públicos"),
    ("emp_titulos_divida_privado", "Empresas: títulos de dívida"),
    ("emp_titulos_divida_securitizado", "Empresas: títulos securitizados"),
    ("emp_divida_externa_mercado_int", "Empresas: dívida externa, mercado interno"),
    ("emp_divida_externa_mercado_ext", "Empresas: dívida externa, mercado externo"),
    ("fam_emprestimos_sfn", "Famílias: empréstimos do SFN"),
    ("fam_emprestimos_osf", "Famílias: empréstimos de outras instituições"),
    ("fam_emprestimos_fundos_gov", "Famílias: empréstimos de fundos públicos"),
    ("fam_titulos_securitizado", "Famílias: títulos securitizados"),
    ("fam_emprestimos_divida_externa", "Famílias: dívida externa"),
    ("gov_emprestimos_sfn", "Governo: empréstimos do SFN"),
    ("gov_titulos_publicos", "Governo: títulos públicos"),
    ("gov_divida_ext_mercado_interno", "Governo: dívida externa, mercado interno"),
    ("gov_divida_ext_mercado_externo", "Governo: dívida externa, mercado externo"),
    ("gov_emprestimos_divida_externa", "Governo: empréstimos, dívida externa"),
)

_UNID_PTC = "índice, −2 a +2"
_SEG_PTC = (("pfc", "PF consumo"), ("pfh", "PF habitação"), ("ge", "Grandes empresas"),
            ("mpme", "Micro, pequenas e médias"))
_PTC = tuple(
    _s(f"{seg}_{lado}_{hor}", f"{rot}: {lado}, {hor}", _UNID_PTC, "dif")
    for seg, rot in _SEG_PTC for lado in ("oferta", "demanda") for hor in ("observada", "esperada"))

_FAMILIAS = (
    _s("endividamento_renda", "Endividamento das famílias", "% da renda 12m", "dif"),
    _s("endividamento_sem_imob", "Endividamento sem imobiliário", "% da renda 12m", "dif"),
    _s("comp_renda_servico_total", "Comprometimento de renda: serviço total", "% da renda", "dif"),
    _s("comp_renda_servico_sem_imob", "Comprometimento de renda: serviço sem imobiliário", "% da renda", "dif"),
    _s("comp_renda_juros", "Comprometimento de renda: só juros", "% da renda", "dif"),
)

_INAD_PJ = (
    _s("inadimplencia_pj", "Inadimplência PJ (acima de 90 dias)", "% da carteira", "dif"),
    _s("atraso_pj", "Atraso PJ de 15 a 90 dias", "% da carteira", "dif"),
    _s("taxa_juros_pj", "Taxa de juros PJ", "% a.a.", "dif"),
    _s("concessao_credito_pj", "Concessões PJ", "R$ bi", "fluxo", escala=_BI, casas=1),
    _s("selic", "Selic (variável da política monetária, só leitura)", "% a.a.", "dif"),
)

_OF = "interna__gov_federal__creditos_inst_fin_oficiais"
_BNDES = _OF + "__creditos_bndes"
_DLSP = (
    _s(f"estoque|{_OF}", "Créditos do Tesouro às instituições financeiras oficiais, estoque (negativo = mais crédito)",
       "R$ bi", "dif", escala=_BI, casas=1),
    _s(f"estoque|{_BNDES}", "Créditos do Tesouro ao BNDES, estoque (negativo = mais crédito)",
       "R$ bi", "dif", escala=_BI, casas=1),
    _s(f"primario|{_OF}", "Créditos às instituições oficiais, fluxo primário do mês (negativo = crédito novo)",
       "R$ bi", "fluxo", escala=_BI, casas=1),
)

_RTN = (
    ("equalizacao_de_custeio_agropecuario", "Equalização de custeio agropecuário"),
    ("equalizacao_de_invest_rural_e_agroindustrial", "Equalização de investimento rural e agroindustrial"),
    ("pronaf_equalizacao_emprestimo_do_governo_federal", "Pronaf, equalização"),
    ("proex_equalizacao_emprestimo_do_governo_federal", "Proex, equalização"),
    ("equalizacao_dos_fundos_fda_fdne_fdco", "Equalização dos fundos regionais (FDA, FDNE, FDCO)"),
    ("impacto_primario_do_fies", "Impacto primário do FIES"),
    ("programa_de_subsidio_a_habitacao_de_interesse_social_psh", "Subsídio à habitação de interesse social (PSH)"),
    ("operacoes_de_microcredito_produtivo_orientado_eqmpo", "Microcrédito produtivo orientado (equalização)"),
    ("operacoes_de_credito_destinadas_a_pessoas_com_deficiencia_eqpcd", "Crédito a pessoas com deficiência (equalização)"),
)


# ── F próprio: a fluxo financeiro, que está parada ────────────────────────────
def fluxo_financeiro(df: pd.DataFrame, ctx: Ctx) -> list[str]:
    """A leitura padrão, mais a data do último dado dita por extenso: a série vem do anexo do
    RPM, e quando uma edição sai sem o gráfico a carga recarrega a última que o trouxe."""
    t = next(t for t in ctx.tabelas if t.nome == "cred_fluxo_financeiro")
    out = bloco_generico(t, df, ctx)
    ult = df["date"].max()
    meses = (ctx.corte.year - ult.year) * 12 + ctx.corte.month - ult.month
    ed = df["vintage"].max() if "vintage" in df else None
    aviso = (f"Último dado da série: {ult:%Y-%m}, {meses} meses antes do corte"
             + (f"; edição do RPM de {ed:%Y-%m}" if ed is not None and not pd.isna(ed) else "") + ". ")
    if meses > 4:
        aviso += ("**Série parada**: o anexo do RPM mais recente saiu sem o gráfico e a carga recarrega "
                  "a última edição que o trouxe. O impulso no conceito do BC não existe para os meses "
                  "depois dessa data; use o impulso pelo estoque (leitura combinada) e diga que esta série parou.")
    return out + ["", aviso]


# ── leituras combinadas ───────────────────────────────────────────────────────
def _ex(s: pd.Series, d) -> float | None:
    """O valor exatamente em `d` (o mês), ou None."""
    d = pd.Timestamp(d)
    return float(s[d]) if d in s.index else None


def _div(a, b, k=100.0):
    return None if a is None or b is None or not b else a / b * k


def _sub(a, b):
    return None if a is None or b is None else a - b


def impulso_estoque(ctx: Ctx) -> list[str]:
    """O impulso de crédito pelo estoque (mapa, 2.7): [S(t) − S(t−12)]/PIB12m(t) menos a mesma
    conta um ano antes, em p.p. do PIB. PF e PJ somam no total porque o saldo soma e o PIB é o
    mesmo. Vai até onde vai o PIB mensal. Nada corrige variação cambial do saldo atrelado ao
    dólar nem o crédito fora do SFN."""
    tit = "### O impulso de crédito pelo estoque"
    pib = ctx.serie("atv_pib_mensal", "pib_acum_12m")
    sal = {k: ctx.serie("cred_credito_resumo", f"saldo_total_{k}") for k in ("total", "pf", "pj")}
    if pib.empty or any(s.empty for s in sal.values()):
        return [tit, "", "Sem dado no corte."]
    fim = min(pib.index[-1], *[s.index[-1] for s in sal.values()])

    def imp(s, t):
        a = _div(_sub(_ex(s, t), _ex(s, antes(t, 12))), _ex(pib, t))
        b = _div(_sub(_ex(s, antes(t, 12)), _ex(s, antes(t, 24))), _ex(pib, antes(t, 12)))
        return a, _sub(a, b)

    linhas = []
    for t in pd.date_range(end=fim, periods=6, freq="MS")[::-1]:
        a, i_t = imp(sal["total"], t)
        _, i_pf = imp(sal["pf"], t)
        _, i_pj = imp(sal["pj"], t)
        linhas.append({"Mês": f"{t:%Y-%m}", "Impulso total (p.p. do PIB)": fmt(i_t, 2, True),
                       "PF": fmt(i_pf, 2, True), "PJ": fmt(i_pj, 2, True),
                       "Δ saldo 12m (% do PIB)": fmt(a, 2, True),
                       "Δ saldo 12m, um ano antes (% do PIB)": fmt(None if a is None or i_t is None else a - i_t, 2, True)})
    return [f"{tit}, até {fdata(fim)}", "",
            "Impulso = [S(t) − S(t−12)] ÷ PIB nominal de 12 meses(t) − a mesma razão um ano antes, em p.p. do "
            "PIB; positivo = o crédito acelera. S é o saldo total do SFN. PF e PJ somam no total. O PIB mensal "
            "é nominal, e o saldo do crédito atrelado ao dólar se move com o câmbio sem que ninguém tenha "
            "emprestado mais ou menos.", ""] + md_tabela(linhas)


def impulso_fluxo(ctx: Ctx) -> list[str]:
    """O impulso no conceito do BC (mapa, 2.7): fluxo(t) − fluxo(t−12), com o fluxo em % do PIB
    de 12 meses. A série está parada; a tabela diz até quando."""
    tit = "### O impulso de crédito no conceito do BC (fluxo financeiro)"
    f = {k: ctx.serie("cred_fluxo_financeiro", f"fluxo_{k}") for k in ("total", "pf", "pj")}
    if any(s.empty for s in f.values()):
        return [tit, "", "Sem dado no corte."]
    fim = min(s.index[-1] for s in f.values())
    meses = (ctx.corte.year - fim.year) * 12 + ctx.corte.month - fim.month
    linhas = []
    for t in pd.date_range(end=fim, periods=6, freq="MS")[::-1]:
        row = {"Mês": f"{t:%Y-%m}"}
        for k, rot in (("total", "Impulso total"), ("pf", "PF"), ("pj", "PJ")):
            row[rot + (" (p.p. do PIB)" if k == "total" else "")] = fmt(
                _sub(_ex(f[k], t), _ex(f[k], antes(t, 12))), 1, True)
        row["Fluxo total (% do PIB, 12m)"] = fmt(_ex(f["total"], t), 1)
        linhas.append(row)
    parada = (f" **A série está parada em {fim:%Y-%m}**, {meses} meses antes do corte: para os meses "
              "seguintes use o impulso pelo estoque e diga isso." if meses > 4 else "")
    return [f"{tit}, até {fim:%Y-%m}", "",
            "Impulso = fluxo(t) − fluxo(t−12), em p.p. do PIB (fluxo = concessões − pagamentos, % do PIB "
            "acumulado em 12 meses; fonte: anexo do RPM)." + parada, ""] + md_tabela(linhas)


_CORTES = (("concessao_total_total", "Total"), ("concessao_livre_total", "Livre"),
           ("concessao_direcionado_total", "Direcionado"), ("concessao_total_pf", "PF"),
           ("concessao_total_pj", "PJ"))


def concessoes_reais(ctx: Ctx) -> list[str]:
    """As concessões em termos reais (mapa, a candidata (b) da tese): a soma de três meses
    deflacionada pelo IPCA contra a soma dos mesmos três meses um ano antes. Comparar com o mesmo
    trimestre do ano anterior tira a sazonalidade sem precisar da série dessazonalizada."""
    tit = "### As concessões em termos reais"
    v = ctx.serie("inflc_agregados", "ipca")
    cs = {k: ctx.serie("cred_credito_resumo", k) for k, _ in _CORTES}
    if v.empty or any(s.empty for s in cs.values()):
        return [tit, "", "Sem dado no corte."]
    fim = min(v.index[-1], *[s.index[-1] for s in cs.values()])
    idx = (1 + v / 100).cumprod()                       # nível do IPCA, base arbitrária
    base = float(idx[fim])

    def soma3(s, t, real):
        meses = pd.date_range(end=t, periods=3, freq="MS")
        if any(m not in s.index or m not in idx.index for m in meses):
            return None
        return float(sum(s[m] / (idx[m] / base if real else 1.0) for m in meses))

    def var(a, b):
        return None if a is None or b is None or not b else (a / b - 1) * 100

    linhas = []
    for k, rot in _CORTES:
        s, t0 = cs[k], antes(fim, 12)
        r1, r0, n1, n0 = soma3(s, fim, True), soma3(s, t0, True), soma3(s, fim, False), soma3(s, t0, False)
        linhas.append({"Corte": rot,
                       "3 meses, real (R$ bi)": fmt(None if r1 is None else r1 / _BI, 1),
                       "Mesmos 3 meses um ano antes, real (R$ bi)": fmt(None if r0 is None else r0 / _BI, 1),
                       "Δ% real": fmt(var(r1, r0), 1, True), "Δ% nominal": fmt(var(n1, n0), 1, True)})
    hist = []
    for t in pd.date_range(end=fim, periods=6, freq="MS")[::-1]:
        s = cs["concessao_total_total"]
        hist.append({"Mês (fim dos 3 meses)": f"{t:%Y-%m}",
                     "Δ% real, total": fmt(var(soma3(s, t, True), soma3(s, antes(t, 12), True)), 1, True),
                     "Δ% nominal, total": fmt(var(soma3(s, t, False), soma3(s, antes(t, 12), False)), 1, True)})
    return [f"{tit}, três meses até {fdata(fim)}", "",
            f"Concessões de três meses (R$ bilhões, preços de {fim:%Y-%m}, deflacionadas pelo IPCA) contra os "
            "mesmos três meses de um ano antes. Sem ajuste sazonal: a comparação com o mesmo trimestre do "
            "ano anterior já o neutraliza.", ""] + md_tabela(linhas) + [""] + md_tabela(hist)


_BLOCOS = (("saldo_livre_pf", "Livre PF"), ("saldo_livre_pj", "Livre PJ"),
           ("saldo_direcionado_pf", "Direcionado PF"), ("saldo_direcionado_pj", "Direcionado PJ"))


def contribuicoes_saldo(ctx: Ctx) -> list[str]:
    """A decomposição do saldo (pedido explícito do usuário): a contribuição de cada recurso e
    segmento ao crescimento de 12 meses do saldo total, (Sᵢ(t) − Sᵢ(t−12)) ÷ S_total(t−12), em
    p.p. As quatro somam o crescimento do total porque o saldo total é a soma delas."""
    tit = "### Quem puxa o crescimento do saldo de crédito"
    tot = ctx.serie("cred_credito_resumo", "saldo_total_total")
    bl = {k: ctx.serie("cred_credito_resumo", k) for k, _ in _BLOCOS}
    if tot.empty or any(s.empty for s in bl.values()):
        return [tit, "", "Sem dado no corte."]
    fim = min(tot.index[-1], *[s.index[-1] for s in bl.values()])
    linhas = []
    for t in pd.date_range(end=fim, periods=6, freq="MS")[::-1]:
        t0 = antes(t, 12)
        base = _ex(tot, t0)
        g = _div(_sub(_ex(tot, t), base), base)
        cs = [_div(_sub(_ex(bl[k], t), _ex(bl[k], t0)), base) for k, _ in _BLOCOS]
        soma = None if any(c is None for c in cs) else float(sum(cs))
        row = {"Mês": f"{t:%Y-%m}", "Saldo total, Δ% 12m": fmt(g, 2, True)}
        row.update({rot: fmt(c, 2, True) for (_, rot), c in zip(_BLOCOS, cs)})
        row["Soma"] = fmt(soma, 2, True)
        row["Resíduo"] = fmt(_sub(g, soma), 2, True)
        linhas.append(row)
    return [f"{tit}, 12 meses até {fdata(fim)}", "",
            "Contribuição em p.p. ao crescimento de 12 meses do saldo total do SFN; livre e direcionado × PF "
            "e PJ somam o total (o resíduo é arredondamento da fonte). O direcionado é a metade da política; "
            "o livre responde ao preço.", ""] + md_tabela(linhas)


def ptc_surpresa(ctx: Ctx) -> list[str]:
    """A surpresa da PTC (mapa, 2.1): o que os bancos relataram contra o que esperavam, um
    trimestre antes. A escala é a do banco, −2 a +2, média simples das respostas."""
    tit = "### PTC: o observado contra o esperado"
    linhas = []
    fim = None
    for seg, rot in _SEG_PTC:
        for lado in ("oferta", "demanda"):
            o = ctx.serie("cred_ptc", f"{seg}_{lado}_observada")
            e = ctx.serie("cred_ptc", f"{seg}_{lado}_esperada")
            if o.empty or e.empty:
                continue
            t = o.index[-1]
            fim = t if fim is None else max(fim, t)
            ant = _ex(e, antes(t, 3))
            linhas.append({"Segmento": rot, "Lado": lado, "Trimestre": f"{t:%Y-%m}",
                           "Observado": fmt(float(o.iloc[-1]), 2, True),
                           "Esperado um trimestre antes": fmt(ant, 2, True),
                           "Surpresa": fmt(_sub(float(o.iloc[-1]), ant), 2, True),
                           "Esperado para o próximo": fmt(_ex(e, t), 2, True)})
    if not linhas:
        return [tit, "", "Sem dado no corte."]
    return [tit, "",
            "Escala de −2 a +2 (média simples das respostas dos bancos): positivo em oferta = aprovação mais "
            "frouxa, positivo em demanda = procura maior. Surpresa = observado − o que se esperava no "
            "trimestre anterior. Painéis pequenos e de tamanhos diferentes: o valor anda em múltiplos de 1/N.",
            ""] + md_tabela(linhas)


COMBINADAS = [impulso_estoque, impulso_fluxo, concessoes_reais, contribuicoes_saldo, ptc_surpresa]


# ── a declaração ──────────────────────────────────────────────────────────────
TABELAS: list[Tabela] = [
    # ── i. Endógeno (leitura completa) ───────────────────────────────────────
    de(pm, "cred_credito_resumo", series=_RESUMO),
    de(pm, "cred_modalidade_livre_pf", series=_LIVRE_PF),
    de(pm, "cred_modalidade_livre_pj", series=_LIVRE_PJ),
    de(pm, "cred_modalidade_direcionado_pf", series=_DIRECIONADO_PF),
    de(pm, "cred_modalidade_direcionado_pj", series=_DIRECIONADO_PJ),
    de(pm, "cred_credito_controle_capital", series=_CONTROLE_CAPITAL),
    Tabela("cred_credito_porte", dims=("porte", "metrica"), series=_PORTE,
           nota="Quebra metodológica no saldo de maior risco: a série até 2024-12 e a desde 2025-01 "
                "(Res. CMN 4.966) não têm sobreposição e não se comparam em nível."),
    Tabela("cred_credito_atividade_economica", especial=_enxuta("cred_credito_atividade_economica"),
           series=tuple(_s(k, rot, "R$ bi", "pct", escala=_BI, casas=1) for k, rot in _ATIVIDADE)),
    Tabela("cred_credito_tipo_cliente", especial=_enxuta("cred_credito_tipo_cliente"),
           series=tuple(_s(k, rot, "R$ bi", "pct", escala=_BI, casas=0) for k, rot in _TIPO_CLIENTE)),
    de(pm, "cred_credito_amplo", series=tuple(_s(k, rot, "R$ bi", "pct", escala=_BI, casas=0)
                                              for k, rot in _AMPLO),
       nota="Universo diferente do crédito do SFN: as duas bases não reconciliam."),
    de(pm, "cred_ptc", series=_PTC),
    de(pm, "cred_fluxo_financeiro", especial=fluxo_financeiro),
    de(pm, "cred_credito_familias", series=_FAMILIAS),
    de(pm, "cred_inadimplencia_pj", series=_INAD_PJ),
    # ── ii. Endógeno de política monetária ───────────────────────────────────
    de(pm, "pm_copom_reuniao"),
    so(pm, "br_interest_rate", ("POLICY|1d", "DIPRE|12M", "DIPRE|24M")),
    # ── iii. Endógeno de atividade ───────────────────────────────────────────
    de(pm, "pm_hiato_produto"),
    de(pm, "atv_pib_mensal", series=(
        _s("pib_acum_12m", "PIB nominal, 12 meses", "R$ bi", "pct", escala=_BI, casas=0),
        _s("pib_mensal", "PIB nominal, mês", "R$ bi", "fluxo", escala=_BI, casas=1))),
    so(pm, "atv_pib", ("pib_pm|Y", "consumo_familias|Y", "fbcf|Y")),
    so(pm, "atv_pmc", ("comercio_restrito_total|Y", "veiculos_motocicletas_pecas|Y",
                       "moveis_eletrodomesticos|Y")),
    so(pm, "atv_pim_uso", ("bens_consumo_duraveis|Y", "bens_capital|Y")),
    # ── iv. Endógeno de inflação ─────────────────────────────────────────────
    de(inflacao, "inflc_agregados", especial=None,
       series=(_s("ipca", "IPCA", "%", "var_mensal"),)),
    # ── v. Endógeno de mercado de trabalho ───────────────────────────────────
    so(mercado_trabalho, "mt_pnad", ("ocupado", "taxa_informalidade", "rend_habitual_real_todos_trabalhos",
                                     "massa_real_habitual")),
    so(mercado_trabalho, "mt_caged", ("caged_total",)),
    # ── vi. Endógeno de fiscal ───────────────────────────────────────────────
    de(fiscal, "fisc_dlsp_fatores", especial=None, dims=("fator", "item"), series=_DLSP,
       nota="Convenção da tabela: fluxo positivo AUMENTA a dívida líquida; um crédito do governo é ativo "
            "e aparece negativo."),
    de(fiscal, "fisc_rtn", especial=None, series=tuple(
        _s(k, rot, "R$ bi", "fluxo", escala=_BI, casas=1) for k, rot in _RTN)),
    # ── vii. Endógeno de expectativas ────────────────────────────────────────
    de(expectativas, "expc_focus_periodo", recorte="Selic"),
    de(cambio, "expc_focus_periodo", recorte="IPCA"),
    # ── viii. Endógeno de câmbio ─────────────────────────────────────────────
    so(cambio, "cmb_ptax", ("ptax_venda",)),
]
