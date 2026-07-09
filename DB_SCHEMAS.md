# Organização dos Schemas MySQL

Servidor: 192.168.15.200 (rede local da empresa) · Credenciais: `.env`

## Regra de organização (2026-07, revisada)

**Schemas são por domínio/geografia, não por estágio de computação.** Cada schema
pode conter tabelas cruas, calculadas, ou uma mistura das duas — não existe uma
regra de "schema só para dado bruto" ou "schema só para dado calculado".

```
macro_brasil        — tudo que é especificamente do Brasil (BCB, IBGE), cru ou calculado
macro_international — tudo que precisa de dado de mais de um país para existir ou fazer sentido
macro_us             — futuro: dados dos EUA que não sejam só insumo de uma série internacional
```

**Critério de qual schema uma tabela nova vai:** só depende da geografia dos dados
que ela consome, nunca de "é bruto ou calculado". Se uma série usa só dado
brasileiro → `macro_brasil`, mesmo que seja calculada (ex.: `inflc_decomposicao.contribuicao`
= `var_mensal × pesos`, calculado no script). Se precisa de dado de 2+ países →
`macro_international`, mesmo que seja um dado "cru" de cada país individualmente
antes de combinar (ex.: `diferenciais_juros` guarda `selic` e `fed_funds` brutos
ao lado dos diferenciais calculados).

**Como sinalizar bruto vs. calculado, já que não é mais pelo schema:** no nível da
tabela/coluna, via `COMMENT` nativo do MySQL (ver `inflc_agregados` como exemplo —
`SHOW CREATE TABLE inflc_agregados`) e/ou docstring do script que a popula (seção
"Series brutas" / "Series derivadas", já usada em `diferenciais_juros.py` e
`inflc_decomposicao.py`).

## Convenção de nomes dentro de um schema (2026-07)

Tabelas são prefixadas por **tema macro**, não por schema/estágio — o prefixo
classifica o que o dado *é*, independente de quem consome ou onde ele mora.

Em `macro_brasil` (prefixos abreviados, segunda rodada de renomeação, por
instrução explícita do usuário):

```
atv_    — atividade real (PIB, produção industrial, varejo, serviços, IBC-Br)
mt_     — mercado de trabalho (PNAD, CAGED) — ficou de fora da 2ª rodada, mantém o prefixo por extenso
cred_   — crédito e condições financeiras das famílias/empresas
cmb_    — câmbio e seus determinantes (reservas, BOP, fluxo, termos de troca, cambio contratado)
inflc_  — IPCA/IPCA-15 (agregados, decomposição por subitem, dimensão)
expc_   — expectativas de mercado (Focus)
```

Em `macro_international` (unificado numa 3ª rodada, 2026-07-09, mesmo dia):

```
cmb_    — câmbio: cmb_reer, cmb_cot_fx
(sem prefixo) — diferenciais_juros: única tabela desse schema sem prefixo,
                por instrução explícita do usuário — não é "cmb_diferenciais_juros"
```

`diferenciais_juros` ficou deliberadamente sem prefixo mesmo sendo tematicamente
câmbio/juros — exceção explícita do usuário, não um esquecimento. Não adicionar
`cmb_` a essa tabela numa futura limpeza sem confirmar de novo.

Uma tabela só ganha prefixo se o tema ajuda a agrupá-la visualmente entre outras
do mesmo schema.

Renomeação executada em 2026-07 em três rodadas (mapeamento completo na tabela
"Tabelas por schema" abaixo) — nenhuma mudança de coluna/série em nenhuma das
três, só o nome da tabela e do script/arquivo que a popula (o nome do arquivo
sempre espelha o nome da tabela, exceto `diferenciais_juros` que nunca teve
prefixo no nome do arquivo mesmo quando a tabela teve).

## Histórico da decisão

**Junho 2026 — arquitetura original (3 schemas por estágio):** `macro_brasil` (raw
Brasil), `macro_international` (raw cross-country), `macro_analytics` (calculado).
Regra: "calculado vai para macro_analytics".

**Julho 2026 — revertida.** Motivo: `macro_analytics` nunca cresceu além de uma
única tabela (`diferenciais_juros`), e essa tabela já violava a própria regra de
origem — ela precisa de dado de Brasil **e** EUA para existir, o que a qualificava
para `macro_international` desde o início (regra: "se a série precisa de mais de um
país, vai para macro_international"). Ao mesmo tempo, `ipca_decomposicao` (criada em
`macro_brasil` na mesma época) já misturava bruto e calculado numa única tabela por
conveniência de query — a separação "só bruto" / "só calculado" já não estava sendo
seguida na prática antes mesmo de ser formalmente abandonada.

**Ação tomada:**
- `RENAME TABLE macro_analytics.diferenciais_juros TO macro_international.diferenciais_juros`
  (essa tabela foi renomeada de novo em jul/2026 para `cambio_diferenciais_juros` e depois
  de volta para `diferenciais_juros`, sem prefixo — ver rodadas abaixo)
- `DROP SCHEMA macro_analytics`
- Script movido: `domain/db/analytics/fred/diferenciais_juros.py` →
  `domain/db/international/fred/diferenciais_juros.py` (`_DATABASE = "macro_international"`)
- `jobs/update_analytics.py` removido; `diferenciais_juros` passou a rodar dentro de
  `jobs/update_international.py`
- `analytics/cambio/generate_report.py` atualizado para ler `diferenciais_juros` de
  `macro_international`

**Julho 2026 — prefixo de tema (1ª rodada).** Depois de decidir o schema por
domínio/geografia acima, faltava um critério para organizar as tabelas *dentro*
de cada schema. Adotado o prefixo por tema macro, por extenso (`atividade_`,
`mt_`, `credito_`, `cambio_`, `inflation_`, `expec_`). Todas as 20 tabelas de
`macro_brasil`/`macro_international` foram renomeadas de uma vez — `RENAME TABLE`
(sem impacto em dados/colunas), scripts/arquivos renomeados para espelhar (ex.:
`ibge/pnad.py` → `ibge/mt_pnad.py`), e todos os consumidores (`jobs/update_db.py`,
`jobs/update_international.py`, `analytics/oraculo/brasil/scores.py`,
`analytics/cambio/generate_report.py`, `analytics/inflation/generate_report.py`)
atualizados para os novos nomes.

**Julho 2026 — prefixo abreviado (2ª rodada, `macro_brasil` apenas).** O usuário
pediu nomes mais curtos para as 16 tabelas de `macro_brasil` (`atv_`, `cred_`,
`cmb_`, `inflc_`, `expc_` — ver mapeamento completo na tabela "Tabelas por
schema" abaixo). `mt_pnad`/`mt_caged` ficaram de fora da lista fornecida pelo
usuário e foram mantidos sem alteração (confirmado explicitamente antes de
executar). Mesma mecânica da 1ª rodada: `RENAME TABLE`, arquivos renomeados,
todos os consumidores atualizados. Resultado imediato: inconsistência entre
`cmb_` em `macro_brasil` e `cambio_` em `macro_international` — resolvida na
rodada seguinte, no mesmo dia.

**Julho 2026-07-09 — prefixo abreviado em `macro_international` (3ª rodada,
mesmo dia).** O usuário pediu para unificar: `cambio_reer`→`cmb_reer`,
`cambio_cot_fx`→`cmb_cot_fx`, e explicitamente `cambio_diferenciais_juros`→
`diferenciais_juros` (sem prefixo, não `cmb_diferenciais_juros`). Mesma
mecânica das rodadas anteriores. Schemas agora consistentes: tema câmbio é
`cmb_` nos dois schemas, com a única exceção documentada acima.

## Quando reconsiderar um schema por camada

Se no futuro surgir uma camada de analytics genuinamente cross-domain — por
exemplo, se os scores do `oraculo` (hoje CSV: `Brasil_base.csv`, `US_BASE.csv`,
`Central_base.csv`, misturando variáveis BR + US numa mesma nota) migrarem para
MySQL — **essa seria uma razão legítima** para um schema dedicado (`macro_oraculo`
ou similar), porque nesse caso a tabela não pertenceria a nenhum domínio
geográfico único. A distinção não é "é calculado?" mas "pertence genuinamente a
mais de um domínio, a ponto de não caber em nenhum schema de domínio existente?".
Não recriar `macro_analytics` preventivamente para uma tabela só — esperar o
padrão aparecer (2-3+ tabelas nessa situação) antes de criar o schema.

## Tabelas por schema (snapshot 2026-07-09, pós 3ª rodada)

| Schema | Tema | Tabelas (nome atual ← ← nome original) | Fonte |
|---|---|---|---|
| `macro_brasil` | `atv_` | `atv_pim` ← `atividade_pim` ← `pim`, `atv_pib` ← `atividade_gdp` ← `gdp`, `atv_pmc` ← `atividade_pmc` ← `pmc`, `atv_pms` ← `atividade_pms` ← `pms`, `atv_ibcbr` ← `atividade_ibc_br` ← `ibc_br` | IBGE, BCB |
| `macro_brasil` | `mt_` | `mt_pnad` ← `pnad` (inalterada na 2ª rodada), `mt_caged` ← `caged` (idem) | IBGE, BCB |
| `macro_brasil` | `cred_` | `cred_credito_amplo` ← `credito_amplo` ← `credito`, `cred_credito_familias` ← `credito_familias` ← `indicadores_familias` | BCB |
| `macro_brasil` | `inflc_` | `inflc_agregados` ← `inflation_agregados` ← `ipca_agregados` ← `inflacao`, `inflc_decomposicao` ← `inflation_decomposicao` ← `ipca_decomposicao`, `inflc_dim` ← `inflation_dimensao` ← `ipca_dimensao` | BCB, IBGE |
| `macro_brasil` | `expc_` | `expc_focus` ← `expec_focus` ← `expectativas` | BCB |
| `macro_brasil` | `cmb_` | `cmb_reservas_bc` ← `cambio_reservas` ← `reservas`, `cmb_balanco_pagmt` ← `cambio_balanco_pagamentos` ← `balanco_pagamentos`, `cmb_fluxo_cambial` ← `cambio_fluxo` ← `fluxo_cambial`, `cmb_termos_troca` ← `cambio_termos_troca` ← `termos_de_troca`, `cmb_cambio_contratado` ← `cambio_contratado` (sem mudança na 1ª rodada) | BCB |
| `macro_international` | `cmb_` | `cmb_reer` ← `cambio_reer` ← `reer`, `cmb_cot_fx` ← `cambio_cot_fx` ← `cot_fx` | BIS, CFTC |
| `macro_international` | (sem prefixo) | `diferenciais_juros` ← `cambio_diferenciais_juros` ← `diferenciais_juros` (voltou ao nome original, sem prefixo — exceção explícita do usuário) | FRED+BCB |

Ver `CLAUDE.md` para descrição de cada tabela individualmente.
