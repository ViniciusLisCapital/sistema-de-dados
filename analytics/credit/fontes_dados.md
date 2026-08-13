# Crédito — mapeamento de fontes (BCB)

Levantamento feito em 2026-08-12, ao vivo contra a planilha mensal do BCB "Tabelas de Estatísticas
Monetárias e de Crédito" (`202607_Tabelas_de_estatisticas_monetarias_e_de_credito.xlsx`, nesta mesma
pasta — 30 abas, cada uma publicando o código SGS de cada coluna própria) e confirmado contra a API
SGS ao vivo. **Atualizado no mesmo dia, mesma sessão** — a pedido do usuário ("quero tudo, todas as
modalidades"), as 21 tabelas de crédito que estavam só "disponíveis via SGS" foram todas trazidas para
`macro_brasil`, deixando só a Tabela 2 (redundante por construção) fora da base. Ver
[`domain/db/CLAUDE.md`](../../domain/db/CLAUDE.md) para o schema completo de todas as tabelas e
[`analytics/credit/CLAUDE.md`](CLAUDE.md) para a arquitetura do relatório (que hoje só consome uma
fração do que está listado aqui — ver o Pending desse arquivo).

**Só BCB (SGS) por enquanto** — não cobre CAGED/IPEA/IBGE nem qualquer outra fonte de dado de crédito
que eventualmente exista fora do SGS (ex: Serasa/Boa Vista, sempre pagos, nunca investigados a fundo
neste projeto). **Fora de escopo, mesma planilha**: as 3 abas de agregados monetários (Tabelas 28-30 —
base monetária, fatores condicionantes, M1-M4) são um tema diferente de crédito e não foram mapeadas
aqui.

## Tabela de cobertura

Uma linha por tabela da planilha-fonte do BCB (27 tabelas de crédito, Tabelas 1-27) — a granularidade
natural aqui, dado que cada uma já é uma unidade coesa de ~10-45 séries SGS. "Nº séries" conta as
colunas com código SGS próprio na planilha (inclui subtotais/totais quando a planilha os publica como
série própria, não só os itens-folha) — quando esse número é maior que o que está de fato na base, a
diferença é redundância com outra tabela já coberta ou uma célula sem código SGS próprio (ver
Comentário).

| Tabela BCB | Dado | Nº séries | Na base | Tabela/Colunas | Comentário |
|---|---|---|---|---|---|
| 1 | Crédito ampliado ao setor não financeiro — saldo, por instrumento (empréstimos/títulos/dívida externa) × setor (Governo/Empresas/Famílias) | 43 | ✅ (17 de 43) | `cred_credito_amplo` | As 26 colunas restantes são subtotais/totais/%PIB, deriváveis por soma das 17 folhas já armazenadas (%PIB precisaria do PIB como denominador, não temos essa coluna aqui — ver `cred_credito_resumo.pct_pib_total_total` para o conceito equivalente do sistema financeiro). |
| 2 | Resumo — Total, por recurso (Livre/Direcionado), 8 métricas | 24 | 🟡 N/A | — | Confirmado **totalmente redundante** com as Tabelas 3+4+5 — toda combinação (recurso, segmento) que expõe já existe com o mesmo código SGS numa das outras três. Não precisa série própria. |
| 3 | Resumo — Total (recurso), por segmento (PJ/PF/Total), 8 métricas | 24 | ✅ completo | `cred_credito_resumo` (`*_total_{pj,pf,total}`) | |
| 4 | Resumo — Recursos Livres, por segmento (PJ/PF/Total), 8 métricas | 24 | ✅ completo | `cred_credito_resumo` (`*_livre_{pj,pf,total}`) | |
| 5 | Resumo — Recursos Direcionados, por segmento (PJ/PF/Total), 8 métricas | 24 | ✅ completo | `cred_credito_resumo` (`*_direcionado_{pj,pf,total}`) | |
| 6 | Recursos livres — saldo por modalidade, PJ (capital de giro, desconto de duplicatas, veículos, ACC, cartão, cheque especial, arrendamento etc.) | 25 | ✅ (24 de 25) | `cred_modalidade_livre_pj` (`metrica='saldo'`) | Coluna "Total" excluída (redundante com `cred_credito_resumo.saldo_livre_pj`). |
| 7 | Recursos livres — saldo por modalidade, PF (consignado por origem, cartão, cheque especial, veículos, composição de dívidas etc.) | 22 | ✅ (21 de 22) | `cred_modalidade_livre_pf` (`metrica='saldo'`) | Coluna "Total" excluída (redundante com `cred_credito_resumo.saldo_livre_pf`). "Total não rotativo"/"Total rotativo" mantidos como modalidades próprias. |
| 8 | Recursos direcionados — saldo por modalidade, PJ (BNDES, rural, imobiliário, MPMe) | 13 | ✅ (12 de 13) | `cred_modalidade_direcionado_pj` (`metrica='saldo'`) | Coluna "Total" excluída (redundante com `cred_credito_resumo.saldo_direcionado_pj`). |
| 9 | Recursos direcionados — saldo por modalidade, PF (imobiliário, rural, BNDES, microcrédito) | 12 | ✅ (10 de 12) | `cred_modalidade_direcionado_pf` (`metrica='saldo'`) | Coluna "Total" excluída (redundante). "BNDES — capital de giro e financiamento a investimentos" não tem código SGS próprio na planilha-fonte (célula "-", confirmado ao vivo). |
| 10 | Recursos livres — concessões por modalidade, PJ | 24 | ✅ (22 de 24) | `cred_modalidade_livre_pj` (`metrica='concessao'`) | "Total" excluído; "Cartão de crédito — Rotativo e parcelado" sem código SGS próprio na planilha (célula "-"). |
| 11 | Recursos livres — concessões por modalidade, PF | 22 | ✅ (21 de 22) | `cred_modalidade_livre_pf` (`metrica='concessao'`) | "Total" excluído. |
| 12 | Recursos direcionados — concessões por modalidade, PJ | 13 | ✅ (12 de 13) | `cred_modalidade_direcionado_pj` (`metrica='concessao'`) | "Total" excluído. |
| 13 | Recursos direcionados — concessões por modalidade, PF | 12 | ✅ (10 de 12) | `cred_modalidade_direcionado_pf` (`metrica='concessao'`) | "Total" excluído; mesmo gap de código SGS do BNDES combinado que a Tabela 9. |
| 14 | Taxas de juros e spread — taxa de aplicação/captação/spread × PJ/PF/Total, geral + crédito não rotativo + recursos livres (com o mesmo cruzamento) | 45 | ✅ (30 de 45 têm código; 12 novos + 18 já cobertos pelas Tabelas 3/4/5) | `cred_credito_resumo` (`taxa_juros_*`/`spread_*`, incl. `*_nao_rotativo_*`/`*_livre_nao_rotativo_*`) | Taxa de aplicação/spread para total/livre/direcionado já existiam (mesmos códigos SGS das Tabelas 3-5); o corte "crédito não rotativo" (12 séries) era novo, trazido nesta rodada. **Taxa de captação (15 células) não tem código SGS em nenhuma delas** — confirmado ao vivo, célula "-" na planilha, não é gap de extração; genuinamente não publicada via SGS. |
| 15 | Recursos livres — taxas médias de juros por modalidade, PJ | 24 | ✅ (22 de 24) | `cred_modalidade_livre_pj` (`metrica='taxa_media'`) | "Total" excluído; "Cartão de crédito — À vista" sem código SGS próprio (célula "-"). |
| 16 | Recursos livres — taxas médias de juros por modalidade, PF | 19 | ✅ (17 de 19) | `cred_modalidade_livre_pf` (`metrica='taxa_media'`) | "Total" excluído; mesmo gap do cartão à vista. |
| 17 | Recursos direcionados — taxas médias de juros por modalidade, PJ | 12 | ✅ (11 de 12) | `cred_modalidade_direcionado_pj` (`metrica='taxa_media'`) | "Total" excluído. |
| 18 | Recursos direcionados — taxas médias de juros por modalidade, PF | 11 | ✅ (9 de 11) | `cred_modalidade_direcionado_pf` (`metrica='taxa_media'`) | "Total" excluído; mesmo gap do BNDES combinado. |
| 19 | Recursos livres — inadimplência (&gt;90d) por modalidade, PJ | 22 | ✅ (21 de 22) | `cred_modalidade_livre_pj` (`metrica='inadimplencia'`) | "Total" excluído. Cartão de crédito aqui é uma única série (sem quebra à vista/rotativo/parcelado) — granularidade mais grossa que saldo/concessão/taxa para esta mesma modalidade, confirmado na própria planilha (não é limitação nossa). |
| 20 | Recursos livres — inadimplência (&gt;90d) por modalidade, PF | 20 | ✅ (18 de 20) | `cred_modalidade_livre_pf` (`metrica='inadimplencia'`) | "Total" excluído; mesmo gap do cartão à vista. |
| 21 | Recursos direcionados — inadimplência (&gt;90d) por modalidade, PJ | 13 | ✅ (12 de 13) | `cred_modalidade_direcionado_pj` (`metrica='inadimplencia'`) | "Total" excluído. |
| 22 | Recursos direcionados — inadimplência (&gt;90d) por modalidade, PF | 12 | ✅ (10 de 12) | `cred_modalidade_direcionado_pf` (`metrica='inadimplencia'`) | "Total" excluído; mesmo gap do BNDES combinado. |
| 23 | Saldo a PJ por porte de empresa (MPMe/Grande) — saldo, inadimplência, saldo de maior risco (Res. CMN 4.966) | 10 | ✅ completo | `cred_credito_porte` | "Saldo — Total"/"Inadimplência — Total" não têm código SGS próprio na planilha (só MPMe/Grande têm) — as 2 métricas de "saldo de maior risco" têm Total próprio, esses sim capturados. |
| 24 | Saldo por atividade econômica (agropecuária, ~17 subsetores industriais, ~15 subsetores de serviços) | 38 | ✅ completo | `cred_credito_atividade_economica` | Quebra setorial mais fina de toda a planilha. |
| 25 | Saldo por tipo de cliente (setor privado PJ/PF, setor público federal/estadual-municipal) | 7 | ✅ completo | `cred_credito_tipo_cliente` | Único lugar da planilha que separa crédito ao setor público (governo como *tomador* de crédito bancário, diferente do que `cred_credito_amplo`/`fisc_divida` medem — esses veem o governo como *emissor* de dívida). A coluna "Total" (código 20539) é o mesmo código de `cred_credito_resumo.saldo_total_total` — mantida aqui como âncora de reconciliação da própria tabela, não uma série nova. |
| 26 | Controle de capital — saldo, inadimplência, provisões, por instituições públicas/privadas nacionais/estrangeiras | 9 | ✅ completo | `cred_credito_controle_capital` | |
| 27 | Endividamento e comprometimento de renda das famílias (%) — com e sem financiamento imobiliário | 4 | ✅ completo | `cred_credito_familias` (`endividamento_renda`, `endividamento_sem_imob`, `comp_renda_servico_total`, `comp_renda_servico_sem_imob`) | `cred_credito_familias` também tem `comp_renda_juros` (29033), que não faz parte desta tabela da planilha (série SGS avulsa, mesma fonte/tema). |

## Séries fora da planilha, mas já na base

Duas séries de `cred_inadimplencia_pj` vêm do SGS mas não pertencem a nenhuma das 30 abas desta
planilha específica — publicações separadas do BCB, mesma fonte (SGS), mapeadas por completo mesmo
assim:

| Série | Código SGS | Na base | Comentário |
|---|---|---|---|
| Selic (acumulada no mês, anualizada) | 4189 | ✅ `cred_inadimplencia_pj.selic` | Não é dado de crédito propriamente — usada como referência de custo de captação em toda a aba "Crédito Corporativo". |
| Atraso 15-90 dias, PJ | 21004 | ✅ `cred_inadimplencia_pj.atraso_pj` | Métrica de atraso "mais curto" que a inadimplência (&gt;90d) padrão de toda a planilha principal — não tem equivalente PF na base hoje. |
| PTC — Pesquisa Trimestral de Condições de Crédito (16 séries: 4 segmentos × oferta/demanda × observada/esperada) | 21380-21395 | ✅ `cred_ptc` (tabela própria) | Indicador de difusão sobre condições de crédito percebidas pelos bancos (equivalente ao Senior Loan Officer Opinion Survey do Fed), **não** dado de crédito bancário no sentido desta planilha. **Correção 2026-08**: os códigos usados antes aqui (21397/21399, só "Aprovação Observada" de 2 dos 4 segmentos) e em `analytics/painel_setores/painel_setores.py` (21397/21399/21401/21403, os 4 segmentos) estavam **obsoletos, não descontinuados** — o BCB manteve a pesquisa rodando sob outros códigos (confirmado ao vivo contra a planilha oficial `Series_PTC.xlsx` do BCB e por chamada direta à API); os códigos antigos simplesmente pararam de ser atualizados em 2022-10 enquanto a série real seguia até hoje. Migrado para tabela própria (`cred_ptc`, 16 séries — as 2 direções × 2 horizontes × todos os 4 segmentos, não só "Aprovação Observada" de 2), colunas antigas removidas de `cred_inadimplencia_pj` e `painel_setores.py` corrigido para os códigos certos. Ver `domain/db/brasil/bcb/cred_ptc.py` para o detalhe completo. |

## Leitura geral

- **BCB/SGS é fonte única e primária de todo dado de crédito bancário mapeado aqui** — diferente do
  levantamento de mercado de trabalho, não há um segundo distribuidor "concorrente" (BCB não
  republica dado de terceiros nesse tema, é quem produz a Nota de Crédito).
- **Cobertura completa desde 2026-08-12**: das 27 tabelas de crédito da planilha-fonte, 26 estão
  inteiramente representadas na base (a única exceção, Tabela 2, é redundante por construção — não é
  uma lacuna). 8 tabelas novas criadas nesta rodada, mais 2 tabelas existentes ampliadas
  (`cred_credito_resumo` +12 séries, `cred_credito_familias` +2 séries) — ver
  [`domain/db/CLAUDE.md`](../../domain/db/CLAUDE.md) para o schema de cada uma.
- **Toda coluna "Total" das tabelas de modalidade (6-13, 15-22) foi deliberadamente excluída** — já
  existe com o mesmo código SGS em `cred_credito_resumo` sob outro nome (ex: a coluna "Total" da
  Tabela 6 é o código 20543, idêntico a `cred_credito_resumo.saldo_livre_pj`). Nada foi perdido, só
  não duplicado.
- **Um pequeno número de células em todo o levantamento não tem código SGS próprio** — confirmado ao
  vivo (célula literal "-" na planilha, não erro de extração): toda a "taxa de captação" da Tabela 14
  (15 células), "Cartão de crédito — À vista" nas 3 tabelas de taxa média (15/16/20), "Cartão de
  crédito — Rotativo e parcelado" na Tabela 10, e "BNDES — Capital de giro e financiamento a
  investimentos" (combinado) nas 4 tabelas PF-direcionado (9/13/18/22). Essas colunas existem na
  planilha como texto/rótulo mas o BCB não publica uma série SGS independente para elas — não há como
  puxá-las via API, com ou sem esforço adicional.
- **Nenhuma tabela nova foi ainda conectada ao relatório `analytics/credit/`** — o escopo desta rodada
  foi só organizar os dados no MySQL; ver "Pending" em
  [`analytics/credit/CLAUDE.md`](CLAUDE.md) para o que fica disponível para uma futura expansão do
  relatório (por modalidade, por setor, por porte etc.).
- **`atraso_pj`/`selic`/PTCC não vêm desta planilha** — publicações SGS separadas, já mapeadas na base
  via `cred_inadimplencia_pj`, sem lacuna conhecida.
