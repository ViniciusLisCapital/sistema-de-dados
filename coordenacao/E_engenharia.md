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

(vazio: o chat começa aqui)

## Decisões

## Pedidos
