"""
Atualiza o banco de dados macro_us (dados dos EUA).

Uso:
    uv run python jobs\\update_us.py             # janela de rotina (3 anos)
    uv run python jobs\\update_us.py --full      # carga fria / historico completo

Cada script e independente: se um falhar, os demais continuam.
Exit code 1 se houver qualquer falha.

--------------------------------------------------------------------------------
A ORDEM AQUI NAO E ARBITRARIA
--------------------------------------------------------------------------------
`inflc_cpi_dim` aparece DUAS vezes, no inicio e no fim, e as duas passadas fazem
coisas diferentes:

  1. dim (1a passada)  monta as duas arvores das fontes primarias (cu.item, a
                       planilha de relative importance, o HTML da Tabela 1 do
                       release). A lista de item_code que o passo seguinte busca sai
                       daqui.
  2. inflc_cpi         busca os niveis de indice na API, para os itens da dim.
  3. inflc_cpi_pesos   busca os pesos anuais (independente dos outros dois).
  4. dim (2a passada)  preenche sa_begin/nsa_begin/nsa_end, que sao MEDIDOS do que
                       esta em inflc_cpi -- e por isso so podem ser calculados
                       depois do passo 2.

Numa base ja carregada a 1a passada e redundante (a dim nao muda de mes para mes),
mas custa ~5s e e idempotente, entao roda sempre: e ela que detecta o BLS mudando a
indentacao publicada ou um rotulo da Tabela 1, levantando em vez de gravar uma
arvore silenciosamente errada.

**O PCE nao tem esse vai-e-volta**: a arvore e as series saem do MESMO arquivo do
BEA, entao `inflc_pce_dim` mede a cobertura direto da fonte e uma passada basta. Ela
vem antes de `inflc_pce` so porque e ela que valida a estrutura -- se o BEA mudar a
indentacao, o passo da arvore levanta antes de qualquer serie ser gravada.

--------------------------------------------------------------------------------
CUSTO
--------------------------------------------------------------------------------
Chave registrada do BLS = 50 series / 20 anos por requisicao, 500 requisicoes/dia.
O BEA nao precisa de chave e nao tem cota: e um xlsx de 12 MB, baixado uma vez e
reaproveitado no mesmo dia pelos dois passos de PCE.

  rotina (sem --full)     ~11 requisicoes BLS + 1 download BEA,  ~40s
  --full                  ~66 requisicoes BLS + 1 download BEA,  ~3min

Fontes:
  BLS — CPI-U: niveis por item (API v2), as duas arvores de itens
        (cu.item + Tabela 1 do news release) e a relative importance anual
  BEA — PCE: tabelas 2.4.4U (indice de preco) e 2.4.5U (despesa nominal) do
        arquivo de underlying detail da Secao 2, mensais, SA
"""

import argparse
import logging
import sys
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("update_us")

from domain.db.us.inflation import (
    inflc_cpi,
    inflc_cpi_dim,
    inflc_cpi_pesos,
    inflc_pce,
    inflc_pce_dim,
)


def _plano(full: bool):
    return [
        ("BLS · CPI dim (arvores)",        inflc_cpi_dim,   {}),
        ("BLS · CPI niveis",               inflc_cpi,       {"start_year": "all"} if full else {}),
        ("BLS · CPI pesos (rel. import.)", inflc_cpi_pesos, {}),
        ("BLS · CPI dim (cobertura)",      inflc_cpi_dim,   {}),
        ("BEA · PCE arvore (2.4.4U/2.4.5U)", inflc_pce_dim,  {}),
        ("BEA · PCE niveis + nominal",      inflc_pce,       {"start_year": "all"} if full else {}),
    ]


def main() -> None:
    ap = argparse.ArgumentParser(description="Atualiza macro_us")
    ap.add_argument("--full", action="store_true",
                    help="carga historica completa dos niveis (1913 em diante) em vez da janela de 3 anos")
    args = ap.parse_args()

    scripts = _plano(args.full)
    inicio = datetime.now()
    erros: list[tuple[str, str]] = []

    logger.info("Iniciando atualizacao macro_us — %d passos%s",
                len(scripts), " (--full)" if args.full else "")

    for label, mod, kwargs in scripts:
        try:
            logger.info("%-45s ...", label)
            mod.run(**kwargs)
            logger.info("%-45s OK", label)
        except Exception as exc:
            logger.error("%-45s FALHOU: %s", label, exc)
            erros.append((label, str(exc)))

    elapsed = (datetime.now() - inicio).seconds
    n_ok = len(scripts) - len(erros)
    logger.info("Concluido em %ds — %d/%d OK", elapsed, n_ok, len(scripts))

    if erros:
        logger.error("%d passo(s) falharam:", len(erros))
        for label, err in erros:
            logger.error("  - %s: %s", label, err)
        sys.exit(1)


if __name__ == "__main__":
    main()
