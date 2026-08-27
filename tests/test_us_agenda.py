# -*- coding: utf-8 -*-
"""
Testes do connectors/us_agenda.py e da agenda que ele alimenta no calendario.

Roda com:
    uv run python tests/test_us_agenda.py            # offline + ao vivo
    uv run python tests/test_us_agenda.py --offline  # so as funcoes puras

Padrao dos demais testes daqui: script executavel com asserts, nao pytest.

Duas metades, e elas cobrem riscos diferentes:

1. **Offline** — os parsers contra fixtures curtas escritas a mao. E aqui que
   moram as tres armadilhas de formato que custaram uma rodada de depuracao cada:
   o TZID nao-IANA do BLS (`US-Eastern`), o UTC com `Z` do BEA (que carrega o
   horario de verao, e cuja leitura ingenua erra em 4-5 horas) e o line-folding
   do RFC 5545 no meio de uma palavra do titulo, que e onde vive o periodo de
   referencia.

2. **Ao vivo** — as tres fontes uma contra a outra. Um parser de HTML/ICS de
   terceiro nao quebra com excecao, ele para de achar linha e devolve lista vazia
   ou meia agenda. A conferencia BLS-pagina x BLS-ICS x FRED (e BEA-ICS x
   BEA-HTML x FRED) e o que transforma isso em falha barulhenta.
"""

from __future__ import annotations

import sys
from datetime import date, datetime

from connectors.us_agenda import (
    BEAAgenda,
    BLSAgenda,
    FREDReleases,
    _parse_ics,
    periodo_referencia,
)
from domain.release_calendar.sync import agenda_da_tabela, agenda_das_tabelas

falhas: list[str] = []


def ok(cond, msg, extra=None):
    if cond:
        print(f"  ok   {msg}")
    else:
        falhas.append(msg)
        print(f"  FALHA {msg}" + (f"  -> {extra}" if extra is not None else ""))


# ---------------------------------------------------------------------- offline

_ICS_BLS = "\r\n".join([
    "BEGIN:VCALENDAR",
    "PRODID:-//Department of Labor//Bureau of Labor Statistics//EN",
    "X-WR-TIMEZONE:US-Eastern",
    "BEGIN:VEVENT",
    "UID:a",
    "DTSTART;TZID=US-Eastern:20260911T083000",
    "SUMMARY:Consumer Price Index",
    "END:VEVENT",
    "BEGIN:VEVENT",
    "UID:b",
    "DTSTART;TZID=US-Eastern:20261210T083000",
    "SUMMARY:Consumer Price Index",
    "END:VEVENT",
    "END:VCALENDAR",
])

# DTSTART em UTC, com o titulo dobrado no meio de uma palavra -- as duas coisas
# como o BEA emite de verdade.
_ICS_BEA = "\r\n".join([
    "BEGIN:VCALENDAR",
    "PRODID://BEA-Release-Calendar-Subscription//",
    "BEGIN:VEVENT",
    "SUMMARY:Personal Income and Outlays\\, August 2026",
    "DTSTART;VALUE=DATE-TIME:20260930T123000Z",
    "UID:c",
    "END:VEVENT",
    "BEGIN:VEVENT",
    "SUMMARY:Gross Domestic Product\\, 4th Quarter and Year 2026 (Advance Estima",
    " te)",
    "DTSTART;VALUE=DATE-TIME:20261125T133000Z",
    "UID:d",
    "END:VEVENT",
    "END:VCALENDAR",
])


def teste_offline():
    print("\n1. parsing do ICS do BLS (TZID nao-IANA)")
    ev = _parse_ics(_ICS_BLS)
    ok(len(ev) == 2, "os dois VEVENTs foram lidos", len(ev))
    ok(ev[0]["date"] == date(2026, 9, 11), "a data sai certa", ev[0]["date"])
    # `US-Eastern` nao existe no tzdata; sem o alias, ZoneInfo levantaria e a hora
    # cairia para o fallback. 08:30 tem de sobreviver como 08:30 local da fonte.
    ok(ev[0]["time"] == "08:30", "e a hora tambem, apesar do TZID nao ser IANA", ev[0]["time"])
    ok(ev[0]["tz"] == "America/New_York", "normalizado para o nome IANA", ev[0]["tz"])

    print("\n2. parsing do ICS do BEA (UTC com Z + line-folding)")
    ev = _parse_ics(_ICS_BEA)
    ok(len(ev) == 2, "os dois VEVENTs foram lidos", len(ev))
    # 12:30Z em setembro e EDT (UTC-4) -> 08:30. Ler como ingenuo daria 12:30.
    ok(ev[0]["time"] == "08:30", "12:30Z em setembro vira 08:30 (EDT)", ev[0]["time"])
    # 13:30Z em novembro ja e EST (UTC-5) -> tambem 08:30. As duas sao a mesma hora
    # de parede, e e isso que um valor unico congelado nao conseguiria representar.
    ok(ev[1]["time"] == "08:30", "13:30Z em novembro tambem vira 08:30 (EST)", ev[1]["time"])
    ok(ev[0]["summary"] == "Personal Income and Outlays, August 2026",
       "o escaping de virgula do RFC 5545 foi desfeito", ev[0]["summary"])
    ok(ev[1]["summary"].endswith("(Advance Estimate)"),
       "e a linha dobrada no meio da palavra foi remontada", ev[1]["summary"][-30:])

    print("\n3. periodo de referencia a partir de texto livre")
    casos = [
        ("Personal Income and Outlays, August 2026", "2026-08"),
        ("November 2025", "2025-11"),
        ("Dec. 2025", "2025-12"),
        ("Third Quarter 2025", "2025-Q3"),
        ("GDP (Advance Estimate), 3rd Quarter 2026", "2026-Q3"),
        # Release anual: sem periodo datavel de proposito -- sync.periodo_para_data
        # so data mensal/trimestral/diario, e um None aqui vira "sem expectativa",
        # que e o correto (nao ha o que cobrar do banco todo mes).
        ("Consumer Expenditures, 2024", None),
        ("", None),
    ]
    for texto, esperado in casos:
        got = periodo_referencia(texto)
        ok(got == esperado, f"{texto[:44]!r} -> {esperado}", got)


# ------------------------------------------------------------------------ vivo


def teste_vivo():
    print("\n4. BLS ao vivo: pagina de agenda x feed ICS")
    bls = BLSAgenda()
    slugs = bls.releases()
    ok("cpi" in slugs and "ppi" in slugs and len(slugs) >= 10,
       f"{len(slugs)} releases com pagina propria", slugs[:6])

    sched = bls.schedule("cpi")
    ok(len(sched) >= 10, f"a agenda do CPI tem {len(sched)} linhas", len(sched))
    ok(all(e["reference_period"] for e in sched),
       "todas com periodo de referencia (a coluna que so a pagina tem)")
    ok(all(e["time"] for e in sched), "e todas com hora")
    # O periodo e o mes anterior ao da divulgacao no CPI. Nao e assumido pelo
    # codigo (e LIDO), mas se deixasse de valer aqui o parser estaria pareando
    # colunas erradas -- e o sintoma seria exatamente este.
    ok(all(e["reference_period"] < e["date"].isoformat()[:7] for e in sched),
       "e cada periodo antecede o mes da divulgacao")

    ics = {e["date"]: e["time"] for e in bls.eventos(summary_contains="Consumer Price Index")}
    comuns = [e for e in sched if e["date"] in ics]
    ok(len(comuns) >= 5, f"{len(comuns)} datas em comum entre pagina e ICS", len(comuns))
    divergentes = [e["date"] for e in comuns if ics[e["date"]] != e["time"]]
    ok(not divergentes, "e a hora bate em todas", divergentes)

    print("\n5. BEA ao vivo: feed ICS x pagina HTML")
    bea = BEAAgenda()
    pio = bea.eventos(summary_starts="Personal Income and Outlays")
    ok(len(pio) >= 12, f"{len(pio)} divulgacoes de Personal Income and Outlays", len(pio))
    ok(all(e["reference_period"] for e in pio),
       "todas com periodo, vindo do proprio titulo do evento")

    html = {e["date"]: e for e in bea.schedule()
            if e["summary"].startswith("Personal Income and Outlays")}
    sobrepostas = [e for e in pio if e["date"] in html]
    ok(len(sobrepostas) >= 3, f"{len(sobrepostas)} datas futuras em comum com o HTML",
       len(sobrepostas))
    ruins = [(e["date"], e["time"], html[e["date"]]["time"])
             for e in sobrepostas if html[e["date"]]["time"] != e["time"]]
    ok(not ruins, "e a hora bate em todas", ruins)
    ruins = [(e["date"], e["reference_period"], html[e["date"]]["reference_period"])
             for e in sobrepostas
             if html[e["date"]]["reference_period"] != e["reference_period"]]
    ok(not ruins, "e o periodo tambem", ruins)

    print("\n6. FRED como terceira opiniao")
    fred = FREDReleases()
    ok([r["id"] for r in fred.release_for_series("CPIAUCSL")] == [10],
       "CPIAUCSL pertence ao release 10")
    ok([r["id"] for r in fred.release_for_series("PCEPI")] == [54],
       "PCEPI pertence ao release 54")
    # A conferencia e DIRECIONAL, e a direcao e o que importa: toda data que a
    # agencia agenda tem de existir no FRED (o contrario seria data inventada pelo
    # nosso parser). O inverso NAO vale, e nao e defeito: um "release" do FRED e o
    # conjunto de publicacoes que mexem naquelas series, e o release 54 inclui as
    # divulgacoes trimestrais de PIB, que republicam o indice de preco do PCE sem
    # se chamarem "Personal Income and Outlays" -- medido em 2026-08-26, o FRED tem
    # 2025-12-23 (GDP 3T25, estimativa inicial) e a agenda do BEA, por titulo, nao.
    for rid, agenda, nome in ((10, sched, "CPI"), (54, pio, "PCE")):
        # `futuras=True` e o que traz as datas ja agendadas mas ainda sem dado; sem
        # esse parametro o FRED devolve so o passado e a conferencia do futuro --
        # que e a parte que interessa -- nao aconteceria.
        do_fred = set(fred.dates(rid))
        minhas = {e["date"] for e in agenda}
        faltando = sorted(minhas - do_fred)
        ok(not faltando, f"toda data de {nome} da agencia existe no FRED", faltando)
        extras = sorted(d for d in do_fred - minhas if min(minhas) <= d <= max(minhas))
        print(f"       ({nome}: {len(extras)} data(s) so no FRED na janela"
              + (f" -- {extras}" if extras else "") + ")")

    print("\n7. a agenda que chega ao relatorio")
    ag = agenda_das_tabelas(["inflc_cpi", "inflc_pce"])
    ok(set(ag) == {"inflc_cpi", "inflc_pce"}, "as duas series tem agenda", sorted(ag))
    ok(ag["inflc_cpi"]["institution"] == "BLS"
       and ag["inflc_pce"]["institution"] == "BEA",
       "cada uma com a sua instituicao")
    for t, info in ag.items():
        p = info["proxima"]
        ok(p is not None and p["confirmed"],
           f"{t}: a proxima divulgacao esta agendada e confirmada")
        ok(p["tz_fonte"] == "America/New_York",
           f"{t}: a hora e guardada no fuso da FONTE", p["tz_fonte"])

    # Fronteira de horario de verao. A mesma 08:30 de Nova York tem de cair em duas
    # horas diferentes de Brasilia ao longo do ano, e e por isso que o YAML guarda
    # release_time_tz em vez de um valor ja convertido.
    print("\n8. a conversao de fuso muda com o horario de verao americano")
    verao = agenda_da_tabela("inflc_cpi", agora=datetime(2026, 9, 1, 12, 0))
    inverno = agenda_da_tabela("inflc_cpi", agora=datetime(2026, 12, 1, 12, 0))
    ok(verao["proxima"]["time_fonte"] == inverno["proxima"]["time_fonte"] == "08:30",
       "a hora da fonte e a mesma nas duas pontas do ano")
    ok(verao["proxima"]["time_local"] == "09:30",
       "em setembro (EDT) sai 09:30 em Brasilia", verao["proxima"]["time_local"])
    ok(inverno["proxima"]["time_local"] == "10:30",
       "em dezembro (EST) sai 10:30", inverno["proxima"]["time_local"])

    # Fronteira do dia da divulgacao: antes da hora a divulgacao ainda e FUTURA.
    print("\n9. no dia da divulgacao, a hora decide de que lado ela cai")
    dia = date.fromisoformat(verao["proxima"]["date"])
    antes = agenda_da_tabela("inflc_cpi", agora=datetime.combine(dia, datetime.min.time()).replace(hour=8))
    depois = agenda_da_tabela("inflc_cpi", agora=datetime.combine(dia, datetime.min.time()).replace(hour=11))
    ok(antes["proxima"]["date"] == dia.isoformat(),
       "as 08:00 de Brasilia ela ainda e a proxima", antes["proxima"]["date"])
    ok(depois["ultima"]["date"] == dia.isoformat(),
       "as 11:00 ja e a ultima", depois["ultima"]["date"])


def main(argv=None) -> int:
    argv = argv if argv is not None else sys.argv[1:]
    print("=" * 62)
    print("connectors/us_agenda.py + agenda do calendario")
    print("=" * 62)
    teste_offline()
    if "--offline" in argv:
        print("\n(testes ao vivo pulados: --offline)")
    else:
        from dotenv import load_dotenv

        load_dotenv()
        teste_vivo()

    print("\n" + "=" * 62)
    if falhas:
        print(f"{len(falhas)} FALHA(S): {falhas}")
        return 1
    print("todos os testes passaram")
    return 0


if __name__ == "__main__":
    sys.exit(main())
