# team_materials/ — Contexto para o Claude

## A regra da pasta

**Aqui entra só o que é MOSTRADO a alguém.** Slide, PDF, painel HTML interativo, vídeo, e o texto
narrativo escrito para ser lido de ponta a ponta por quem não conhece o assunto. Nada que exista
para ser *consultado* ou *mantido*: lista, inventário, mapa, rastreador de aquisição e nota de
pipeline vivem no [`repository/`](../repository/CLAUDE.md), qualquer que seja a voz em que foram
escritos.

O critério é o **uso**, não o formato nem a qualidade da escrita, e é essa a distinção que a pasta
já errou uma vez. Um `.md` bem escrito, sem jargão de mecanismo, ainda é material de base se a
pergunta que ele responde é "o que existe sobre isso" — e não "o que estamos dizendo ao time". Foi
por confundir os dois que três documentos de base moraram aqui de julho a setembro de 2026.

## A mudança de 2026-09-10

Os três saíram para o `repository/agent_mapping/`, a pedido do usuário:

| saiu de `team_materials/` | foi para | o que aconteceu |
|---|---|---|
| `bibliography.md` | `agent_mapping/recommended_bibliography/exchange_rate_bibliography.md` | movido inteiro |
| `conceptual_map.md` | fundido em `agent_mapping/conceptual_maps/exchange_rate_conceptual_map.md` | **apagado depois de fundir** — saiu daqui como arquivo próprio e, no mesmo dia, foi para dentro do mapa de ~140 conceitos: organizado pelos mesmos 9 clusters, era um segundo mapa conceitual com outro nome, e a convenção é **um por área** |
| `data_inventory.md` | fundido em `agent_mapping/recommended_data/exchange_rate_data_inventory.md` | **apagado depois de fundir** — era subconjunto estrito do upstream (as mesmas 8 categorias, na mesma ordem, sem as colunas de status), então só o racional *Why it matters* por categoria era novo |

O que **ficou**, e por quê: os dois exploradores HTML (interativos, feitos para navegar), os 7 PDFs
de modelo e de modelos mentais de gestoras, os 2 vídeos, e as duas introduções narrativas — prosa
contando a história intelectual do câmbio para quem nunca estudou o tema, com o
`introduction_pt.pdf` ao lado como exportação.

**As introduções são o caso limite da regra**, e a decisão foi explícita: elas citam a bibliografia
sem *serem* uma bibliografia, então o teste do uso as mantém aqui. Se um dia virarem um índice
comentado de fontes, mudam de pasta.

## Estrutura

**Área primeiro** — re-aninhada assim em 2026-09-10, no mesmo padrão de
`analytics/<país>/<área>/` e `repository/<área>/`:

```
<área>/agent_materials/   — material de apresentação daquela área macro. Hoje só exchange_rate:
                            2 exploradores HTML, 7 PDFs, 2 vídeos, as 2 introduções + o PDF
structure_materials/      — o que é do PROJETO INTEIRO, não de uma área: macro-project-context.md
                            (o racional estratégico, citado pelo CLAUDE.md da raiz), o "Mapa de
                            Usos (Tito).pdf" e a "Organizacao (Pedro).excalidraw"
```

**A regra do primeiro nível é o escopo, não o tipo**, e ela existe porque o aninhamento por área
não tem onde pôr material do projeto. Uma área nova é uma pasta nova ao lado de `exchange_rate/`;
o que vale para o repositório todo fica em `structure_materials/`, sem fingir pertencer a uma área.
Foi por isso que os dois arquivos de estrutura passaram algumas horas dentro de `exchange_rate/`
antes de subir: nenhum dos dois é de câmbio — o `.excalidraw` do Pedro não é nem de macro.

O `.excalidraw` do Pedro (737 elementos) desenha um pipeline de análise de **empresa** — 20-F/FRE,
release de resultado, transcrição de call, relatórios sell-side, cada um lido por IA para virar
fato, e as seções do relatório lendo esses fatos. Pelo critério de uso ele pertence aqui, e por não
ser de área nenhuma pertence ao primeiro nível; só não é assunto deste repositório, que é de macro.

## Pendências

- **A limpeza de 2026-09-10 apagou 9 dos 10 arquivos de `structure_materials/`** — as 3 versões do
  mapa de arquitetura, as 2 do research, o deck e os dois PDFs de 16 MB. Só
  `macro-project-context.md` foi restaurado, porque o `CLAUDE.md` da raiz o cita como o racional
  estratégico do projeto e o ponteiro estava quebrado. Os outros 8 continuam apagados e **a
  exclusão não está commitada**: qualquer um volta com `git checkout -- <caminho>` enquanto isso
  não for commitado. Depois, só pelo histórico.
- **83 dos 85 MB da pasta não estão no git** — todo binário (`.mp4`, `.pdf`, `.excalidraw`) está no
  `.gitignore`, então existe só no Dropbox, e os dois vídeos de câmbio são 83 MB disso. Não é
  defeito, mas significa que um clone limpo não tem o material de apresentação.
- **`kinea_fx_mental_models.pdf` é órfão** — ver o item em [`PENDENCIAS.md`](../PENDENCIAS.md).
