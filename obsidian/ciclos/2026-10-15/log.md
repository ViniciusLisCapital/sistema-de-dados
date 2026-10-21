# Log — ciclo 2026-10-15

Escrito pela sessão que conduz o ciclo. Este ciclo não é um ciclo completo: guarda dois testes solo da rodada 1, rodados em 2026-10-21 sobre os dados de 15/10 (o ciclo de 21/10 não foi montado porque o FRED estava em manutenção). Os dois agentes leram só a camada 1, pelo retrato do conhecimento (`conhecimento/<agente>/`).

- **Câmbio, re-teste só com a camada 1** (`PLANO_AGENTES.md`, Fase 4): `cambio_r1.md`. Tratado como primeiro ciclo; não leu o teste anterior do mesmo dia (`cambio_r1_projecao.md`, que lia o vault inteiro).
- **Política monetária, primeiro teste solo** (Fase 6): `politica_monetaria_r1.md`.

## Informação nova desde o ciclo anterior

Testes solo, sem ciclo anterior aprovado. O fato que domina os dois reports: a reprecificação do pregão de 05/10, depois do 1º turno (PTAX −4,55%, DI de 5 anos −135 p.b., CDS −22 p.b. entre 02/10 e 06/10).

## Rodadas

### Rodada 1 · câmbio (re-teste, camada 1)

- **Leu:** `F_cambio.md` (inteiro); mapa conceitual, Partes 1–4 (e a Parte 5 até #exchange_rate_determination); `_modelo_report.md`; manual do escrivão §6–9. Nenhum report de outro agente nem P.
- **Conhecimento aberto:** 11 arquivos (tabela abaixo); nenhum `clean_md`.
- **Faltou:** 7 temas de conhecimento e 6 de dados (tabela abaixo).
- **Escreveu:** report 1 (`cambio_r1.md`).

### Rodada 1 · política monetária (primeiro teste solo)

- **Leu:** `F_politica_monetaria.md` (inteiro); mapa conceitual, Partes 1–4 (e a Parte 5 na passada); comunicado e ata da 281ª e RPM de set/26 (24/09), este inteiro menos o boxe do El Niño (só o resumo); comunicado da 280ª, para comparar o texto; manual do escrivão §6–9; `_modelo_report.md`. Nenhum report de outro agente nem P.
- **Conhecimento aberto:** 13 arquivos (tabela abaixo); nenhum de outro dono.
- **Faltou:** 6 temas (tabela abaixo).
- **Escreveu:** report 1 (`politica_monetaria_r1.md`).

## Conhecimento

| Agente · rodada | Arquivo (caminho no retrato) | Tipo | Dono | Outro dono |
|---|---|---|---|---|
| câmbio · r1 | `INDICE.md` | índice | — | |
| câmbio · r1 | `exchange_rate/exchange_rate_conceptual_map.md` | mapa | câmbio | |
| câmbio · r1 | `exchange_rate/mental_models/verde_fx_mental_models.md` (§1.1, §1.9–2.4, §3.1–3.4, §4.6–4.8, §5.1–8.5, §10, Connections) | modelo mental | câmbio | |
| câmbio · r1 | `concepts/risk_premium.md` | conceito | — | |
| câmbio · r1 | `concepts/carry_trade.md` | conceito | — | |
| câmbio · r1 | `concepts/fx_intervention.md` | conceito | — | |
| câmbio · r1 | `concepts/bank_fx_position.md` | conceito | — | |
| câmbio · r1 | `concepts/global_financial_cycle.md` | conceito | — | |
| câmbio · r1 | `concepts/fiscal_dominance.md` | conceito | — | |
| câmbio · r1 | `monetary_policy/synthesis/monetary_policy_exchange_rates (BIS, 2026).md` | síntese | câmbio | |
| câmbio · r1 | `exchange_rate/synthesis/padrao_transmissao_cambial (Cortapasso, 2023).md` | síntese | inflação | sim |
| PM · r1 | `INDICE.md` | índice | — | |
| PM · r1 | `monetary_policy/monetary_policy_conceptual_map.md` | mapa | PM | |
| PM · r1 | `monetary_policy/clean_md/central_bank/comunicados/copom_281_comunicado_2026-09-16.md` | Copom | PM | |
| PM · r1 | `monetary_policy/clean_md/central_bank/atas/copom_281_ata_2026-09-16.md` | Copom | PM | |
| PM · r1 | `monetary_policy/clean_md/central_bank/rpm/rpm_202609_2026-09-24.md` | Copom | PM | |
| PM · r1 | `monetary_policy/clean_md/central_bank/comunicados/copom_280_comunicado_2026-08-05.md` | Copom | PM | |
| PM · r1 | `monetary_policy/clean_md/central_bank/comunicados/copom_277_comunicado_2026-03-18.md` (só a orientação, por grep) | Copom | PM | |
| PM · r1 | `monetary_policy/mental_models/verde_mp_mental_models.md` (§1 e §2) | modelo mental | PM | |
| PM · r1 | `concepts/natural_rate_of_interest.md` | conceito | — | |
| PM · r1 | `concepts/interest_rate_smoothing.md` | conceito | — | |
| PM · r1 | `concepts/inflation_forecast_targeting.md` | conceito | — | |
| PM · r1 | `concepts/forward_guidance.md` | conceito | — | |
| PM · r1 | `monetary_policy/synthesis/neutral_rate_time_varying_brazil (Perrelli & Roache, 2014).md` | síntese | PM | |

O câmbio citou Chamon & Garcia 2016 só pelo que diz `concepts/fx_intervention.md`. A PM citou Svensson 1997, Minella 2002, Bernanke & Gertler 1995 e Blanchard 2004 pelas páginas de conceito e pela Parte 2 do mapa, sem abrir as sínteses.

## Faltou

| Agente · rodada | Tema | Por que fez falta | O que resolveria (se o agente souber) |
|---|---|---|---|
| câmbio · r1 | Modelos mentais Kapitalo (§1.5), Kinea e GS | O mapa os indica para Q3 (global × idiossincrático), 2.1–2.3 e 2.8; Q3 e a valuation ficaram com uma gestora | Trazer as três para a camada 1. **Promovida a Kapitalo** (decisão do usuário, 2026-10-21) |
| câmbio · r1 | Repasse cambial com coeficientes | E3 saiu só dos pesos do modelo; a síntese de Cortapasso dizia que a extração terminava antes dos resultados do VAR | Completar Cortapasso e trazer Goldfajn/Belaisch. O `clean_md` já está inteiro: **a síntese foi removida para ser refeita** pelo `/vault` |
| câmbio · r1 | Por que o CDS em dólar subestima o prêmio fiscal/político local | Justificativa do tempero (i) × 1,5, argumentada só com os preços do episódio | Texto sobre prêmio de prazo da curva brasileira e eleições |
| câmbio · r1 | Estudo de evento de eleições e câmbio (2002, 2014, 2018, 2022) | Decide E1 e a probabilidade da cauda worst; só a Verde §6.2, por anedotas | — |
| câmbio · r1 | Desmonte de posição comprada em moeda EM de alto carry | O BIS 2026 trata de moedas de funding; aplicado ao real por analogia | — |
| câmbio · r1 | GSDEER/BEER para o real | A valuation ficou só no REER do BIS | Camada 2 (GS primer, 2º da fila) |
| câmbio · r1 | Dados: vol. implícita, cupom cambial (E7), posição à vista dos bancos de setembro, condicionante de câmbio do Copom (E4), pesquisas eleitorais, IC-Br de outubro | Para o F, não para o conhecimento | Cupom: API da Bloomberg (01/11). Condicionante do Copom: vem pela S3 (o agente agora declara a lacuna em vez de escrever de memória) |
| PM · r1 | Prêmio a termo (`term_premium`) | Separar caminho esperado de prêmio na curva DI (Q4) e na inflação implícita | **Promovido Adrian, Crump & Moench 2013** |
| PM · r1 | Crédito direcionado | Neutro mais alto e transmissão mais fraca (Q2/Q3) ficaram só no que diz a ata | **Promovido Segura-Ubiergo 2012** |
| PM · r1 | Repasse do petróleo aos monitorados e política de preços da Petrobras | O tempero (ii) do petróleo ficou sem medida | Agente de inflação (não existe) |
| PM · r1 | Dado eleitoral | A reprecificação de 05/10 é a premissa mais pesada do base e do worst | Fora enquanto o sistema está em teste (decidido 2026-10-15) |
| PM · r1 | Calendário do Copom de 2028 | O oficial termina em 08/12/27; supôs duas reuniões no 1T28 | — |
| PM · r1 | Expectativas Firmus e FGV; datas de divulgação do IPCA | Citadas pelo texto do RPM | — |

## Funções G

| Agente · rodada | Arquivo | O que calcula | Resultado usado | Destino |
|---|---|---|---|---|
| câmbio · r1 | `r1b_cambio_modelo_listar.py` | exógenas, padrões e coeficientes do simulador | chaves e intervalos de 90% (b_fiscal 25,111 [19,481; 30,608], ia3, ii4) | registro |
| câmbio · r1 | `r1b_cambio_modelo_padrao.py` | simulador no padrão | PTAX 4T26 5,210 | registro |
| câmbio · r1 | `r1b_cambio_unidades.py` | confere que as exógenas são nível no fim do trimestre | CDS 3T26 = 131,21 em 30/09 | registro (a convenção vai para o `listar`) |
| câmbio · r1 | `r1b_cambio_trajetoria.py` | PTAX, CDS, DXY, dólar EM, pares, Brent, DI 1a/5a desde ago | PTAX −2,64%, CDS −19 p.b., DI 5a −142 p.b. desde 30/09 | registro |
| câmbio · r1 | `r1b_cambio_mercado.py` | intervenções, fluxo diário, COT, diferencial | vendas do BC e linhas de set; fluxo financeiro +4,13 bi em 05–09/10 | registro |
| câmbio · r1 | `r1b_cambio_diferencas.py` | COT na semana da eleição; PTAX e DI em 02→05/10; pares | fundos alavancados +17.843; PTAX −4,55% | registro |
| câmbio · r1 | `r1b_cambio_dezembro.py` | fluxo e PTAX em dezembro, 2016–2025 | −15,2 bi contra −3,5 bi nos outros meses | registro |
| câmbio · r1 | `r1b_cambio_modelo_base.py` | cenário base | central 5,156 … 5,223 | registro |
| câmbio · r1 | `r1b_cambio_modelo_decomp.py` | contribuição de cada exógena e multiplicador do CDS | CDS −1,60%, resíduo −2,17% | registro |
| câmbio · r1 | `r1b_cambio_modelo_canais.py` | de onde vem a subida da central | +1,31% de 4T26 a 1T28 | registro |
| câmbio · r1 | `r1b_cambio_modelo_cenarios.py` | worst e best, com e sem × 1,5 | worst 5,42→5,51 (4T26); best 5,01→4,94 | registro |
| câmbio · r1 | `r1b_cambio_probabilidades.py` | referência lognormal para as faixas | 35/39/27 no 4T26 | registro |
| PM · r1 | `pm_modelo_listar.py` | exógenas, coeficientes e cenário padrão | unidades e intervalos do posterior | registro |
| PM · r1 | `pm_exogenas_hoje.py` | nível de hoje e médias trimestrais das exógenas; DI10, NTN-B 10a, UST10 | rr_10a 4T26 = 6,89; o salto de 05/10 | registro |
| PM · r1 | `pm_cenarios.py` | base, worst, best e os temperos (i) | central 12,47 … 11,22 | registro |
| PM · r1 | `pm_sensibilidade_rr.py` | Selic do modelo contra a NTN-B 10a | +0,95 a +0,97 p.p. de Selic para +0,97 de NTN-B | registro (levou à decisão de 2026-10-21 sobre a central) |
| PM · r1 | `pm_temperos.py` | candidatos a tempero (i) | escolha de R.t3 e E.e1 | registro |
| PM · r1 | `pm_reunioes.py` | julgamento reunião a reunião em cadeia de probabilidades | tabela de reuniões e P da tese | registro |
| PM · r1 | `pm_tempero_ii.py` | piso de 25 p.b. por reunião e pausa por petróleo | tabela 3.3 | registro |
| PM · r1 | `pm_leituras.py` | contas pequenas do texto | surpresa do IPCA, juro real contra neutro, inflação implícita | registro |

## Divergências abertas

Nenhuma: os dois reports não leram um ao outro. Possível: o câmbio usou a Selic precificada na curva (12,13% em dez/27) e a PM põe a massa de 0,07 a 0,30 p.p. acima da Focus e da curva.

## O que os testes mudaram (2026-10-21)

- **PM:** nos dois trimestres reunião a reunião, a central passa a ser o caminho de reuniões do agente; a do modelo fica como referência (a regra de juros pedia 12,47% no 4T26 com a Selic em 13,75%).
- **Câmbio:** o agente não escreve de memória o que o Copom disse do câmbio; aguarda a S3.
- **F de PM:** passa a trazer o IC-Br em dólar e o núcleo EX0, que o agente tirou do A.

## Relatório

Nenhum: testes solo.
