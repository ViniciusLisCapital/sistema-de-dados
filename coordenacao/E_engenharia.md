# Chat E — Engenharia do ciclo

**Objetivo.** Fazer a engrenagem acompanhar as decisões das outras frentes:
- fechar o ciclo 2026-10-27;
- consertar o corte do F por data de divulgação;
- aplicar o ciclo novo (chat A), o modelo novo (chat C) e os dois agentes novos (chat B) nas definições dos sete, na consolidação, no motor e no retrato;
- deixar a montagem dos nove pronta para o ciclo 2.

**Ler primeiro:**
- `README.md` desta pasta.
- `analytics/agent_system/CLAUDE.md`.
- `SISTEMA_AGENTES.md` III.III.ii–iii e IV.ii, iv, vi e vii.
- `obsidian/ciclos/2026-10-27/log.md` e `cobrancas.md`.


## O que precisa do usuário

1. **A regra do corte do F por divulgação**, numa janela. Hoje o F corta as tabelas pela data de referência, e o ciclo de 2026-10-02 trouxe o IPCA de set/26 (divulgado em 9/10) e a PMS de ago/26. O usuário decidiu corrigir antes do próximo ciclo; as opções são o calendário de divulgação (`domain/release_calendar/`) ou um atraso declarado por tabela. Recomendar depois de medir o que o calendário cobre.
2. **A base atualizada antes do ciclo 2.** A lista de lacunas da Fase 10 a reconferir:
    - a Focus parada em 09/10;
    - o CDS por carga manual;
    - `cred_fluxo_financeiro` em abr/26;
    - `mt_pnad` fora do job de rotina;
    - a posição de swap do BC em 01/08;
    - o EFGG e o PIB trimestral no 2T26;
    - `inflc_meta` só até 2026;
    - a inflação implícita de 1 ano em 6,66% contra a Focus em 4,48%, com a causa não confirmada;
    - o IPCA 24 meses suavizado, com 17 respondentes.


## Passos

- **E1a. Fechar o ciclo 2026-10-27.**
    - A cobrança C6 está aberta (fiscal, `fiscal_rf.md` seção 4, a subvenção: a frase põe o degrau de janeiro na base da inflação, e a inflação o pôs na cauda). Reabrir o fiscal só no trecho, como manda IV.vii.
    - Conferir todo número do relatório contra o banco (III.III.iii: o log diz "contra a fonte, no banco: não").
    - Registrar as duas coisas no log.
- **E1b. O corte do F por divulgação**, com teste. Atenção: `domain/release_calendar/` está sendo mexido por outro chat, fora deste plano; leia, não edite sem combinar pelo principal.
- **E1c.** Reconferir a lista de lacunas acima e entregar ao usuário, pelo principal, o que ele precisa atualizar.
- **E2. Aplicar as outras frentes**, conforme os pedidos chegam:
    - do chat A: o ciclo novo nas definições dos sete, no `web.md` e na `consolidacao.py`;
    - do chat C: a interface nova do `modelo.py`;
    - do chat B: o registro dos dois novos (a linha em `AGENTES`; `credito` → pasta `credit` no `OWNERS` do tracker e no `AREA` do retrato, que o `tests/test_conhecimento.py` exige iguais; a checagem de consulta entre todos os pares; a aba de crédito no tracker) e as mudanças que ele listar nas definições dos sete.
- **E3. Montagem de ensaio dos nove**, com literatura, numa data de teste fora de `obsidian/ciclos/`:
    - `dados` e retrato para cada um;
    - todos os testes da Verificação do PLANO;
    - um checklist para o chat F.

**Escreve:** este arquivo, as definições dos sete e do agente web, `consolidacao.py`, `dados/motor.py`, `dados/__main__.py`, `conhecimento.py`, os testes deles e `obsidian/ciclos/2026-10-27/` (só o fechamento). **Não escreve:** os templates e o moderador (chat A), o modelo (chat C), os módulos e as definições dos dois novos (chat B), o SISTEMA (principal).

**Pronto quando:** o ciclo 2026-10-27 está fechado, o corte por divulgação está no F com teste, os nove montam e todos os testes passam.


## Estado

- **2026-10-30 · E1a, C6 — feito antes do aviso do principal de parar.** Um `fiscal-analyst` novo (Opus, ~105k tokens), só com C6, o item do fiscal na seção 4 e o IN-E7 da inflação, sem editar arquivo; eu apliquei a frase dele. Arquivos tocados:
    - `obsidian/ciclos/2026-10-27/fiscal_rf.md`, uma frase (seção 4, "O fato"): sem o ato legal, o degrau de janeiro fica na cauda de alta da inflação, não na base; a base fiscal tira o custo. Nenhum caminho, faixa ou probabilidade muda.
    - `obsidian/ciclos/2026-10-27/cobrancas.md`: C6 marcada respondida, com a linha de resposta.
    - O relatório não muda: já dizia "cauda de alta da inflação".
    - Sem commit.
- **E1a, conferência contra o banco — planejado, parado até o principal liberar.**
    - O que: cada número do `relatorio.md` que vem de dado (seções 1, 2 e 5, a coluna "Hoje"; o apêndice é modelo e julgamento) contra o A do ciclo (`dados/A/*.csv.gz`, o banco congelado em 27/10), refazendo a conta do dado bruto, para pegar também erro de F. Número de modelo contra o `PF.json`; notícia contra `noticias/`; julgamento do agente não se confere.
    - Como: dois subagentes Sonnet em paralelo (seções 1–2; seções 3–5), cada um devolvendo uma tabela número · fonte · valor na fonte · bate/não bate. Sem editar o relatório.
    - Custo estimado: 0,6M a 1M tokens no total.
    - Arquivos que vai tocar: só `obsidian/ciclos/2026-10-27/log.md` (seção "Relatório": C6 e o resultado da conferência), e o relatório só se houver número errado, depois de passar pelo usuário.
- **E1b — medido, decisão com o principal (2026-10-30).** O vazamento só ocorre com A extraído depois da data do ciclo (02/10 sim; 27/10, extraído no dia, não). O calendário por tabela não conserta o IPCA: `inflc_agregados` mistura IPCA e IPCA-15, e o IPCA-15 de set já tinha saído em 02/10. Cobertura das 77 tabelas: 48 com período pelo calendário, 17 diárias, 12 sem regra. Recomendação: defasagem declarada por tabela/série, vintage onde houver, com teste que refaz 02/10. Opções enviadas ao principal.
- **E1c — reconferido no banco (2026-10-30).**
    - Focus em dia (23/10).
    - **CDS (`cmb_risco_pais`) voltou a 08/09 hoje às 11:14**, por recarga de outro chat. O backup em `domain/db/brasil/bloomberg/backup/` tem até 26/10. Alerta já com o principal.
    - `cred_fluxo_financeiro` em abr/26, sem fonte (o gráfico saiu do RPM).
    - `mt_pnad` em set/26.
    - Swap do BC em ago/26.
    - EFGG e PIB no 2T26 (normal até dezembro).
    - `inflc_meta` só até 2026.
    - Implícita de 1 ano × Focus e IPCA 24m suavizado não reconferidos (pedem G).
- **2026-10-30 · E1a, conferência — feita** (liberada pelo usuário via principal). Dois Sonnet, ~526k. ~100 números de dado batem com o A; apêndice = PF\* em 450 campos; 3 defeitos de redação/arredondamento (dezembro × nov+dez no fluxo, 1,8 → 1,7% do PIB no BNDES, "mercado fechado" → "leilões cancelados"), nenhum do F e nenhum que mova central, faixa ou probabilidade. Registrado em `log.md`, seção Relatório. Relatório **não** editado: as três correções vão ao usuário pelo principal.
- **CDS:** causa achada (o `run()` trunca e recarrega o xlsx de 08/09; a linha nova de `continuous` no calendário o fez rodar às 11:14 e o fará todo dia). Restauração pronta em script no scratchpad, mas bloqueada pela permissão desta sessão (escrita no banco sem aprovação direta do usuário aqui). Nada escrito no banco.
- **CDS fora do passe diário** (ver Decisões); `sync.continuas()` conferido: 26 tabelas, sem `cmb_risco_pais`, com as da Focus. **Restauração das 34 linhas bloqueada de novo** pela permissão desta sessão; pedida ao usuário diretamente aqui.
- **E1b fechado sem código**: decisão do usuário, nenhuma regra de corte (Decisões). Proposta pequena, a fazer só se o usuário quiser: a hora da extração no cabeçalho do F (o `_manifesto.json` já guarda `extraido_em`).
- **Próximo:** restaurar o CDS (aprovação do usuário); as três correções do relatório (com o usuário pelo principal). Depois disso, o ciclo 2026-10-27 está fechado e passo ao E1c/E2.
- **2026-10-30 · E1 fechado.**
    - O CDS voltou ao banco: a sessão do principal gravou as 34 linhas, com autorização do usuário dada lá.
    - Conferido daqui só com leitura: 6.423 linhas, fim em 26/10, último valor 137,43.
    - Registrado no `log.md`. O ciclo 2026-10-27 está fechado.
    - E1b terminou sem código, por decisão; o E1c está entregue acima.
- **2026-10-30 · E2, parte A — plano enviado ao principal, nada escrito.** Entrada: A3 → E (`A_ciclo.md`, Pedidos) e SISTEMA III.III.viii. Cinco blocos:
    - consolidação, com `tests/test_consolidacao.py`, por um Sonnet com teste;
    - as definições dos sete: o câmbio como piloto nesta sessão, depois um Opus para os outros seis e um teste de forma novo;
    - `web.md`;
    - a skill `/ciclo`;
    - a seção da consolidação em `analytics/agent_system/CLAUDE.md`.
    Custo estimado: ~1,1–1,4M. Espera o ok e as cinco escolhas pedidas ao principal.
- **E2 · bloco 3 (`web.md`) — feito, ~35k nesta sessão.**
    - O agente recebe `modo=demanda d=<n>`, lê `noticias/pedidos_d<n>.md` (gravado pela sessão com o bloco do moderador) e grava `demanda_d<n>.md`; os ids passam a `d<n>-<nn>`.
    - O ciclo anterior é a pasta que tem `relatorio.md`.
    - Os pedidos anteriores saem da seção 5 do `<agente>_r1.md`, ou do `_rf.md` nos ciclos antigos.
    - O modo pauta continua desligado.
- **E2 · bloco 1 (consolidação) — feito. Custo real: 134k (Sonnet) + ~15k de revisão aqui.**
    - Mudança: `--etapa p1|pf`, as duas lendo `<agente>_r1.json`; sem P2/rf; `*_r1b.json` ignorado; `caudas` validadas (os dois lados, base escrita no trimestre, upside ≥ base ≥ downside, só do principal) e listadas no P.
    - O segundo `pf` confere caminhos, central e faixa contra o `PF.json`, que são determinísticos; `--refazer` pula a conferência.
    - `tests/test_consolidacao.py`: 90 checks, `tudo ok`, rodado também por mim. O teste passou a usar o retrato de 2026-10-27, porque a pasta 2026-10-22 não existe mais, e confere pelo mtime que a pasta real não mudou.
    - `analytics/agent_system/CLAUDE.md`, seção da consolidação, reescrita.
- **E2 · bloco 2 (definições dos sete) — feito. Custo real: ~0,47M.** Piloto ~0,1M, Opus nos seis 273k, Sonnet do teste ~80k, revisão ~20k.
    - Os seis seguem o piloto. O que é de área ficou como estava. O ruído (`r1b`) foi só para câmbio e PM.
    - A PM ganhou a resposta ao câmbio sobre a Selic: o caminho que ela espera, não a central do modelo. Precisei a frase depois do Opus.
    - Fiscal e externo: a central é o próprio caminho base, e o PF* não a move.
    - Inflação, atividade e expectativas não são principal de nenhuma chave e dizem isso numa linha.
    - `tests/test_definicoes_agentes.py`: `tudo ok` nos sete e no `web.md`.
- **E2 · bloco 4, skill `/ciclo` — feita, ~50k nesta sessão.** `.claude/skills/ciclo/SKILL.md`:
    - a preparação (o ciclo anterior, o tipo de R1, os retratos de dados e do modelo, o log);
    - os passos 1–9: R1 com o ruído, D1, R1 final, P1, pauta (vista pelo usuário no ciclo 2), as voltas com as pausas do web, PF*, a atualização com o PF* refeito, e o relatório com as cobranças e a conferência contra a fonte;
    - o teto de 10M e a retomada de um ciclo pela etapa.
    - A lista de agentes é lida de `AGENTES`, nunca escrita na skill. O item 11 do teste de forma passou a conferir isso, além dos modos, dos comandos e das definições citadas; antes ele exigia os nomes dos agentes escritos.
- **E2 · diagrama — feito, ~60k nesta sessão.**
    - `analytics/agent_system/report.html` desenha o ciclo novo em três colunas (R1, R1 final, atualização), com o moderador entre as duas últimas, P1 e PF* em cima, o agente web embaixo (D1 e pausas) e o escrivão na saída.
    - Ganhou a caixa de detalhe do moderador; P1/PF*, modelo, web, a legenda e a caixa do R1 foram reescritos.
    - `Sistema de Agentes.html` foi regerado. Conferido em Chrome headless: 0 exceções, nenhum rótulo de seta sobre caixa, o detalhe abre.
    - `analytics/agent_system/CLAUDE.md` atualizado.
    - Os dois agentes novos entram quando o B registrar.
- **B4, mercado de trabalho — em parte feito, ~40k nesta sessão.**
    - **Já estava:** `mercado_trabalho → labor_market` no `AREA` do retrato e no `OWNERS` do tracker; `test_conhecimento.py` passa.
    - **Feito:** a coluna "Mercado de trabalho" na aba Exógenas, depois de Expectativas, em branco (sem papel em nenhuma exógena até o usuário preencher). O título mesclado e a validação foram estendidos à coluna nova, e as outras abas conferidas iguais. Backup no scratchpad. `test_consolidacao.py`, `test_dados_agentes.py` e `ler_tutela()` passam.
    - **Espera o B2:** as linhas em `AGENTES` do `dados/__main__.py` e do `consolidacao.py`. A primeira importa `dados/mercado_trabalho.py` e a segunda faz o teste de forma exigir `mercado-trabalho-analyst.md`, e nenhum dos dois existe ainda. Entram no mesmo momento que o módulo, com `conferir_consultas()` e os testes rodados.
- **B4, mercado de trabalho — fechado, ~70k no total.**
    - Linhas em `AGENTES` do `dados/__main__.py` e do `consolidacao.py`, depois do módulo e da definição do B; `conferir_consultas()` passa.
    - `test_dados_agentes.py`: oito agentes, a variante do MT na lista conhecida, e uma exceção explícita (`DIVIDIDAS`) para o arquivo da Focus de desocupação que atividade e MT dividem. Ela sai quando expectativas declarar esse recorte (B3, que pede a V.VII no SISTEMA).
    - Duas teses próprias do MT (`desocupacao`, `caged_12m`) validam como `propria` no contrato atual.
    - Passam `test_dados_mercado_trabalho.py`, `test_consolidacao.py`, `test_definicoes_agentes.py` (oito agentes) e `test_conhecimento.py`.
- **Literatura sempre (decisão do usuário, via principal, 2026-10-30) — feito, ~30k.**
    - Os sete: o comando de parada perdeu o `--sem-literatura`. O texto do retrato diz que todo ciclo roda com literatura e que 2026-10-27 foi o benchmark sem ela. O "Sobre o modelo" de expectativas deixou de tratar "nada neste ciclo" como padrão.
    - Skill: `--sem-literatura` só para refazer o benchmark.
    - As duas do B já estavam assim (citam a flag só como exceção).
    - Teste de forma: `tudo ok`.
- **Na fila:**
    - **Registro do crédito**, quando o B fechar o módulo: as duas listas `AGENTES`; `AREA`/`OWNERS` `credito → credit` (hoje `None`); a coluna na aba Exógenas.
    - **Esvaziar `DIVIDIDAS`** em `test_dados_agentes.py`, quando o B trocar o módulo de expectativas na B3. O principal põe a Focus de desocupação na V.VII no mesmo momento.
    - **Pedido do D, via principal, sem pressa:** o retrato da PM (`conhecimento.py`) passa a levar `obsidian/monetary_policy/central_bank/gestao_galipolo.md` como item do dono PM, camada 1, seguido pelos conceitos como as sínteses. Espera o D confirmar que a página existe (D2, gestão Galípolo).
- **Antes na fila** (principal, 2026-10-30): o B4 só para o `mercado_trabalho`, sem esperar o crédito.
    - A linha em `AGENTES` do `dados/__main__.py`.
    - `labor_market` no `OWNERS` do tracker e no `AREA` do retrato.
    - A checagem de consulta entre os pares.
    - A coluna na aba Exógenas, se couber.
    - Mandar o custo ao principal.
    - O principal mexeu numa linha de `dados/expectativas.py`: o fim da seção passou a ser "## (V.VIII)".
- **E2 · bloco 2, piloto do câmbio — escrito, ~0,1M nesta sessão.**
    - O que mudou: seção "The cycle", os modos `r1`/`r1-final`/`conversa`/`atualizacao`, a leitura do ciclo anterior, as caudas no JSON, as sete seções e a seção 7, as regras da conversa, e a 5.f.
    - Dois pontos com o principal: a 5.f por G sobre os coeficientes da (F), porque `modelo.rodar` não fixa a Selic (talvez um pedido ao C); e o critério de "diferença grande".
    - Os outros seis esperam o bloco 1.
    - Principal: piloto aprovado. A 5.f fica como aproximação, dita no R1, e a opção de fixar endógena vai como pedido ao C (Pedidos). O critério de "diferença grande" fica.

## Decisões

- 2026-10-30 (usuário, via principal), E1b: **nenhuma regra de corte por divulgação.** "O ciclo pode ver todo dado que já está na base, na verdade isso é mandatário, que o ciclo considere todos os dados disponíveis no momento." O ciclo extrai o A no dia e usa tudo o que está no banco. No máximo, o F diz no cabeçalho a hora da extração. Substitui o "corrigir o corte do F por data de divulgação" do objetivo deste chat.
- 2026-10-30 (usuário, via principal): as três correções da conferência vão direto no `relatorio.md`, sem reabrir o escrivão ("E corrige direto"). Feito; registrado no `log.md`.
- 2026-10-30 (usuário, via principal), E2 parte A: liberado com as cinco recomendadas.
    - 1a. A consolidação perde r2/rf. As etapas `p1` e `pf` leem `<agente>_r1.json`.
    - 2a. As caudas de exógena exigem upside ≥ base ≥ downside em cada trimestre.
    - 3a. O agente sem papel segura a exógena no r1, com "aguarda <principal>". Do r1-final em diante, lê as caudas em `caminhos/<principal>_r1.json`. P1 e PF mostram a tabela.
    - 4a. O câmbio sai como piloto nesta sessão, um Opus faz os outros seis, e um Sonnet faz o teste de forma.
    - 5a. Os blocos 1 e 3 andam em paralelo, depois vem o 2, e a skill `/ciclo` fica por último.
    - O diagrama (`generate_report.py` → `Sistema de Agentes.html`) entra no pacote, com o fluxo R1 → web → R1 final → P1 → conversa moderada → PF* → atualização → escrivão.
    - Sem commit; avisar o principal ao fim de cada bloco.
- 2026-10-30 (usuário, via principal): tirar o CDS (`cmb_risco_pais`) da carga diária. Feito no `calendar_2026.yaml` (de `max_age_days`, que o punha em `continuas()`; comentário de `no_release.continuous` reescrito), sem tocar no resto do diff do outro chat, sem commit.

## Pedidos

- **2026-10-30 → C** (vai pelo principal, no lote de afinação do modelo antes do ciclo 2): uma opção em `modelo.rodar` para fixar o caminho de uma endógena, a Selic em primeiro lugar. Hoje `modelo._caminhos` levanta ("é endógena: o modelo a resolve"). O pedido vem da decisão 5.f: o câmbio roda o cenário base com a Selic do modelo, a da curva e a da Focus. Até a opção existir, o R1 do câmbio aproxima por um G que só aplica à diferença de Selic os coeficientes da (F), e diz no R1 que é aproximação.
