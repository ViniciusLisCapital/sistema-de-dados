# jobs/ — entry points e a rotina diária

Cinco entry points, todos com `main()` e todos chamáveis por `uv run python jobs/<arquivo>.py`.
A lista de tabelas nunca mora aqui: vem de `domain/db/registry.py` (quem escreve o quê) e de
`domain/release_calendar/calendar_2026.yaml` (o que é grupo de divulgação e o que é série
contínua).

| arquivo | o que roda |
|---|---|
| `update_db.py` | `macro_brasil`. Passe completo (54 scripts) ou recorte: `--continuous` (as 11 séries diárias, ~45s), `--group <slug>` (o que o botão do calendário chama), `--tables a,b`, `--list` |
| `update_us.py` | `macro_us`, 10 passos, **e a ORDEM importa** — ver a docstring do arquivo. O 7º (JOLTS), o 8º (CES), o 9º (CPS) e o 10º (produtividade) ignoram `--full` de propósito |
| `update_international.py` | `macro_international`, 3 scripts (REER do BIS, COT da CFTC, diferenciais de juros do FRED) |
| `update_oraculo.py` | recalcula as notas 1–10 do termômetro macro |
| `atualizar_diario.py` | envelope fino em volta de `update_db.main(["--continuous"])`, só para a tarefa agendada — ver abaixo |

## Terminado o ETL, o CLI regera os dashboards afetados

O calendário servido **não** encadeia atualizar dado e reconstruir relatório — são dois botões.
Na linha de comando, encadeia, **desde 2026-08-28 e a pedido do usuário** ("quando atualizar os
dados, as métricas também devem ser atualizadas"). Terminado o ETL, `update_db.py` regera os
dashboards que **leem** as tabelas que acabou de escrever, e só os que ficaram para trás:
`status.afetados()` responde quem lê (a contrapartida do `registry`, que responde quem escreve)
e o veredito de `status.estado()` decide se é preciso — um passe que não trouxe linha nova
deixa todo mundo "em dia" e não regera nada. `--sem-gerar` desliga. A página continua como
estava: ela chama `executar_grupo()` direto, que não passa por esse caminho, então a escolha
um-a-um da aba "Status dashboard" segue intacta.

**O que motivou** (2026-08-28): o usuário atualizou o RTN e esperou as medidas de impulso
fiscal se moverem. Elas não leem `fisc_rtn` — leem `fisc_efgg` (trimestral, IEG), `fisc_nfsp`
e `fisc_dlsp_fatores`, cada uma no seu próprio calendário. Nada no sistema dizia isso nem
regerava o que de fato lê. As duas metades da resposta são um mapa "quem lê esta tabela" e um
gatilho que só dispara para quem ficou atrás; o caso concreto está em
[`analytics/brasil/fiscal_policy/CLAUDE.md`](../analytics/brasil/fiscal_policy/CLAUDE.md).
↳ o mecanismo (`afetados()`, `regerar_afetados()`, o veredito de `estado()`, e por que a
página **não** passa por este caminho) está em
[`domain/dashboards/CLAUDE.md`](../domain/dashboards/CLAUDE.md).

## A tarefa agendada

**Há uma tarefa agendada deste projeto desde 2026-09-03**: `Macro - series diarias`, no Agendador
do Windows, rodando **de 30 em 30 minutos das 09:30 às 12:00** (seis disparos: 09:30, 10:00, 10:30,
11:00, 11:30, 12:00), todos os dias. Não confundir com a "Atualizacao da base de dados" das 09:30,
que é do CentralManagement.

O que ela chama é **`.venv\Scripts\pythonw.exe jobs/atualizar_diario.py`**, um envelope fino em
volta de `update_db.main(["--continuous"])` que só acrescenta log em arquivo, poda e código de saída
— a lista de tabelas continua vindo de `no_release.continuous` no `calendar_2026.yaml`, e a
regeração dos dashboards continua sendo a do próprio `update_db`. O `atualizar_diario.bat` ficou
como atalho de dois cliques (mesma lógica, com `python` em vez de `pythonw` para dar saída na tela);
a tarefa **não** passa por ele.

**`pythonw` é o pedido do usuário — "para não criar a janela interativa" — e o motivo é que a janela
vinha do `.bat`**: arquivo de lote é executado pelo cmd.exe, que é binário de console, então cada um
dos seis disparos pipocaria um prompt preto na frente de quem estivesse usando a máquina.
`pythonw.exe` é a variante compilada para o subsistema GUI e não aloca console. **E é aí que está a
armadilha, medida em 2026-09-03**: sem console não há stdout, e sob `pythonw` `sys.stdout` e
`sys.stderr` são literalmente `None`. O que isso produz **não é exceção, é silêncio** — `print()` com
arquivo None sai cedo no CPython e não faz nada, e um `logging.basicConfig()` sem `stream=` fixa o
`sys.stderr` **na hora da chamada** (o `update_db` chama isso no topo do módulo, ou seja, no
`import`), nascendo com `stream=None` e engolindo o próprio erro de handler. Sem o setup do
`atualizar_diario.py` a tarefa **funcionaria** — gravaria no banco, regeraria os dashboards — e não
deixaria uma linha de log; no dia em que falhasse não haveria nada para ler. Daí a ordem daquele
arquivo ser load-bearing: abrir o log, apontar `sys.stdout`/`sys.stderr` para ele, chamar o
`basicConfig` com `stream=` (o do `update_db` vira no-op, porque o root logger já tem handler) e só
então importar o `update_db`.

**Nenhuma janela retroativa é configurada na tarefa, e é por isso que seis disparos não são
desperdício nem risco**: cada script tem a sua no default do próprio `run()`, e toda inserção é
upsert (`ON DUPLICATE KEY UPDATE`), então reescrever um dia que não mudou não produz linha nova. As
janelas, auditadas por introspecção das assinaturas em 2026-09-03: **`cmb_dollar_index` (1971),
`comm_brent` e `cmb_equity_us` (1990), `cmb_fx_latam` (2000) e `cmb_dollar_index_em` (2006) rebuscam
a série INTEIRA** a cada passe — `start` é literal no `run()`, não uma janela —, o que é por que elas
se curam de qualquer buraco histórico sozinhas; `cmb_ptax` 90 dias corridos; `br_interest_rate` 10
dias **úteis** nas curvas da B3 e 60 corridos na POLICY; `inter_interest_rate` e `us_interest_rate`
30 dias corridos; `cmb_cambio_contratado` e `cmb_reservas_bc` 3 meses.

Custo medido: **~45s a ~100s** quando nada mudou e **~280s** quando há dado novo o suficiente para
regerar — a regeração é gatilhada por `status.estado()`, então um passe que não trouxe linha nova
não regera nada (o log diz *"Dashboards que leem estas tabelas: 2, nenhum desatualizado"*). O
`ExecutionTimeLimit` é de 25 min, deliberadamente **menor que o intervalo de 30**, e
`MultipleInstances` é `IgnoreNew`: um passe travado é morto antes do próximo disparar, e dois nunca
se sobrepõem.

O que motivou não foi teoria: no dia em que a tarefa foi criada, **8 das 11 tabelas contínuas estavam
7 a 16 dias atrás** (`comm_brent` 16, `cmb_dollar_index_em` 13, `cmb_cambio_contratado` 13,
`cmb_ptax` 10), e um único passe pôs todas em dia. **Duas armadilhas do agendamento além da do
`pythonw`**, ambas do tipo que só aparece quando a tarefa roda pelo Agendador e não no teste manual:
uma tarefa agendada **não herda o PATH da sessão interativa**, então `uv` puro falha com "não
reconhecido" (daí a tarefa e o `.bat` usarem caminhos absolutos dentro do `.venv`); e `%DATE%` muda
com a configuração regional da máquina, o que quebraria o nome do arquivo de log (agora a data vem do
Python). A tarefa foi verificada **por disparo real pelo Agendador**, não só rodando o script:
`LastTaskResult 0`, 11/11 OK em 99s, mais uma execução completa sob `pythonw` com regeração de
verdade (FX Report, 66s) cujos prints e acentos chegaram corretos ao log. Log em
`logs/continuous_AAAA-MM-DD.log` (gitignored, poda em 30 dias).
