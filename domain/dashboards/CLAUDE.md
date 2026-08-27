# domain/dashboards/ — quem LÊ cada tabela

Config estática + resolvedor de estado, no mesmo formato de `domain/release_calendar/`.
Responde a pergunta que faltava no sistema: **este dashboard está olhando para dado velho?**

As três peças, e por que são separadas:

| | pergunta | onde |
|---|---|---|
| `domain/release_calendar/` | QUANDO cada dado sai | `calendar_2026.yaml` |
| `domain/db/registry.py` | QUEM ESCREVE cada tabela | derivado de `_TABLE` |
| **`domain/dashboards/`** | **QUEM LÊ cada tabela** | `manifest.yaml` |

Sem a terceira, apertar "Atualizar" no calendário deixava o banco em dia e todo HTML em
`reports/` parado — o ETL rodava e nada mais acontecia.

## Arquivos

- **`manifest.yaml`** — uma entrada por dashboard: saída, módulo com `run()`, comando, custo
  medido de geração, e a lista de dependências. Hoje 11 dashboards, 116 dependências.
- **`status.py`** — resolve o estado ao vivo de cada dependência e compara com o *stamp*.

## Por que declarado à mão

O registry deriva tabela→script porque todo ETL declara `_TABLE`. Do lado do consumo não há
convenção equivalente: cada `generate_report.py` lê de um jeito (`MySQLDataRequester` direto,
`_load_flat()`, `pd.read_sql` com JOIN, e um caso que lê tabela de outro projeto). Varrer isso
com regex daria falso negativo em silêncio — que é o erro que este arquivo existe para impedir.

`validar()` cobra o que dá para cobrar sem adivinhar: toda tabela declarada existe no banco,
todo arquivo declarado existe em disco, todo módulo importa. O inverso (tabela lida pelo código
e não declarada aqui) **não** é checável — ao adicionar uma leitura nova num relatório, declare
aqui também.

## Os 5 tipos de dependência

`mysql` · `csv` · `artifact` · `yaml` · `live`. O que separa os quatro últimos do primeiro é
prático: **nenhum botão de ETL os move**. `fora_do_mysql()` marca isso, e `base_mercado`
entra na marcação apesar de ser MySQL — quem escreve nela é o projeto CentralManagement.

## Stamp: por que o veredito precisa dele

O mtime do HTML diz *quando* foi gerado, não *o que tinha dentro*. `stamp()` grava, no momento
da geração, o último dado de cada dependência — aí a comparação vira exata: "o banco tem IPCA de
agosto, o relatório foi feito com até julho". Sem stamp o veredito é `sem stamp`, nunca um
`em dia` de mentira.

`gerar(key)` é o ponto de entrada único (roda `run()` + `stamp()`) e é o que o botão de regerar
chama, via `POST /api/gerar`. Gerar por fora continua funcionando e aparece como `sem stamp` — o campo
`output_mtime_ns` do stamp detecta o arquivo reescrito depois (nanossegundos, não segundos:
com resolução de segundo, regerar à mão no mesmo segundo do stamp passava por "em dia").

Dependência de arquivo tem um segundo sinal, `arquivo_mais_novo`, que **não** precisa de stamp:
um artefato reescrito depois do HTML não está dentro dele, ponto.

## Uso

```powershell
uv run python -m domain.dashboards.status                      # tabela de estado
uv run python -m domain.dashboards.status --detalhe brasil_credit
uv run python -m domain.dashboards.status --validar            # manifesto x banco x disco
uv run python -m domain.dashboards.status --live               # inclui FRED
uv run python -m domain.dashboards.status --gerar todos        # regera + stampa (~4 min)
```

Consumido por [`analytics/release_calendar/`](../../analytics/release_calendar/CLAUDE.md) — aba
"Status dashboard", e pelo endpoint `/api/dashboards` do `serve.py`.

Testes: [`tests/test_dashboard_status.py`](../../tests/test_dashboard_status.py) (lógica do
veredito sobre manifesto sintético + manifesto real contra banco e registry) e a seção
"STATUS DASHBOARD" de [`tests/test_release_calendar_js.js`](../../tests/test_release_calendar_js.js).

## Custo

`estado()` leva ~2s: um `UNION ALL` só resolve o `MAX(date)` das ~70 tabelas em 0,1s, e as
contagens de linha vêm aproximadas do `information_schema` de propósito — `COUNT(*)` exato no
mesmo conjunto custava 7,6s de varredura completa para preencher uma coluna informativa.
`--live` acrescenta uma chamada de rede por série externa.

## Um de cada vez, por decisão

**Não existe "regerar todos os atrasados"** — nem na aba, nem no endpoint, e isso é escolha do
usuário (2026-08-26), não uma etapa que faltou. Quem acabou de atualizar o IPCA escolhe qual dos
seis dashboards que o consomem interessa naquele momento; regerar os seis levaria 151s para
entregar cinco arquivos que ninguém ia abrir.

O `--gerar todos` do CLI continua existindo para o caso de carga inicial (é o que dá stamp a
todos de uma vez), mas a página nunca oferece lote. Há um teste que cobra isso — se alguém
reintroduzir um botão de lote na aba, a seção "STATUS DASHBOARD" do harness JS falha.

## Pending

- **`build_seconds` foi medido uma vez** (2026-08-26) e envelhece sozinho. `gerar()` já devolve
  o tempo real de cada execução; ninguém o grava de volta.
- **`POST /api/gerar` é síncrono**, igual ao `/api/run`: Expectations (53s) e FX (43s) deixam o
  botão em "regerando..." sem progresso. Fechar a aba não aborta. Se incomodar, a saída é job id
  + polling, não timeout — mesma pendência que o botão da outra aba já tinha.
- **O Oráculo não tem `module` com `run()`** (o entry point é o script solto
  `jobs/update_oraculo.py`, que escreve o CSV no nível do módulo). `gerar()` levanta nele de
  propósito, em vez de fingir sucesso. Fica manual até o job virar função.
