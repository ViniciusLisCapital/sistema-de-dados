# Mercado de trabalho — mapeamento de fontes (IBGE / CAGED / BCB / IPEA)

Levantamento feito em 2026-08-11, ao vivo contra as APIs de cada fonte (não apenas
documentação). Objetivo: deixar claro, por dado, quem é a fonte primária e quais
distribuidores (BCB, IPEA) republicam qual fatia — ver
[`domain/db/CLAUDE.md`](../../domain/db/CLAUDE.md) para as tabelas que já temos no
banco (`mt_pnad`, `mt_caged`).

## Tabela de cobertura

Atualizado em 2026-08-11 (segunda passada) — coluna "Na base/ETL" reflete o estado
real do banco depois de fechar `mt_pnad`/`mt_pnad_trimestral`, não mais o estado do
levantamento original.

| Dado | IPEA | CAGED (fonte primária/MTE-PDET) | BCB | IBGE | Fonte primária | Na base/ETL | Comentário |
|---|---|---|---|---|---|---|---|
| Estoque de empregos formais (nível) | ❌ | ✅ | ✅ (SGS 28763-28776) | ❌ | **CAGED/MTE** | ✅ (mal rotulado) | `mt_caged.py` coleta isso hoje via BCB — mas o script rotula errado como "saldo". Ainda não corrigido. |
| Saldo nacional (admissões − desligamentos) | ✅ (`CAGED12_SALDON12`, bruto + dessaz.) | ✅ | ❌ | ❌ | **CAGED/MTE** | ❌ | É o número que todo mundo cita ("X mil empregos criados"). IPEA é o único distribuidor limpo disso — ainda não implementado. |
| Admissões nacional | ✅ (`CAGED12_ADMISN12`) | ✅ | ❌ | ❌ | **CAGED/MTE** | ❌ | Ainda não implementado. |
| Desligamentos nacional | ✅ (`CAGED12_DESLIGN12`) | ✅ | ❌ | ❌ | **CAGED/MTE** | ❌ | Ainda não implementado. |
| Saldo/admissões/desligamentos por setor (CNAE) | ❌ | ✅ (microdados/tabelas oficiais) | ❌ | ❌ | **CAGED/MTE** | ❌ | Nenhum distribuidor via API tem isso — só nos microdados brutos do FTP. |
| Saldo por UF/município | ❌ | ✅ (microdados/tabelas oficiais) | ❌ | ❌ | **CAGED/MTE** | ❌ | Só microdados. |
| Salário de admissão/desligamento | ❌ | ✅ (campo nos microdados) | ❌ | ❌ | **CAGED/MTE** | ❌ | Não existe em nenhum agregado publicado — só no registro individual do microdado. |
| Taxa de desocupação | ❌ | ❌ | ❌ | ✅ (agregado 6381) | **IBGE** | ✅ | `mt_pnad`, série `taxa_desocupacao` — nacional. Por sexo/idade/instrução/raça em `mt_pnad_trimestral`. |
| Taxa de informalidade | ❌ | ❌ | ❌ | ✅ (agregados 8501/8513) | **IBGE** | ✅ | `mt_pnad`, séries `ocup_informal`/`taxa_informalidade` — nacional. Por dimensão em `mt_pnad_trimestral`. |
| Subutilização da força de trabalho | ❌ | ❌ | ❌ | ✅ (agregados 6438-6441, 6785, 6807) | **IBGE** | ✅ | `mt_pnad`, séries `subutil_*`/`taxa_subutil_*` — nacional. Combinada/composta por sexo/idade também em `mt_pnad_trimestral`. |
| Taxa de participação na força de trabalho | ❌ | ❌ | ❌ | ✅ (agregado 5944) | **IBGE** | ✅ | `mt_pnad`, série `taxa_participacao` — nacional. Por dimensão em `mt_pnad_trimestral`. |
| Pessoas ocupadas/desocupadas (níveis, condição) | ❌ | ❌ | ❌ | ✅ (agregados 6318/6379/6380) | **IBGE** | ✅ | `mt_pnad`, séries `forca_*`/`nivel_ocupacao`/`nivel_desocupacao` — completo. |
| Rendimento habitual/efetivo (posição/atividade) | ❌ | ❌ | ❌ | ✅ (agregados 6387-6391) | **IBGE** | ✅ | `mt_pnad`, séries `rend_*`/`rend_efetivo_*`/`rend_habitual_*_todos_trabalhos` — completo. Por sexo/idade/instrução/raça/ocupação em `mt_pnad_trimestral`. |
| Massa de rendimento | ❌ | ❌ | ❌ | ✅ (agregado 6392/6393) | **IBGE** | ✅ | `mt_pnad`, séries `massa_*`/`massa_efetiva_*` — completo (habitual + efetivamente recebido). |
| Rendimento/massa/horas por sexo, idade, instrução, cor/raça | ❌ | ❌ | ❌ | ✅ (PNAD Contínua trimestral, pesquisa DD) | **IBGE** | ✅ | `mt_pnad_trimestral` — nível Brasil apenas; nível UF (N3) ainda fora de escopo. Dimensão nova, não fazia parte do levantamento original desta tabela. |

## Leitura geral

- **IBGE** é fonte primária de tudo que é PNAD (desemprego, informalidade,
  rendimento) — hoje coletamos praticamente tudo que a mensal (`mt_pnad`) e a
  trimestral (`mt_pnad_trimestral`, cortes demográficos/ocupacionais em nível
  Brasil) oferecem. Falta só o nível UF (N3) da trimestral, deixado de fora
  deliberadamente na primeira rodada.
- **CAGED/MTE** é fonte primária de tudo que é emprego formal (estoque, saldo,
  admissões, desligamentos, por setor/UF/salário) — hoje só coletamos a fatia de
  **estoque**, e coletamos ela rotulada errado como saldo (ver
  `domain/db/brasil/bcb/mt_caged.py`). Esse é o item pendente principal.
- **BCB** e **IPEA** nunca são fonte primária de nada aqui — são distribuidores,
  cada um carregando uma fatia diferente do que o CAGED/MTE produz (BCB: estoque
  nacional+setor; IPEA: saldo/admissões/desligamentos só nacional).
