# -*- coding: utf-8 -*-
"""
Testes da logica de expectativa do domain/release_calendar/sync.py.

Roda com:
    uv run python tests/test_sync_calendar.py

Nao toca no banco de proposito: tudo aqui exercita as funcoes puras contra um
calendario sintetico. A parte que fala com o MySQL (estado_banco) e uma unica
query e nao tem logica para testar; toda a subtileza esta em expectativas().

Segue o padrao do tests/test_ibge2.py: script executavel com asserts, nao pytest
(o projeto nao tem pytest configurado).
"""

from datetime import date, datetime
from datetime import time as dtime

from domain.release_calendar.sync import (
    _divulgada_em,
    _hora,
    hora_da_entrada,
    continuas,
    expectativas,
    periodo_para_data,
    sem_divulgacao,
)
from domain.release_calendar.update_calendar import _horas_por_data, _preencher_horas

falhas = []


def check(rotulo, obtido, esperado):
    ok = obtido == esperado
    print(f"  {'ok  ' if ok else 'FALHA'}  {rotulo}")
    if not ok:
        print(f"          esperado: {esperado!r}")
        print(f"          obtido  : {obtido!r}")
        falhas.append(rotulo)


# ---------------------------------------------------------------------------
# 1. reference_period -> data esperada de MAX(date)
# ---------------------------------------------------------------------------
print("\n1. periodo_para_data — as 4 formas que o campo tem no YAML")

check("mensal", periodo_para_data("2026-08"), date(2026, 8, 1))
check("trimestral Q1", periodo_para_data("2026-Q1"), date(2026, 1, 1))
check("trimestral Q2", periodo_para_data("2026-Q2"), date(2026, 4, 1))
check("trimestral Q4", periodo_para_data("2026-Q4"), date(2026, 10, 1))
check("data cheia (CFTC)", periodo_para_data("2026-08-11"), date(2026, 8, 11))
# texto livre -> None: reuniao de Copom/FOMC nao entrega periodo de dado
check("Copom (nao datavel)", periodo_para_data("281ª reunião"), None)
check("FOMC (nao datavel)", periodo_para_data("Sep 2026 (SEP)"), None)
check("vazio", periodo_para_data(None), None)
check("lixo", periodo_para_data("2026-13"), None)


# ---------------------------------------------------------------------------
# 2. quando a divulgacao conta como ocorrida
# ---------------------------------------------------------------------------
print("\n2. _divulgada_em — data simples, janela, e valor invalido")

check("data simples", _divulgada_em({"date": "2026-08-14"}), date(2026, 8, 14))
# janela (confirmed:false): so conta depois do FIM, senao gera atraso falso
# durante toda a janela
check("janela usa date_end",
      _divulgada_em({"date": "2026-08-10", "date_end": "2026-08-20"}),
      date(2026, 8, 20))
check("data ja parseada", _divulgada_em({"date": date(2026, 8, 14)}), date(2026, 8, 14))
check("invalida", _divulgada_em({"date": "quinta-feira"}), None)
check("ausente", _divulgada_em({}), None)


# ---------------------------------------------------------------------------
# 3. expectativas — calendario sintetico
# ---------------------------------------------------------------------------
print("\n3. expectativas — agregacao, futuro, grace, motivos")

DOC = {
    "no_release": ["tab_diaria"],
    "groups": [
        {   # mensal comum
            "group": "g_mensal", "institution": "IBGE", "tables": ["tab_a"],
            "entries": [
                {"date": "2026-07-10", "reference_period": "2026-06"},
                {"date": "2026-08-10", "reference_period": "2026-07"},
                {"date": "2026-09-10", "reference_period": "2026-08"},  # futuro
            ],
        },
        {   # segundo grupo sobre a MESMA tabela, exigindo menos
            "group": "g_fraco", "institution": "BCB", "tables": ["tab_a"],
            "entries": [{"date": "2026-08-01", "reference_period": "2026-03"}],
        },
        {   # grupo sem periodo datavel (Copom/FOMC)
            "group": "g_reuniao", "institution": "BCB", "tables": ["tab_b"],
            "entries": [{"date": "2026-08-05", "reference_period": "281ª reunião"}],
        },
        {   # grupo so com datas futuras (IBGE/Tesouro hoje)
            "group": "g_futuro", "institution": "MDIC", "tables": ["tab_c"],
            "entries": [{"date": "2026-09-04", "reference_period": "2026-08"}],
        },
    ],
}
AS_OF = date(2026, 8, 17)

exp, motivos = expectativas(DOC, AS_OF)

# vale a expectativa MAIS ALTA entre os grupos: 2026-07 do g_mensal, nao 2026-03
check("tabela em 2 grupos usa a maior", exp["tab_a"]["esperado"], date(2026, 7, 1))
check("  e credita o grupo certo", exp["tab_a"]["grupo"], "g_mensal")
check("divulgacao futura ignorada", exp["tab_a"]["divulgado_em"], date(2026, 8, 10))

# as duas causas distintas de "sem expectativa"
check("periodo nao datavel", motivos.get("tab_b"), "periodo nao datavel")
check("so datas futuras", motivos.get("tab_c"), "sem divulgacao passada no arquivo")
check("tab_b sem expectativa", "tab_b" in exp, False)
check("tab_c sem expectativa", "tab_c" in exp, False)

# grace: 8 dias para tras engole a divulgacao de 10/08, sobra a de 10/07
exp_g, _ = expectativas(DOC, AS_OF, grace=8)
check("grace recua a expectativa", exp_g["tab_a"]["esperado"], date(2026, 6, 1))

# no_release e uma lista declarada, nao inferida de "nao tem grupo"
check("no_release lido", sem_divulgacao(DOC), {"tab_diaria"})


# ---------------------------------------------------------------------------
# 4. expectation_overrides — os 3 modos
# ---------------------------------------------------------------------------
print("\n4. expectation_overrides — expect:none, lag_months, release_minus_days")

DOC_OVR = {
    "expectation_overrides": {
        "tab_a": {"lag_months": 1, "why": "sai um mes atras do resto da nota"},
        "tab_x": {"expect": "none", "why": "fonte tem calendario proprio"},
        "tab_semanal": {"release_minus_days": 3, "why": "coleta fecha na sexta"},
    },
    "groups": [
        {"group": "g_mensal", "institution": "BCB", "tables": ["tab_a", "tab_x"],
         "entries": [{"date": "2026-08-10", "reference_period": "2026-07"}]},
        # alta frequencia sem reference_period nenhum (o caso do Focus) + um grupo
        # trimestral sobre a mesma tabela, que era o que mascarava o atraso
        {"group": "g_semanal", "institution": "BCB", "tables": ["tab_semanal"],
         "entries": [{"date": "2026-08-10"}, {"date": "2026-08-17"},
                     {"date": "2026-08-24"}]},
        {"group": "g_trimestral", "institution": "BCB", "tables": ["tab_semanal"],
         "entries": [{"date": "2026-06-25", "reference_period": "2026-Q2"}]},
    ],
}

exp_o, motivos_o = expectativas(DOC_OVR, AS_OF)

# lag_months desloca a expectativa, nao desliga: 2026-07 -> 2026-06
check("lag_months desloca 1 mes", exp_o["tab_a"]["esperado"], date(2026, 6, 1))
check("  e registra o motivo", exp_o["tab_a"]["override"].startswith("-1m:"), True)

# expect:none remove a expectativa e explica
check("expect:none remove", "tab_x" in exp_o, False)
check("  com motivo", motivos_o["tab_x"].startswith("override:"), True)

# release_minus_days: ancora na DATA (17/08 - 3d), nao no trimestre (2026-04-01).
# Regressao do buraco real encontrado em 2026-08-17: sem isto, expc_focus ficava
# preso na expectativa trimestral do bcb_rpm e um Focus 2 semanas parado dava OK.
check("release_minus_days ancora na data",
      exp_o["tab_semanal"]["esperado"], date(2026, 8, 14))
check("  credita o grupo semanal", exp_o["tab_semanal"]["grupo"], "g_semanal")
check("  ignora entrada futura (24/08)",
      exp_o["tab_semanal"]["divulgado_em"], date(2026, 8, 17))
check("  e NAO usa o trimestre do outro grupo",
      exp_o["tab_semanal"]["esperado"] > date(2026, 4, 1), True)


# ---------------------------------------------------------------------------
# 5. max_age_days — conteudo diario cobrado contra HOJE, nao contra periodo
# ---------------------------------------------------------------------------
print("\n5. max_age_days — a regra que faltava para serie diaria")

DOC_AGE = {
    "no_release": {"continuous": ["tab_diaria"], "not_a_series": ["tab_dim"]},
    "max_age_days": {"tab_diaria": 5, "tab_mista": 5},
    "groups": [
        # tabela diaria pendurada num grupo MENSAL: era exatamente o caso do
        # cmb_cambio_contratado / cmb_reservas_bc em 2026-08-19, que passavam a
        # checagem com 2-3 semanas de atraso porque a nota mensal e frouxa
        {"group": "g_nota_mensal", "institution": "BCB", "tables": ["tab_mista"],
         "entries": [{"date": "2026-07-28", "reference_period": "2026-06"}]},
    ],
}

exp_a, motivos_a = expectativas(DOC_AGE, AS_OF)   # AS_OF = 2026-08-17

# serie continua (sem grupo nenhum) passa a TER expectativa: hoje - 5 dias
check("continua ganha expectativa", exp_a["tab_diaria"]["esperado"], date(2026, 8, 12))
check("  marcada como max_age", "max 5d" in (exp_a["tab_diaria"]["override"] or ""), True)
check("  sem divulgacao para citar", exp_a["tab_diaria"]["divulgado_em"], None)

# na tabela mista, a regra de idade (12/08) vence a da nota mensal (01/06)
check("max_age vence expectativa mensal frouxa",
      exp_a["tab_mista"]["esperado"], date(2026, 8, 12))
check("  e mantem o grupo que a cobre", exp_a["tab_mista"]["grupo"], "g_nota_mensal")

# grace afrouxa junto
exp_a2, _ = expectativas(DOC_AGE, AS_OF, grace=3)
check("grace afrouxa a idade", exp_a2["tab_diaria"]["esperado"], date(2026, 8, 9))

# continuas() = uniao de no_release.continuous com as chaves de max_age_days, menos
# not_a_series -- e o que traz a tabela mista para o passe diario
check("continuas() une as duas listas", continuas(DOC_AGE), ["tab_diaria", "tab_mista"])
check("continuas() exclui not_a_series", "tab_dim" not in continuas(DOC_AGE), True)

# sem o bloco, nada muda (compatibilidade com um YAML antigo)
DOC_SEM = {k: v for k, v in DOC_AGE.items() if k != "max_age_days"}
exp_s, _ = expectativas(DOC_SEM, AS_OF)
check("sem max_age_days a continua nao e cobrada", "tab_diaria" in exp_s, False)
check("  e a mista volta a expectativa mensal",
      exp_s["tab_mista"]["esperado"], date(2026, 6, 1))


# ---------------------------------------------------------------------------
# 6. hora da divulgacao — release_time no grupo, time na entrada
# ---------------------------------------------------------------------------
print("\n6. hora — o portao que evita cobrar o dado antes do anuncio")

check("hora valida", _hora("14:30"), __import__("datetime").time(14, 30))
check("hora sem zero a esquerda", _hora("9:05"), __import__("datetime").time(9, 5))
# valor malformado nao derruba a checagem: cai para "sem hora", igual reference_period
check("hora impossivel -> None", _hora("25:00"), None)
check("hora sem sentido -> None", _hora("14h30"), None)
check("vazio -> None", _hora(None), None)

HOJE = date(2026, 8, 20)
DOC_HORA = {
    "groups": [
        # grupo com hora propria, entrada sem hora -> vale a do grupo
        {"group": "g_grupo", "institution": "IBGE", "tables": ["tab_grupo"],
         "release_time": "09:00",
         "entries": [{"date": "2026-08-20", "reference_period": "2026-07"},
                     {"date": "2026-07-20", "reference_period": "2026-06"}]},
        # entrada com hora propria VENCE a do grupo (feed do BCB escreve aqui)
        {"group": "g_entrada", "institution": "BCB", "tables": ["tab_entrada"],
         "release_time": "09:00",
         "entries": [{"date": "2026-08-20", "time": "14:30", "reference_period": "2026-Q2"},
                     {"date": "2026-05-20", "time": "14:30", "reference_period": "2026-Q1"}]},
        # sem hora em lugar nenhum: comportamento antigo, vale desde a meia-noite
        {"group": "g_sem", "institution": "BCB", "tables": ["tab_sem"],
         "entries": [{"date": "2026-08-20", "reference_period": "2026-07"},
                     {"date": "2026-07-20", "reference_period": "2026-06"}]},
    ],
}


def esperado_as(hh, mm, tabela):
    exp, _ = expectativas(DOC_HORA, HOJE, agora=datetime(2026, 8, 20, hh, mm))
    return exp.get(tabela, {}).get("esperado")


check("antes da hora do grupo, vale a divulgacao anterior",
      esperado_as(8, 59, "tab_grupo"), date(2026, 6, 1))
check("na hora exata, passa a valer a de hoje",
      esperado_as(9, 0, "tab_grupo"), date(2026, 7, 1))

# o caso que motivou o campo: PTC as 14:30 nao pode ser cobrada as 9h da manha
check("PTC as 09:00 ainda cobra o trimestre anterior",
      esperado_as(9, 0, "tab_entrada"), date(2026, 1, 1))
check("PTC as 14:29 idem (limite)",
      esperado_as(14, 29, "tab_entrada"), date(2026, 1, 1))
check("PTC as 14:30 passa a cobrar o trimestre novo",
      esperado_as(14, 30, "tab_entrada"), date(2026, 4, 1))
check("PTC as 16:00 idem", esperado_as(16, 0, "tab_entrada"), date(2026, 4, 1))

check("sem hora, cobra desde a meia-noite",
      esperado_as(0, 1, "tab_sem"), date(2026, 7, 1))
# divulgacao de ontem nao depende de hora nenhuma
exp_h, _ = expectativas(DOC_HORA, date(2026, 8, 21), agora=datetime(2026, 8, 21, 0, 1))
check("divulgacao passada ignora a hora", exp_h["tab_grupo"]["esperado"], date(2026, 7, 1))

# fonte estrangeira: a hora e declarada no fuso DELA e convertida por entrada. Os EUA
# tem horario de verao e o Brasil nao desde 2019, entao a mesma hora da fonte cai em
# duas horas diferentes aqui ao longo do ano -- congelar um valor unico erraria por uma
# hora em metade do calendario, calado.
G_US = {"group": "cftc_cot", "release_time": "15:30",
        "release_time_tz": "America/New_York"}
check("15:30 ET no verao americano -> 16:30 aqui",
      hora_da_entrada({}, G_US, date(2026, 10, 30)), dtime(16, 30))
check("a MESMA 15:30 ET uma semana depois -> 17:30",
      hora_da_entrada({}, G_US, date(2026, 11, 6)), dtime(17, 30))
check("time da entrada tambem passa pela conversao",
      hora_da_entrada({"time": "14:00"}, G_US, date(2026, 12, 9)), dtime(16, 0))
check("grupo sem tz nao converte nada",
      hora_da_entrada({}, {"release_time": "15:00"}, date(2026, 11, 6)), dtime(15, 0))
# fuso com typo nao pode derrubar a checagem inteira
check("tz invalido cai para a hora crua",
      hora_da_entrada({}, {"group": "x", "release_time": "15:30",
                           "release_time_tz": "Nao/Existe"}, date(2026, 11, 6)),
      dtime(15, 30))
check("grupo sem horario nenhum", hora_da_entrada({}, {}, date(2026, 11, 6)), None)

# e o portao usa a hora CONVERTIDA, nao a da fonte
DOC_US = {"groups": [dict(G_US, tables=["tab_us"], entries=[
    {"date": "2026-11-06", "reference_period": "2026-11-03"},
    {"date": "2026-10-30", "reference_period": "2026-10-27"}])]}


def esperado_us(hh, mm):
    exp, _ = expectativas(DOC_US, date(2026, 11, 6),
                          agora=datetime(2026, 11, 6, hh, mm))
    return exp.get("tab_us", {}).get("esperado")


check("as 16:30 (hora da fonte + 1) ainda nao saiu",
      esperado_us(16, 30), date(2026, 10, 27))
check("as 17:30 saiu", esperado_us(17, 30), date(2026, 11, 3))



# ---------------------------------------------------------------------------
# 7. update_calendar — hora lida do feed ICS do BCB
# ---------------------------------------------------------------------------
print("\n7. _horas_por_data / _preencher_horas — o que vem do DTSTART")

D = date(2026, 8, 20)
check("hora do feed", _horas_por_data([{"date": D, "time": "14:30"}]), {D: "14:30"})
# 00:00 e placeholder de evento de dia inteiro (as 16 reunioes do Copom de 2026 sao
# assim); gravar como hora reproduziria o bug que a hora veio corrigir
check("00:00 e descartado, nao gravado",
      _horas_por_data([{"date": D, "time": "00:00"}]), {})
check("evento sem hora", _horas_por_data([{"date": D, "time": None}]), {})
# duas horas no mesmo dia: fica a mais tarde, para nao liberar antes de tudo sair
check("empate no mesmo dia fica com a mais tarde",
      _horas_por_data([{"date": D, "time": "08:30"}, {"date": D, "time": "14:00"}]),
      {D: "14:00"})


class _AgendaFake:
    def __init__(self, eventos):
        self._eventos = eventos

    def eventos(self, lista, start=None, end=None, summary_contains=None):
        return self._eventos


def _grupo_ruamel(entradas):
    from ruamel.yaml import YAML
    y = YAML()
    y.preserve_quotes = True
    doc = y.load("group: g\nics: {lista: L}\nentries:\n" + entradas)
    return doc


g = _grupo_ruamel('    - {date: "2026-08-20", reference_period: "2026-Q2", confirmed: true}\n')
mud = _preencher_horas(g, _AgendaFake([{"date": D, "time": "14:30"}]), D, D)
check("preenche a entrada existente", mud, [("2026-08-20", "sem hora", "14:30")])
# a ordem das chaves importa para o arquivo continuar legivel/diffavel
check("time entra logo depois de date",
      list(g["entries"][0].keys()), ["date", "time", "reference_period", "confirmed"])

# segunda passada nao mexe em nada (o --write e idempotente)
mud2 = _preencher_horas(g, _AgendaFake([{"date": D, "time": "14:30"}]), D, D)
check("segunda passada nao muda nada", mud2, [])

# nota escrita a mao sobrevive ao preenchimento
g2 = _grupo_ruamel('    - {date: "2026-08-20", note: "escrita a mao", confirmed: true}\n')
_preencher_horas(g2, _AgendaFake([{"date": D, "time": "14:30"}]), D, D)
check("nota a mao sobrevive", str(g2["entries"][0]["note"]), "escrita a mao")

# entrada que o feed nao cobre fica intacta
g3 = _grupo_ruamel('    - {date: "2026-08-20", confirmed: true}\n')
check("feed sem hora nao inventa nada",
      _preencher_horas(g3, _AgendaFake([{"date": D, "time": "00:00"}]), D, D), [])
check("  e nao cria a chave", "time" in g3["entries"][0], False)



# ---------------------------------------------------------------------------
print("\n" + "=" * 70)
if falhas:
    print(f"{len(falhas)} FALHA(S): {', '.join(falhas)}")
    raise SystemExit(1)
print("todos os testes passaram")
