"""
Parser do Questionario Pre-Copom (`domain/db/brasil/bcb/_qpc.py`) contra arquivos reais.

    uv run python tests/test_qpc_parse.py

Baixa 5 edicoes do BCB (~1,4 MB), sem banco. Cada edicao esta aqui por uma armadilha
que custou uma rodada na construcao (2026-09-29):

- 238a  formato de 2021: titulo da aba e o da questao-mae, subquestao na linha 2;
        questao 1 com contagem e % na mesma linha, sem rotulo de reuniao
- 240a  vies com duas linhas por ano (Copom 239 e Copom 240); % da questao 1 com base
        diferente da soma das contagens (a carga avisa, nao para)
- 246a  capa datada com a data da 247a -- o conserto e do ETL, aqui so se confirma o defeito
- 255a  rotulo de reuniao sem ano, "Copom 256 (Ago)"
- 281a  a aba Indice repete todos os titulos; "Media dos nucleos" e subtitulo e nao a
        estatistica "Media"; e os numeros conferidos contra os prints que o usuario mandou
"""

from __future__ import annotations

import datetime as dt
import logging

from connectors.bcb_copom import calendario_reunioes
from connectors.bcb_qpc import QPC
from domain.db.brasil.bcb import _qpc

logging.basicConfig(level=logging.WARNING, format="%(message)s")


def _v(rows, **k):
    achados = [r["valor"] for r in rows if all(r[c] == v for c, v in k.items())]
    assert len(achados) == 1, f"{k}: {len(achados)} linhas"
    return achados[0]


def main() -> None:
    datas = {n: dt.date.fromisoformat(d) for n, d in calendario_reunioes().items() if n >= 238}
    qpc = QPC()
    wb = {}
    for n in (238, 240, 246, 255, 279, 281):
        url = qpc.localizar(n, datas[n])
        assert url, f"edicao {n} nao localizada"
        wb[n] = qpc.abrir(url)
    rows = {n: _qpc.parse(w, n, datas[n]) for n, w in wb.items()}

    # 238a: formato antigo, uma reuniao-alvo, que e a propria edicao
    r = rows[238]
    alvos = {x["referencia"] for x in r if x["bloco"] == "copom_decisao"}
    assert alvos == {"R238"}, alvos
    assert _v(r, bloco="copom_decisao", variavel="fara", categoria="75") == 95
    assert _v(r, bloco="hiato", referencia="2021T1", estatistica="mediana") == -3.7
    assert _v(r, bloco="vies_ipca", referencia="2021", categoria="risco_de_alta") > 0.67
    assert not any(x["bloco"] == "ipca_curto_prazo" for x in r), "formato de medianas por componente deveria ficar fora"

    # 240a: so a linha da propria edicao no vies
    assert round(_v(rows[240], bloco="vies_ipca", referencia="2021", categoria="risco_de_alta"), 4) == 0.8812
    assert _v(rows[240], bloco="vies_ipca", referencia="2021", estatistica="n_respostas") == 101

    # 246a: o defeito da capa continua la (se sumir, o conserto do ETL vira inocuo)
    assert QPC.publicado_em(wb[246]) > datas[246] + dt.timedelta(days=30)

    # 255a: tres reunioes, ano inferido
    refs = sorted({(x["referencia"], x["ref_date"]) for x in rows[255] if x["bloco"] == "copom_decisao"})
    assert refs == [("R255", dt.date(2023, 6, 1)), ("R256", dt.date(2023, 8, 1)),
                    ("R257", dt.date(2023, 9, 1))], refs

    # 279a: a tabela de evolucao da mesma aba confirma a serie das 10 edicoes
    r = rows[279]
    assert [_v(r, bloco=b, referencia=h, estatistica="mediana") for b, h in
            (("juro_real_neutro", "curto_prazo"), ("juro_real_neutro", "5a"), ("nairu", "2a"))] == [6.4, 5.5, 7.4]

    # 281a: os prints
    r = rows[281]
    assert [_v(r, bloco="hiato", referencia=q, estatistica="mediana")
            for q in ("2026T2", "2026T4", "2027T4")] == [0.5, 0.2, -0.2]
    assert round(_v(r, bloco="vies_pib", referencia="2027", categoria="risco_de_baixa"), 2) == 0.73
    assert round(_v(r, bloco="ambiente_externo", categoria="menos_favoravel"), 2) == 0.67
    assert _v(r, bloco="situacao_fiscal", estatistica="n_respostas") == 106
    assert _v(r, bloco="ipca_horizonte_relevante", variavel="ipca_4t", estatistica="mediana") == 4.0
    assert round(_v(r, bloco="ipca_horizonte_relevante", variavel="prob_desvio",
                    categoria="entre_0_5pp", estatistica="media"), 2) == 0.55
    assert _v(r, bloco="copom_decisao", variavel="fara", referencia="R281", categoria="-25") == 111
    nucleos = [x for x in r if x["bloco"] == "ipca_curto_prazo" and x["variavel"] == "media_nucleos"]
    assert {x["estatistica"] for x in nucleos} == {"p25", "mediana", "p75", "n_respostas"}
    assert len({x["referencia"] for x in nucleos}) == 4

    # juro real neutro, PIB potencial e Nairu: tres blocos da mesma aba
    r = rows[240]
    assert _v(r, bloco="juro_real_neutro", referencia="curto_prazo", estatistica="mediana") == 3
    assert _v(r, bloco="pib_potencial", referencia="2a", estatistica="mediana") == 2
    assert not any(x["bloco"] == "nairu" for x in r), "Nairu so existe desde a 271a"
    assert not any(x["bloco"] in ("juro_real_neutro", "pib_potencial") for x in rows[238] + rows[281])
    assert all(x["variavel"] == x["bloco"] and x["ref_date"] is None
               for x in r if x["bloco"] in ("juro_real_neutro", "pib_potencial"))

    print("todos os asserts passaram")


if __name__ == "__main__":
    main()
