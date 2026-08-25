"""
A arvore do PCE: uma linha por linha das tabelas 2.4.4U / 2.4.5U do BEA.

--------------------------------------------------------------------------------
POR QUE A CHAVE E O NUMERO DA LINHA, NAO O CODIGO
--------------------------------------------------------------------------------
13 codigos do BEA aparecem em DUAS linhas da tabela cada um: a mesma serie entra
duas vezes na arvore (`Health care` sob Household consumption e sob Market-based
PCE; `Religious organizations' services to households` sob Household consumption e
dentro da ponte dos NPISHs). Os valores sao identicos nas duas posicoes -- conferido
serie a serie -- so o lugar na hierarquia muda. E `ZZZZZZ` nao e nem codigo: e o
marcador do BEA para "nao publico serie para esta linha".

Entao `linha` e a chave, e `code` e atributo. E o mesmo raciocinio do
`inflc_cpi_dim` (onde `Apparel` tem o mesmo nivel nas duas arvores), invertido: la a
arvore estava na chave e o codigo era unico dentro dela; aqui a posicao E a
identidade.

--------------------------------------------------------------------------------
COMO A ARVORE E MONTADA
--------------------------------------------------------------------------------
Indentacao da coluna B, 2 espacos por nivel, com duas correcoes:

1. **A raiz.** O BEA indenta `Personal consumption expenditures` (linha 1) com 6
   espacos e `Goods`/`Services` com 0. E cosmetico do stub head. Aqui a linha 1 e
   nivel 0 por definicao e todo o resto e `indentacao/2 + 1`.
2. **O bloco de addenda (linhas 369-402) nao e arvore.** A indentacao dele e
   inconsistente na propria fonte: `Market-based PCE` (linha 377) vem MAIS indentado
   que as linhas que ele encabeca (378+). Sao 34 agregados especiais -- Control
   group, PCE food and energy, PCE excluding food and energy (o core), a familia
   market-based -- que existem para leitura, nao para particao. Ficam com
   `parent_linha = NULL`, `bloco = 'addenda'`, e nenhuma parentesco e inventado.
   `nivel` guarda a indentacao publicada para o relatorio poder exibir o recuo do
   BEA sem afirmar hierarquia.

--------------------------------------------------------------------------------
O SINAL: LINHAS QUE SUBTRAEM
--------------------------------------------------------------------------------
Quatro linhas comecam com `Less:` -- entram subtraindo no pai (`Less: Personal
remittances in kind to nonresidents`, `Less: Household insurance normal losses`,
`Less: Expenditures in the United States by nonresidents`, `Less: Receipts from
sales of goods and services by nonprofit institutions`). Duas colunas, porque as
duas perguntas sao diferentes:

  `sinal`            como a linha entra NO PAI:  +1 ou -1.
  `sinal_acumulado`  como a linha entra NO PCE:  o produto dos sinais no caminho
                     ate a raiz.

A segunda existe porque **a subarvore inteira de um `Less:` herda o sinal**: sao 4
linhas com `Less:` no rotulo, mas **19** que entram negativas no PCE. Os 12 itens
sob `Less: Receipts from sales...` nao dizem "Less:" no proprio rotulo e ainda
assim subtraem. Somar um nivel sem isso da 116% do PCE em vez de 100% -- foi
exatamente o que aconteceu na primeira versao desta carga.

--------------------------------------------------------------------------------
O QUE A VALIDACAO CONFERE (e se recusa a gravar)
--------------------------------------------------------------------------------
1. **As duas abas casam linha a linha** -- numero, rotulo e indentacao iguais em
   2.4.4U e 2.4.5U. E o que permite juntar indice e nominal por posicao.
2. **Aditividade em nominal, em toda a historia**: cada pai == soma dos filhos
   vezes o `sinal` de cada filho. 122 pais, 92 mil checagens, 810 meses. A
   tolerancia nao e um epsilon escolhido a dedo: o BEA publica cada linha
   arredondada ao milhao de dolares, entao a soma de k filhos contra um pai
   arredondado pode diferir de ate `0.5 * (k + 1)` so por arredondamento, e o teste
   e que o residuo caiba nesse limite. Cabe com folga -- o pior pai usa 80% do
   limite dele, e o erro absoluto maximo em toda a tabela e de US$ 3 milhoes num
   PCE de US$ 20 trilhoes. Um erro de arvore nao passaria por esse crivo: trocar um
   pai de lugar move bilhoes.
3. **Os niveis 1 a 4 somam 100% do PCE** (com sinal acumulado), e as 245 folhas
   somam 100.0000%. E o teste que diz ate onde uma decomposicao e completa: o
   nivel 5 cobre 95,5% e o 6 cai para 65,1%, porque a arvore nao tem profundidade
   uniforme.

Qualquer um dos tres falhando levanta em vez de gravar -- se o BEA mudar a
indentacao publicada ou renumerar as linhas, isso aparece como erro, nao como uma
arvore silenciosamente errada.

--------------------------------------------------------------------------------
DDL
--------------------------------------------------------------------------------
  CREATE TABLE macro_us.inflc_pce_dim (
      linha            SMALLINT     NOT NULL,
      code             VARCHAR(10),
      item_name        VARCHAR(180) NOT NULL,
      item_name_bruto  VARCHAR(220) NOT NULL,
      nivel            TINYINT      NOT NULL,
      parent_linha     SMALLINT,
      bloco            VARCHAR(10)  NOT NULL,
      sinal            TINYINT      NOT NULL,
      sinal_acumulado  TINYINT      NOT NULL,
      n_filhos         SMALLINT     NOT NULL,
      is_leaf          TINYINT      NOT NULL,
      tem_indice       TINYINT      NOT NULL,
      caminho          VARCHAR(900) NOT NULL,
      sort_order       SMALLINT     NOT NULL,
      idx_begin        VARCHAR(7),
      idx_end          VARCHAR(7),
      nom_begin        VARCHAR(7),
      nom_end          VARCHAR(7),
      PRIMARY KEY (linha),
      KEY idx_pai (parent_linha),
      KEY idx_code (code)
  );

Banco: macro_us.inflc_pce_dim -- PRIMARY KEY (linha)
"""

from __future__ import annotations

import pandas as pd

from connectors.bea import ABA_PCE_INDICE, ABA_PCE_NOMINAL, ler_tabela
from domain.db.us._gravar import gravar

_DATABASE = "macro_us"
_TABLE = "inflc_pce_dim"

# Primeira linha do bloco de agregados especiais ("Addenda:") da tabela 2.4.4U.
# Detectado por rotulo, com este valor so como conferencia -- ver `_bloco_addenda`.
_ADDENDA_ESPERADA = 369

# Rotulos que abrem o bloco de addenda. O BEA nao marca o bloco com uma linha
# "Addenda:" propria no xlsx (marca no HTML/PDF), entao o corte e pelo primeiro
# rotulo do bloco.
_PRIMEIRO_ADDENDA = "Control group"

# Folga sobre o limite de arredondamento, para o caso de o BEA publicar uma linha
# com meio milhao de casa (nao acontece hoje: o pior pai usa 80% do limite).
_FOLGA_ARRED = 0.05


def _bloco_addenda(estrutura: pd.DataFrame) -> int:
    """Numero da linha onde comeca o bloco de agregados especiais."""
    achou = estrutura.loc[estrutura["rotulo"] == _PRIMEIRO_ADDENDA, "linha"]
    if achou.empty:
        raise ValueError(
            f"nao achei a linha {_PRIMEIRO_ADDENDA!r}, que abre o bloco de addenda da "
            "tabela 2.4.4U. O BEA reorganizou a tabela -- confira antes de gravar."
        )
    linha = int(achou.iloc[0])
    if linha != _ADDENDA_ESPERADA:
        print(f"  aviso: o bloco de addenda comeca na linha {linha}, nao na "
              f"{_ADDENDA_ESPERADA} de sempre (o BEA inseriu ou removeu linhas acima)")
    return linha


def _montar(estrutura: pd.DataFrame) -> pd.DataFrame:
    """Nivel, pai, sinal, sinal acumulado e caminho, a partir da indentacao."""
    ini_addenda = _bloco_addenda(estrutura)
    df = estrutura.sort_values("linha").reset_index(drop=True).copy()

    df["bloco"] = ["addenda" if l >= ini_addenda else "principal" for l in df["linha"]]
    df["nivel"] = [
        0 if l == 1 else i // 2 + 1
        for l, i in zip(df["linha"], df["indentacao"])
    ]
    df["sinal"] = [-1 if r.lower().startswith("less:") else 1 for r in df["rotulo"]]

    # Pai: a ultima linha anterior de nivel-1, dentro do bloco principal.
    pai: dict[int, int | None] = {}
    pilha: dict[int, int] = {}
    for _, r in df.iterrows():
        linha, nivel = int(r["linha"]), int(r["nivel"])
        if r["bloco"] == "addenda":
            pai[linha] = None
            continue
        pilha[nivel] = linha
        pai[linha] = None if nivel == 0 else pilha.get(nivel - 1)
    df["parent_linha"] = [pai[int(l)] for l in df["linha"]]

    orfas = df[(df["bloco"] == "principal") & (df["nivel"] > 0)
               & df["parent_linha"].isna()]
    if not orfas.empty:
        raise ValueError(
            f"{len(orfas)} linhas do bloco principal ficaram sem pai "
            f"(linhas {orfas['linha'].tolist()[:8]}) -- a indentacao publicada pulou um "
            "nivel. Confira o xlsx antes de gravar."
        )

    # Sinal acumulado e caminho: descem pela arvore, na ordem das linhas (um pai
    # sempre aparece antes dos filhos).
    sinal_ac: dict[int, int] = {}
    caminho: dict[int, str] = {}
    for _, r in df.iterrows():
        linha = int(r["linha"])
        p = r["parent_linha"]
        if p is None or pd.isna(p):
            sinal_ac[linha] = int(r["sinal"])
            caminho[linha] = r["rotulo"]
        else:
            p = int(p)
            sinal_ac[linha] = int(r["sinal"]) * sinal_ac[p]
            caminho[linha] = f"{caminho[p]} > {r['rotulo']}"
    df["sinal_acumulado"] = [sinal_ac[int(l)] for l in df["linha"]]
    df["caminho"] = [caminho[int(l)][:900] for l in df["linha"]]

    n_filhos = df["parent_linha"].value_counts()
    df["n_filhos"] = [int(n_filhos.get(l, 0)) for l in df["linha"]]
    df["is_leaf"] = (df["n_filhos"] == 0).astype(int)
    df["sort_order"] = range(1, len(df) + 1)
    return df


def _validar_casamento(idx: pd.DataFrame, nom: pd.DataFrame) -> None:
    """As duas abas tem de casar linha a linha -- e o que permite juntar por posicao."""
    if len(idx) != len(nom):
        raise ValueError(
            f"2.4.4U tem {len(idx)} linhas e 2.4.5U tem {len(nom)} -- as duas abas "
            "deixaram de casar linha a linha, e o join por numero de linha "
            "(indice x nominal) nao vale mais."
        )
    for col in ("linha", "rotulo", "indentacao"):
        a, b = idx[col].tolist(), nom[col].tolist()
        if a != b:
            difs = [(x, y) for x, y in zip(a, b) if x != y][:5]
            raise ValueError(
                f"a coluna {col!r} difere entre 2.4.4U e 2.4.5U: {difs}. As abas "
                "deixaram de casar linha a linha."
            )
    print(f"  2.4.4U e 2.4.5U casam linha a linha: {len(idx)} linhas, mesmo rotulo "
          "e mesma indentacao")


def _validar_aditividade(df: pd.DataFrame, nominal: pd.DataFrame) -> None:
    """Cada pai == soma dos filhos x sinal, em nominal, em toda a historia.

    A tolerancia e o proprio arredondamento da fonte, nao um epsilon escolhido: o
    BEA publica em milhoes de dolares inteiros, entao k filhos arredondados contra
    um pai arredondado podem diferir de ate `0.5 * (k + 1)`. O teste e que o residuo
    caiba nesse limite -- um erro de arvore nao caberia, porque trocar um pai de
    lugar move bilhoes.
    """
    wide = nominal.pivot(index="date", columns="linha", values="value")
    sinal = dict(zip(df["linha"], df["sinal"]))
    filhos: dict[int, list[int]] = {}
    for _, r in df.iterrows():
        p = r["parent_linha"]
        if p is not None and not pd.isna(p):
            filhos.setdefault(int(p), []).append(int(r["linha"]))

    checagens, piores = 0, []
    for p, fs in filhos.items():
        if p not in wide.columns or any(f not in wide.columns for f in fs):
            continue
        difs = (sum(wide[f] * sinal[f] for f in fs) - wide[p]).abs().dropna()
        checagens += int(difs.shape[0])
        if difs.empty:
            continue
        limite = 0.5 * (len(fs) + 1)
        piores.append((float(difs.max()) / limite, float(difs.max()), p,
                       df.loc[df["linha"] == p, "rotulo"].iloc[0]))
    if not piores:
        raise ValueError(
            "nenhum pai pode ser conferido em nominal -- ou a tabela veio vazia, ou "
            "a arvore ficou sem pais. Nao gravo sem ter conferido nada."
        )
    piores.sort(reverse=True)
    ruins = [x for x in piores if x[0] > 1.0 + _FOLGA_ARRED]
    print(f"  aditividade em nominal: {len(piores)} pais conferidos, {checagens:,} "
          f"checagens, pior residuo usa {piores[0][0]:.0%} do limite de arredondamento "
          f"(US$ {piores[0][1]:.0f} mi, {piores[0][3][:34]})")
    for razao, abso, p, nome in ruins[:5]:
        print(f"    NAO FECHA  linha {p} {nome[:42]}: US$ {abso:.0f} mi = "
              f"{razao:.1f}x o arredondamento")
    if ruins:
        raise ValueError(
            f"{len(ruins)} pais nao fecham em nominal alem do que o arredondamento "
            "publicado explica. A indentacao mudou, ou uma linha 'Less:' deixou de "
            "ser 'Less:'."
        )


def _validar_particao(df: pd.DataFrame, nominal: pd.DataFrame) -> None:
    """Quais niveis particionam o PCE, no ultimo mes. Nivel 1-4 tem de dar 100%."""
    ultimo = nominal["date"].max()
    val = nominal[nominal["date"] == ultimo].set_index("linha")["value"]
    total = float(val.loc[1])
    principal = df[df["bloco"] == "principal"]

    for nivel in range(1, 5):
        g = principal[principal["nivel"] == nivel]
        soma = sum(float(val.get(int(l), 0.0)) * int(s)
                   for l, s in zip(g["linha"], g["sinal_acumulado"]))
        pct = 100 * soma / total
        if abs(pct - 100) > 0.01:
            raise ValueError(
                f"o nivel {nivel} soma {pct:.4f}% do PCE em {ultimo:%Y-%m}, nao 100%. "
                "Ou a arvore esta errada, ou um sinal acumulado esta errado."
            )
    folhas = principal[principal["is_leaf"] == 1]
    soma_f = sum(float(val.get(int(l), 0.0)) * int(s)
                 for l, s in zip(folhas["linha"], folhas["sinal_acumulado"]))
    pct_f = 100 * soma_f / total
    if abs(pct_f - 100) > 0.01:
        raise ValueError(
            f"as {len(folhas)} folhas somam {pct_f:.4f}% do PCE em {ultimo:%Y-%m}, "
            "nao 100%."
        )
    coberturas = []
    for nivel in sorted(principal["nivel"].unique()):
        if nivel == 0:
            continue
        g = principal[principal["nivel"] == nivel]
        soma = sum(float(val.get(int(l), 0.0)) * int(s)
                   for l, s in zip(g["linha"], g["sinal_acumulado"]))
        coberturas.append(f"n{nivel}={100 * soma / total:.1f}%")
    print(f"  particao em {ultimo:%Y-%m}: niveis 1-4 fecham em 100%, "
          f"{len(folhas)} folhas somam {pct_f:.4f}%")
    print(f"  cobertura por nivel: {' '.join(coberturas)}")


def _cobertura(df: pd.DataFrame, indice: pd.DataFrame,
               nominal: pd.DataFrame) -> pd.DataFrame:
    """Primeiro/ultimo mes de cada linha, em indice e em nominal, MEDIDOS da fonte."""
    def limites(obs: pd.DataFrame, pref: str) -> pd.DataFrame:
        g = obs.groupby("linha")["date"].agg(["min", "max"])
        return pd.DataFrame({
            f"{pref}_begin": g["min"].dt.strftime("%Y-%m"),
            f"{pref}_end": g["max"].dt.strftime("%Y-%m"),
        })

    out = df.set_index("linha").join(limites(indice, "idx")).join(limites(nominal, "nom"))
    out["tem_indice"] = out["idx_begin"].notna().astype(int)
    return out.reset_index()


def run(validar: bool = True) -> None:
    """Reconstroi macro_us.inflc_pce_dim a partir do xlsx da Secao 2 do BEA.

    Args:
        validar: refaz os tres testes (casamento das abas, aditividade em nominal,
                 particao dos niveis) e levanta se algum falhar. Default True -- e o
                 que detecta o BEA mudando a indentacao publicada em vez de gravar
                 uma arvore errada em silencio.
    """
    print("BEA Secao 2 (underlying detail, mensal)...")
    t_idx = ler_tabela(ABA_PCE_INDICE)
    t_nom = ler_tabela(ABA_PCE_NOMINAL)
    print(f"  {t_idx.titulo[:64]}")
    print(f"  {t_idx.publicado_em} | {t_idx.periodo} | {t_idx.sazonalidade}")

    if validar:
        _validar_casamento(t_idx.estrutura, t_nom.estrutura)

    df = _montar(t_idx.estrutura)
    principal = df[df["bloco"] == "principal"]
    print(f"  arvore: {len(principal)} linhas em {principal['nivel'].max() + 1} niveis, "
          f"{int((df['n_filhos'] > 0).sum())} pais, {int(principal['is_leaf'].sum())} folhas")
    print(f"  addenda: {int((df['bloco'] == 'addenda').sum())} agregados especiais "
          "(inclui o core, PCE excluding food and energy)")
    neg = df[df["sinal_acumulado"] < 0]
    print(f"  entram subtraindo no PCE: {len(neg)} linhas "
          f"({int((df['sinal'] < 0).sum())} com 'Less:' no rotulo, o resto herdando do pai)")

    nominal = t_nom.observacoes.copy()
    nominal["date"] = pd.to_datetime(nominal["date"])
    indice = t_idx.observacoes.copy()
    indice["date"] = pd.to_datetime(indice["date"])

    if validar:
        _validar_aditividade(df, nominal)
        _validar_particao(df, nominal)

    out = _cobertura(df, indice, nominal)
    out = out.rename(columns={"rotulo": "item_name", "rotulo_bruto": "item_name_bruto"})
    sem_idx = out[out["tem_indice"] == 0]
    print(f"  sem indice de preco publicado: {len(sem_idx)} linhas "
          f"({', '.join(sem_idx['item_name'].str[:34])}) -- o BEA marca com ZZZZZZ")

    cols = ["linha", "code", "item_name", "item_name_bruto", "nivel", "parent_linha",
            "bloco", "sinal", "sinal_acumulado", "n_filhos", "is_leaf", "tem_indice",
            "caminho", "sort_order", "idx_begin", "idx_end", "nom_begin", "nom_end"]
    out = out[cols].astype(object).where(out[cols].notna(), None)
    gravar(_DATABASE, _TABLE, out, sonda="linha")


if __name__ == "__main__":
    run()
