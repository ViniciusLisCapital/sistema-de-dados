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
| Estoque de empregos formais (nível) | ❌ | ✅ | ✅ (SGS 28763-28776) | ❌ | **CAGED/MTE** | ✅ | `mt_caged.py` coleta via BCB. A rotulagem errada ("saldo") foi corrigida em 2026-08 — docstring do script + `COMMENT` nativo da tabela. Confirmado ao vivo que é estoque: 48.032.308 em 2026-06, e a diferença mensal bate exatamente com o saldo do microdado (145.161). |
| Saldo nacional (admissões − desligamentos) | ✅ (`CAGED12_SALDON12`, bruto + dessaz.) | ✅ | ❌ | ❌ | **CAGED/MTE** | ✅ | Direto da fonte primária desde 2026-08: soma de qualquer uma das 3 tabelas `mt_caged_setor`/`_uf`/`_salario` (as três fecham no mesmo total nacional por construção). |
| Admissões nacional | ✅ (`CAGED12_ADMISN12`) | ✅ | ❌ | ❌ | **CAGED/MTE** | ✅ | Idem — métrica `admissoes` nas 3 tabelas. |
| Desligamentos nacional | ✅ (`CAGED12_DESLIGN12`) | ✅ | ❌ | ❌ | **CAGED/MTE** | ✅ | Idem — métrica `desligamentos` nas 3 tabelas. |
| Saldo/admissões/desligamentos por setor (CNAE) | ❌ | ✅ (microdados/tabelas oficiais) | ❌ | ❌ | **CAGED/MTE** | ✅ | `mt_caged_setor` — 22 seções CNAE 2.0, do microdado do FTP. Nenhum distribuidor via API tem isso. |
| Saldo por UF | ❌ | ✅ (microdados/tabelas oficiais) | ❌ | ❌ | **CAGED/MTE** | ✅ | `mt_caged_uf` — 27 UFs. Nível município fica fora de escopo (o microdado tem, mas não foi modelado). |
| Salário de admissão/desligamento | ❌ | ✅ (campo nos microdados) | ❌ | ❌ | **CAGED/MTE** | ✅ (por faixa) | `mt_caged_salario` — 10 faixas em múltiplos do salário mínimo vigente. O valor individual do salário existe no microdado mas não é persistido (arquitetura agregar-e-descartar). |
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
  admissões, desligamentos, por setor/UF/salário). Desde 2026-08 coletamos
  saldo/admissões/desligamentos **direto do microdado do FTP do PDET** em 3
  cortes independentes (`mt_caged_setor`/`mt_caged_uf`/`mt_caged_salario`, ver
  `domain/db/brasil/mte/`) — dispensa o IPEA como distribuidor e vai além do que
  ele publica (que era só o total nacional). O **estoque** continua vindo do BCB
  (`mt_caged`), agora corretamente rotulado, e é a única série longa do tema
  (1992→hoje, contra 2020-01→hoje do microdado). As quatro tabelas alimentam a
  aba "Emprego Formal" de `analytics/labor_market/` desde 2026-08.
- **BCB** e **IPEA** nunca são fonte primária de nada aqui — são distribuidores,
  cada um carregando uma fatia diferente do que o CAGED/MTE produz (BCB: estoque
  nacional+setor; IPEA: saldo/admissões/desligamentos só nacional).

## Novo CAGED (microdado do FTP) — o que é preciso saber

- **Cobertura começa em 2020-01**, quando o Novo CAGED substituiu o CAGED antigo
  (que ia até 2019 num layout diferente, deliberadamente fora de escopo). Para
  série longa pré-2020, o BCB/IPEA continuam sendo o caminho.
- **`date` é a competência de MOVIMENTAÇÃO**, não a de declaração — é o mês em
  que a admissão/desligamento aconteceu de fato.
- **Os números de meses recentes são revisados para cima/baixo por até ~1 ano**,
  porque declarações fora do prazo (`CAGEDFOR`) e exclusões (`CAGEDEXC`) chegam
  em releases posteriores e se aplicam retroativamente à competência original.
  A atualização de rotina reprocessa os últimos 6 releases; uma competência só
  estabiliza de vez ~12 meses depois. Para refazer o histórico inteiro
  incorporando todas as correções já publicadas:
  `mt_caged_novo.run(start="all")` (~4GB de download, job longo).
- As 3 tabelas somam ao **mesmo total nacional** por construção (são cortes do
  mesmo universo de movimentações) — bom cross-check depois de qualquer carga.
