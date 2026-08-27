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

**O PCE nao tem esse vai-e-volta**, e desde 2026-08-26 o passe de rotina dele nao
baixa arquivo nenhum: os dois passos vao pela API.

A arvore do PCE so pode ser montada do xlsx -- a API nao publica hierarquia (checado
em todos os datasets do servico). Mas ela nao precisa ser RECONSTRUIDA todo mes: e
gravada em `inflc_pce_dim` e, nas rodadas seguintes, `run(fonte="auto")` a RELE do
MySQL e usa a API para provar que continua valida:

  - o conjunto de linhas (numero, rotulo, e codigo na tabela de indice) bate com o
    gravado -> nenhuma linha foi inserida, removida, renomeada ou recodificada;
  - a aditividade em nominal fecha contra os valores da API, sobre a arvore GRAVADA
    -> nenhuma linha trocou de pai (re-indentacao sem renomeacao, que a comparacao
    de conjunto nao veria, move bilhoes e nao fecha);
  - a particao dos niveis 1-4 da 100%.

Passando as tres, so a COBERTURA e reescrita (`idx_end`/`nom_end` andam todo mes; o
comeco de uma serie nao anda). Falhando qualquer uma, o xlsx e baixado e a arvore
reconstruida do zero -- o arquivo virou caminho de REPARO, nao dependencia mensal.
Conferido: a tabela que o caminho auto grava e identica em todas as 18 colunas a que
a reconstrucao completa grava.

A ordem ainda importa -- a arvore antes das series --, porque e ela que valida a
estrutura: se o BEA reorganizou a tabela, o passo da arvore levanta antes de qualquer
serie ser gravada.

**O que se perde:** a conferencia valor-a-valor de `inflc_pce.run(conferir=True)`
contra o xlsx era gratuita porque o arquivo estava em cache, e agora ele nao e mais
baixado -- entao ela e PULADA no passe de rotina, e o log diz isso. Ela nao
desapareceu: roda em `tests/test_bea_api.py` (as duas portas, historia inteira) e em
qualquer execucao com `fonte="xlsx"`. O guarda de rotina passou a ser o estrutural
acima.

--------------------------------------------------------------------------------
CUSTO
--------------------------------------------------------------------------------
Chave registrada do BLS = 50 series / 20 anos por requisicao, 500 requisicoes/dia.
O BEA precisa da `BEA_API_KEY` no `.env` (100 req/min, 100 MB/min, 30 erros/min). O
xlsx de 12 MB nao entra no passe de rotina -- so quando a estrutura muda, ou com
`fonte="xlsx"` explicito.

  rotina (sem --full)     ~11 req BLS + 4 req API (~9 MB),   ~45s   sem xlsx
  --full                  ~66 req BLS + 4 req API (~153 MB), ~4min  sem xlsx
  reparo de estrutura     + 1 download de 12 MB, so quando a checagem acusa

As 4 requisicoes de BEA sao 2 da arvore (janela de 2 anos, so para conferir conjunto
e aditividade) e 2 das series. O `--full` pela API e mais pesado do que era pelo xlsx
-- 150 MB de JSON contra 12 MB de planilha comprimida -- e passa perto do limite de
100 MB/min, medido em 2026-08-26 sem estrangulamento, mas sem margem para rodar duas
vezes no mesmo minuto. A rotina ficou mais leve nas duas pontas: a API entrega
exatamente a janela pedida, e a arvore deixou de exigir o arquivo inteiro.

Fontes:
  BLS — CPI-U: niveis por item (API v2), as duas arvores de itens
        (cu.item + Tabela 1 do news release) e a relative importance anual
  BEA — PCE: tabelas 2.4.4U (indice de preco) e 2.4.5U (despesa nominal), mensais,
        SA. Tudo pela API (dataset NIUnderlyingDetail) no passe de rotina; a arvore
        vem do xlsx de underlying detail da Secao 2 -- unico lugar onde a hierarquia
        existe -- mas so na carga inicial e quando a estrutura muda
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
        ("BEA · PCE arvore (2.4.4U/2.4.5U)", inflc_pce_dim,
         {"fonte": "xlsx"} if full else {}),
        ("BEA · PCE niveis + nominal (API)",       inflc_pce,
         {"start_year": "all"} if full else {}),
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
