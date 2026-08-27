# Comunicados do Copom — o que a fonte permite

Levantado ao vivo contra a API do BCB em 2026-08-20, varrendo as reuniões 1–281 e lendo o texto de
todas as 233 que respondem. Redescobrir isso custa ~250 chamadas e nada está documentado pelo BCB.

Consumidores: [`_copom_texto.py`](_copom_texto.py) (sincronização + parsing),
[`pm_copom_projecoes.py`](pm_copom_projecoes.py) (a tabela), `connectors/bcb_copom.py` (o cliente).

Companheiro deste arquivo: [`relatorio_politica_monetaria.md`](relatorio_politica_monetaria.md), a
mesma coisa para o RPM/RI — a outra metade da tabela `pm_copom_projecoes`, e a que estende a série de
horizonte relevante para trás até 1999.

---

## As duas comunicações do Copom

| | Comunicado | Ata |
|---|---|---|
| Quando sai | dia da decisão | ~1 semana depois |
| Endpoint | `api/servico/sitebcb/copom/comunicados_detalhes?nro_reuniao=N` | `api/servico/sitebcb/atascopom/ultimas?quantidade=N&filtro=` |
| Formato | **JSON com HTML embutido** (`textoComunicado`) | **listagem JSON → PDF** (`/content/copom/atascopom/Copom280-not20260805280.pdf`) |
| Cobertura | reunião **48** (2000-06-20) → 280 (2026-08-05). De 47 para trás devolve `conteudo: []` | idem, via `quantidade` alto |
| Está no pipeline? | sim, tudo baixado | **não** — só PDF, sem parser |

Sem autenticação, resposta em UTF-8. O `?` no terminal Windows é codepage, não corrupção.

**Gotchas do endpoint:** timeouts esporádicos em requisições isoladas (o `_get()` do connector tenta
3 vezes com backoff — uma varredura completa sem isso quebra no meio); texto com lixo de editor
SharePoint (NBSP, zero-width space no início de parágrafo, entidades numéricas, classes
`ExternalClass…`).

## Os cinco regimes de comunicação

O comunicado mudou de forma várias vezes, e o que dá para extrair muda com ele.

| Reuniões | Datas | Projeções no comunicado |
|---|---|---|
| 48–199 | 2000-06 → 2016-06 | **nenhuma**. Um parágrafo curto, às vezes literalmente "sem declaração" |
| 200–205 | 2016-07 → 2017-02 | prosa, anos civis, dois cenários por frase ("nos cenários de referência e mercado, … 4,4% e 4,7%, respectivamente") |
| 206–247 | 2017-04 → 2022-06 | prosa, anos civis, um cenário por frase com o condicionamento explícito. De 2020-03 (229) em diante em `<ul><li>` |
| 248–263 | 2022-08 → 2024-06 | idem + a frase do **horizonte de seis trimestres à frente** "que suaviza o efeito ano-calendário" (só até a 253; 254–263 voltam a ser só ano civil) |
| 264 | 2024-07-31 | prosa; primeira vez com o HR de 6 trimestres como conceito **oficial** (meta contínua, Decreto 12.079/2024) |
| 265–280 | 2024-09-18 → | **Tabela 1 em HTML**: IPCA, livres e administrados × colunas de período |

## A armadilha do nome do cenário

O rótulo que o BCB usa mudou de significado no meio da série:

- **2016–2017**: "cenário de referência" = Selic e câmbio **constantes**; "cenário de mercado" =
  trajetórias da Focus.
- **2017–2020**: os nomes desaparecem e o condicionamento vira o próprio rótulo ("cenário com
  trajetórias para as taxas de juros e câmbio extraídas da pesquisa Focus" vs. "cenário com juros
  constantes a 6,50% a.a. e taxa de câmbio constante a R$/US$ 3,70").
- **2020–2022**: "cenário híbrido" e depois "cenário básico" — os dois com juros da Focus.
- **2022 → hoje**: "cenário de referência" = juros da Focus e câmbio por PPC, ou seja **o oposto**
  do que o mesmo nome significava em 2016.

Guardar o rótulo como se fosse a mesma coisa produziria uma série silenciosamente errada. Por isso a
coluna `cenario` da tabela classifica pelo **condicionamento** (`juros_esperado` / `juros_constante`) e
o rótulo original vai para `cenario_publicado`.

Ressalva de procedência: a definição do par referência/mercado de 2016–2017 vem da convenção do
Relatório de Inflação da época, **não** de uma frase do próprio comunicado — os comunicados daquele
período não explicitam o condicionamento. Isso, mais as duas projeções por frase, é o motivo de as
reuniões ≤ 205 ficarem fora da carga (`PRIMEIRA_REUNIAO_CARGA = 206`). São ~10 pontos.

## Horizonte relevante: três conceitos, uma coluna

`horizonte_relevante = 1` marca um período por reunião, mas o conceito por trás muda — daí a coluna
`regime`:

- **`hr_6_trimestres`** (264+): fixo em 6 trimestres à frente. Na Tabela 1 é sempre a **última
  coluna**; quando cai num 4º trimestre o BCB rotula só com o ano ("2026"), porque o acumulado em
  quatro trimestres ali é o ano civil fechado — normalizado para `2026Q4`.
- **`horizonte_suavizado`** (248–253): o BCB já publicava um ponto de 6 trimestres à frente, mas a
  meta ainda era anual. A 248 não nomeia o trimestre ("horizonte de seis trimestres à frente"), então
  o parser calcula reunião + 6 trimestres; da 249 em diante o trimestre vem escrito.
- **`ano_calendario`** (206–247, 254–263): o horizonte era o ano civil da meta, e o comunicado o
  nomeia em "horizonte relevante, que inclui o ano de 2024" / "os anos de 2023 e de 2024" /
  "o ano-calendário de 2022 e, em grau menor, o de 2023". Quando cita dois, o parser marca o último.
  As reuniões 206–228 não têm essa frase — ficam sem HR marcado.

**Não comparar as três eras sem ressalva**: não é a mesma pergunta.

## Conferência cruzada que a fonte oferece de graça

De 265 em diante o comunicado diz a projeção do HR **duas vezes**: na prosa ("A projeção de inflação
do Copom para o primeiro trimestre de 2028, atual horizonte relevante de política monetária, situa-se
em 3,2% no cenário de referência") e na última coluna da Tabela 1. `validar()` compara período e
valor — divergência acusa parser quebrado, não dado errado. Nas 16 reuniões com Tabela 1 as duas
fontes batem em todas, e o HR fica a exatamente 6 trimestres da reunião.

## Além das projeções

O mesmo texto carrega, sem esforço extra de fonte e já extraído pelo parser, mas **ainda não
gravado em tabela nenhuma**: o câmbio inicial do cenário, a hipótese de bandeira tarifária e as
expectativas Focus que o Comitê cita. A tabela irmã onde esses três cabem já existe —
[`pm_copom_reuniao`](pm_copom_reuniao.py), atributos de reunião, criada em 2026-08-25.

A **decisão de Selic e a direção** saíram dessa lista, e não porque foram gravadas daqui: a
`pm_copom_reuniao` as tira da SGS 432 (meta diária, desde 1999-03-05) cruzada com o calendário de
reuniões, que cobre 247 reuniões contra as 63 em que este texto escreve a decisão em prosa. O que o
parser lê virou **conferência independente** — as duas fontes não compartilham nem dado nem código,
e concordam nas 63.

Fora isso, ainda no texto e não extraído: o balanço de riscos (listas de alta/baixa e a assimetria),
a forward guidance e o placar de votos.
