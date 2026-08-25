# TVP: a transmissão do juro real caiu? (2026-08-21)

**Órfãos.** Estes cinco arquivos estavam soltos na raiz do projeto e foram movidos para cá em
2026-08-25. **O script que os produziu não existe no repositório** — nenhum `.py` versionado
menciona `tvp`, e nada no projeto usa `pickle`. Rodou ad hoc na mesma sessão que escreveu
`modelo_painel.py` e `modelo_agregado.py` e não foi salvo. Então: **o resultado é auditável, a
receita não.** Para reproduzir ou estender, o código tem de ser reescrito.

Ficam em `referencia/` e não em `data/` justamente por isso — `data/` é o que os scripts da pasta
leem e escrevem, e nada aqui é lido por nada.

## A pergunta

Numa regressão do hiato (ou da atividade) contra o desvio do juro real em relação à neutra, o
coeficiente `b` — a força da transmissão — **cai ao longo do tempo?** Cada linha é uma hipótese
diferente sobre o que é a neutra, e é isso que a coluna `H` indica:

| `H` | medida de r* |
|---|---|
| `MM de r` | média móvel do juro real |
| `Focus 3,5a` | juro real esperado pela Focus, 3-5 anos |
| `const 5,0 (RPM)` | constante em 5,0% (a premissa do RPM) |
| `media expandida de r` | média de amostra expandida |
| `NTN-B fwd 5-20a` | forward implícito na NTN-B, 5-20 anos |
| `NTN-B fwd - premio` | o mesmo, descontado o prêmio |

`MA` é a defasagem/suavização e `k` o número de defasagens do bloco.

## Os três arquivos de resultado

- **`tvp_resumo.csv`** e **`tvp2_resumo.csv`** — a mesma tabela em duas especificações
  (a 2ª acrescenta `a_const`/`b_ols`, a referência de parâmetro constante, e `LR_M2`).
  Colunas que carregam a resposta: `b_ini`/`b_fim`/`b_ult` (o coeficiente no início, no fim e no
  último ponto), `sd_ult`, `P_neg_ult` (probabilidade de ele já ser negativo), `mult_*`/`m_*`
  (o multiplicador implícito), `LR` (razão de verossimilhança contra o modelo de parâmetro
  constante) e **`cai`**, o veredito SIM/não.
- **`tvp3_oos.csv`** — a corrida fora da amostra: `rmse_ar` (autorregressivo puro), `rmse_con`
  (parâmetro constante) e `rmse_tvp`, com os ganhos percentuais e as estatísticas t de
  Diebold-Mariano.
- **`tvp_paths.pkl`**, **`tvp2_paths.pkl`** — as trajetórias completas de `b_t`, um dicionário
  por medida de neutra.

## O que os números dizem

Nas 6 medidas, `cai = SIM` em **2 de 6** na 1ª especificação e **3 de 6** na 2ª, e as duas não
concordam sobre quais — ou seja, **o veredito depende de qual neutra se assume**, que é
exatamente a premissa em disputa (ver "O resultado que precisa de olhar" no `CLAUDE.md` da pasta).

E o teste fora da amostra é contrário ao TVP: `ganho_tvp` contra o AR puro é negativo nas
**30 de 30** configurações, com perdas de até 56% de RMSE, e nenhuma estatística t passa de
|1,8|. O parâmetro constante também perde para o AR, mas por muito menos (0,4% a 7%), e o TVP só
supera o constante em 2 das 30. A leitura honesta é que a queda de `b` aparece em amostra em
algumas especificações e **não sobrevive fora dela**.
