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

--------------------------------------------------------------------------------
CUSTO
--------------------------------------------------------------------------------
Chave registrada do BLS = 50 series / 20 anos por requisicao, 500 requisicoes/dia.

  rotina (--sem --full)   ~11 requisicoes,  ~20s   (2% da cota)
  --full                  ~66 requisicoes,  ~2min  (13% da cota)

Fontes:
  BLS — CPI-U: niveis por item (API v2), as duas arvores de itens
        (cu.item + Tabela 1 do news release) e a relative importance anual
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

from domain.db.us.inflation import inflc_cpi, inflc_cpi_dim, inflc_cpi_pesos


def _plano(full: bool):
    return [
        ("BLS · CPI dim (arvores)",        inflc_cpi_dim,   {}),
        ("BLS · CPI niveis",               inflc_cpi,       {"start_year": "all"} if full else {}),
        ("BLS · CPI pesos (rel. import.)", inflc_cpi_pesos, {}),
        ("BLS · CPI dim (cobertura)",      inflc_cpi_dim,   {}),
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
