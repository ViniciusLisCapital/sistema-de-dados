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

from datetime import date

from domain.release_calendar.sync import (
    _divulgada_em,
    expectativas,
    periodo_para_data,
    sem_divulgacao,
)

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
print("\n" + "=" * 70)
if falhas:
    print(f"{len(falhas)} FALHA(S): {', '.join(falhas)}")
    raise SystemExit(1)
print("todos os testes passaram")
