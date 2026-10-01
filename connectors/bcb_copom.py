"""Cliente da API de comunicados do Copom (Banco Central do Brasil).

Endpoint (nao documentado publicamente, mas e o que o proprio site do BCB consome):

    https://www.bcb.gov.br/api/servico/sitebcb/copom/comunicados_detalhes?nro_reuniao=N

Retorna JSON com o texto do comunicado em HTML no campo `textoComunicado`, o que e melhor
do que raspar a pagina: a Tabela 1 (projecoes de inflacao no cenario de referencia) vem
como `<table>` estruturada, nao como texto corrido.

## Cobertura (medida ao vivo em 2026-08-20)

Reuniao 48 (2000-06-20) e a mais antiga que responde -- de 47 para tras o endpoint devolve
`conteudo: []`. A 280a (2026-08-05) e a mais recente. Os comunicados dos primeiros anos sao
curtissimos (um paragrafo, as vezes "sem declaracao"); o formato longo com balanco de riscos
comeca por volta de 2016 e a Tabela 1 em HTML so a partir da 265a (2024-09-18).

## Atas

As atas saem pelo endpoint irmao, `copom/atas_detalhes?nro_reuniao=N` (achado 2026-09-30, mesmo
formato): `textoAta` em HTML e `urlPdfAta`. O HTML cobre as atas antigas e as recentes; da 200a
(2016-07) em diante ha tambem o PDF, e num trecho do meio so ha o PDF (`textoAta` vazio). `ata()`
devolve os dois e quem sincroniza decide (`domain/db/brasil/bcb/_copom_texto.sincronizar_atas`). O
HTML das atas antigas e exportacao do Word, um `<div>` por paragrafo, diferente do dos comunicados:
por isso `ata_html_para_markdown()`.

## Gotchas

- **O servidor e instavel**: timeouts esporadicos (WinError 10060) em requisicoes isoladas.
  `_get()` tenta 3 vezes com backoff; uma varredura completa do historico sem isso falha no meio.
- **Resposta em UTF-8**, mas o texto vem com lixo de editor SharePoint: NBSP (`\\xa0`), zero-width
  space (`\\u200b`) no inicio de paragrafos, entidades HTML numericas (`&#58;` para dois-pontos) e
  classes `ExternalClass...`/`ms-rteTable-default`. `html_para_markdown()` limpa tudo.
- **Buracos no meio**: reunioes que existiram mas nao respondem. `intervalo()` devolve os
  numeros faltantes em vez de silenciar.
"""

from __future__ import annotations

import html as _html
import json
import re
import time
import unicodedata
import urllib.request
from dataclasses import dataclass

BASE_URL = "https://www.bcb.gov.br/api/servico/sitebcb/copom/comunicados_detalhes"

# Listagem de atas -- usada aqui SO para o par numero/data das reunioes, ver
# `calendario_reunioes()`. O texto da ata (PDF) nao esta no pipeline.
_API_ATAS = "https://www.bcb.gov.br/api/servico/sitebcb/atascopom"
PRIMEIRA_REUNIAO = 48  # medido: 47 e anteriores devolvem conteudo vazio
_UA = "Mozilla/5.0 (compatible; LIS Capital macro data pipeline)"


@dataclass
class Comunicado:
    nro_reuniao: int
    data_referencia: str  # 'YYYY-MM-DD'
    titulo: str
    html: str

    @property
    def url(self) -> str:
        return f"{BASE_URL}?nro_reuniao={self.nro_reuniao}"

    def markdown(self) -> str:
        """Texto completo em markdown, com o cabecalho de procedencia."""
        corpo = html_para_markdown(self.html)
        return (
            f"Fonte: Banco Central do Brasil — API oficial de comunicados do Copom\n"
            f"({self.url})\n"
            f"Reunião: {self.nro_reuniao}ª reunião do Copom\n"
            f"Data de referência: {self.data_referencia}\n"
            f"Título: {self.titulo}\n"
            f"\n---\n\n"
            f"{corpo}\n"
        )

    def nome_arquivo(self) -> str:
        return f"copom_{self.nro_reuniao}_comunicado_{self.data_referencia}.md"


# --------------------------------------------------------------------------- HTTP


def _get(url: str, tentativas: int = 3, timeout: int = 40) -> dict:
    erro: Exception | None = None
    for k in range(tentativas):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": _UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read().decode("utf-8"))
        except Exception as e:  # timeout, 5xx, JSON invalido
            erro = e
            if k < tentativas - 1:
                time.sleep(2 * (k + 1))
    raise RuntimeError(f"falhou em {tentativas} tentativas: {url} ({erro})")


def calendario_reunioes(*, quantidade: int = 500, timeout: int = 60) -> dict[int, str]:
    """Numero da reuniao -> data, para TODAS as reunioes que o BCB lista.

    Vem da listagem de ATAS (`api/servico/sitebcb/atascopom/ultimas`), nao dos comunicados: a de
    atas cobre da 21a (1998-01-28) a hoje -- 260 reunioes, contra 233 dos comunicados, que so
    respondem da 48a em diante. E a unica fonte do projeto para o numero das reunioes de 1998-2000,
    e a que permite ligar uma edicao do RPM/RI a reuniao que a condiciona sem inferir numeracao.

    Inclui as reunioes EXTRAORDINARIAS (a 28a, de 1998-09-10, e uma), que entram na mesma sequencia
    numerica das ordinarias.

    Devolve `{numero: 'YYYY-MM-DD'}` -- data como string ISO, igual ao `data_referencia` do
    `Comunicado`. O PDF da ata em si nao esta no pipeline (ver `copom_comunicados.md`).
    """
    d = _get(f"{_API_ATAS}/ultimas?quantidade={quantidade}&filtro=", timeout=timeout)
    out: dict[int, str] = {}
    for item in d.get("conteudo") or []:
        m = re.match(r"\s*(\d+)", item.get("Titulo") or "")
        if not m:
            continue
        out[int(m.group(1))] = (item.get("DataReferencia") or "")[:10]
    return dict(sorted(out.items()))


ATAS_URL = "https://www.bcb.gov.br/api/servico/sitebcb/copom/atas_detalhes"
PRIMEIRA_ATA = 21  # medido: a listagem de atas comeca na 21a (1998-01-28)


@dataclass
class Ata:
    nro_reuniao: int
    data_referencia: str  # 'YYYY-MM-DD'
    data_publicacao: str
    titulo: str
    html: str
    url_pdf: str | None

    @property
    def url(self) -> str:
        return f"{ATAS_URL}?nro_reuniao={self.nro_reuniao}"

    def nome_base(self) -> str:
        return f"copom_{self.nro_reuniao}_ata_{self.data_referencia}"

    def cabecalho(self, origem: str) -> str:
        """Cabecalho de procedencia. `origem` e 'API' (texto em HTML) ou 'PDF' (extraido)."""
        return (
            f"Fonte: Banco Central do Brasil — ata do Copom ({origem})\n"
            f"({self.url_pdf if origem == 'PDF' else self.url})\n"
            f"Reunião: {self.nro_reuniao}ª reunião do Copom\n"
            f"Data de referência: {self.data_referencia}\n"
            f"Data de publicação: {self.data_publicacao}\n"
            f"\n---\n\n"
        )


def ata(nro_reuniao: int) -> Ata | None:
    """Uma ata. None quando a reuniao nao existe no endpoint."""
    d = _get(f"{ATAS_URL}?nro_reuniao={nro_reuniao}")
    c = d.get("conteudo") or []
    if not c:
        return None
    c = c[0]
    return Ata(
        nro_reuniao=int(c["nroReuniao"]),
        data_referencia=(c.get("dataReferencia") or "")[:10],
        data_publicacao=(c.get("dataPublicacao") or "")[:10],
        titulo=_limpa_texto(c.get("titulo") or ""),
        html=c.get("textoAta") or "",
        url_pdf=c.get("urlPdfAta") or None,
    )


def baixar(url: str, destino, tentativas: int = 3, timeout: int = 60) -> None:
    """Baixa um arquivo binario (o PDF da ata) para `destino`."""
    erro: Exception | None = None
    for k in range(tentativas):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": _UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                dados = r.read()
            with open(destino, "wb") as f:
                f.write(dados)
            return
        except Exception as e:
            erro = e
            if k < tentativas - 1:
                time.sleep(2 * (k + 1))
    raise RuntimeError(f"falhou em {tentativas} tentativas: {url} ({erro})")


def comunicado(nro_reuniao: int) -> Comunicado | None:
    """Um comunicado. None quando a reuniao nao existe no endpoint."""
    d = _get(f"{BASE_URL}?nro_reuniao={nro_reuniao}")
    conteudo = d.get("conteudo") or []
    if not conteudo:
        return None
    x = conteudo[0]
    return Comunicado(
        nro_reuniao=int(x["nro_reuniao"]),
        data_referencia=str(x["dataReferencia"])[:10],
        titulo=_limpa_texto(x.get("titulo") or ""),
        html=x.get("textoComunicado") or "",
    )


def ultima_reuniao(chute: int = 280, teto: int = 400) -> int:
    """Descobre o numero da reuniao mais recente publicada, subindo de `chute`."""
    n = chute
    while n <= teto:
        if comunicado(n) is None:
            return n - 1
        n += 1
    raise RuntimeError(f"nenhuma reuniao vazia ate {teto} -- revisar o teto")


def intervalo(inicio: int = PRIMEIRA_REUNIAO, fim: int | None = None, pausa: float = 0.4):
    """Itera (Comunicado | None) de `inicio` a `fim`. Gentil com o servidor por default."""
    if fim is None:
        fim = ultima_reuniao()
    for n in range(inicio, fim + 1):
        yield n, comunicado(n)
        time.sleep(pausa)


# ------------------------------------------------------------------- HTML -> markdown

_ZERO_WIDTH = dict.fromkeys(map(ord, "​‌‍﻿"), None)


def _limpa_texto(s: str) -> str:
    """Desfaz entidades, normaliza NBSP/zero-width e colapsa espacos."""
    s = _html.unescape(s)
    s = unicodedata.normalize("NFC", s)
    s = s.translate(_ZERO_WIDTH).replace("\xa0", " ")
    return re.sub(r"[ \t]+", " ", s).strip()


def _inline(frag: str) -> str:
    """HTML inline -> markdown inline. Aplicado dentro de um paragrafo ou celula."""
    frag = re.sub(r"<br\s*/?>", "\n", frag, flags=re.I)
    frag = re.sub(r"</?(?:em|i)\b[^>]*>", "*", frag, flags=re.I)
    frag = re.sub(r"</?(?:strong|b)\b[^>]*>", "**", frag, flags=re.I)
    frag = re.sub(r"<[^>]+>", "", frag)  # sub/sup/span/a/etc: fica so o texto
    frag = _limpa_texto(frag)
    # marcacao vazia que sobra de <em></em> em paragrafo de espacador
    frag = re.sub(r"(?<!\*)\*\*(\s*)\*\*(?!\*)", r"\1", frag)
    return frag.strip()


def _tabela_para_markdown(bloco: str) -> str:
    linhas = []
    for tr in re.findall(r"<tr\b[^>]*>(.*?)</tr>", bloco, flags=re.I | re.S):
        celulas = [
            _inline(td) for td in re.findall(r"<t[dh]\b[^>]*>(.*?)</t[dh]>", tr, flags=re.I | re.S)
        ]
        if celulas:
            linhas.append(celulas)
    if not linhas:
        return ""
    largura = max(len(l) for l in linhas)
    linhas = [l + [""] * (largura - len(l)) for l in linhas]
    out = ["| " + " | ".join(linhas[0]) + " |", "|" + "---|" * largura]
    out += ["| " + " | ".join(l) + " |" for l in linhas[1:]]
    return "\n".join(out)


def _lista_para_markdown(bloco: str) -> str:
    itens = [_inline(li) for li in re.findall(r"<li\b[^>]*>(.*?)</li>", bloco, flags=re.I | re.S)]
    return "\n".join(f"- {i}" for i in itens if i)


def html_para_markdown(texto_html: str) -> str:
    """Converte o `textoComunicado` do BCB em markdown.

    Nao e um conversor de HTML generico -- resolve as quatro formas que o BCB usa: paragrafos
    (`<p>`), listas (`<ul>/<ol>`, onde os comunicados de 2020-2023 poem as observacoes de cenario
    e com elas as projecoes), a Tabela 1 (`<table>`) e enfase inline (`<em>`/`<strong>`).
    """
    if not texto_html:
        return ""

    blocos: list[str] = []
    # varre <p>, <table> e <ul>/<ol> na ordem em que aparecem
    padrao = (
        r"<p\b[^>]*>(.*?)</p>"
        r"|<table\b[^>]*>(.*?)</table>"
        r"|<(?:ul|ol)\b[^>]*>(.*?)</(?:ul|ol)>"
    )
    for m in re.finditer(padrao, texto_html, re.I | re.S):
        if m.group(1) is not None:
            t = _inline(m.group(1))
            if t and t not in {"*", "**", "***"}:
                blocos.append(t)
        elif m.group(2) is not None:
            t = _tabela_para_markdown(m.group(2))
            if t:
                blocos.append(t)
        else:
            t = _lista_para_markdown(m.group(3))
            if t:
                blocos.append(t)

    if not blocos:  # comunicados antigos sem <p>: texto solto dentro de <div>
        t = _inline(re.sub(r"</?div[^>]*>", "", texto_html))
        if t:
            blocos.append(t)

    return "\n\n".join(blocos)


_BLOCO_ATA = re.compile(r"</?(?:p|div|h[1-6]|li|tr|table|thead|tbody|ul|ol|body|hr)\b[^>]*>", re.I)


def ata_html_para_markdown(texto_html: str) -> str:
    """Converte o `textoAta` em markdown, nas tres formas que o BCB usou.

    1998-2003: `<p>` com as secoes em `<b>`; 2004-2016: um `<div>` por paragrafo (exportacao do
    Word); recentes: `<p class="paragrafo">` numerado, `<h3>` por secao e tabelas. Em vez de casar
    pares de tags (os `<div>` antigos se aninham), toda tag de bloco vira quebra de paragrafo e o
    resto passa pelo mesmo `_inline()` dos comunicados. As tabelas saem antes, inteiras.
    """
    if not texto_html:
        return ""
    tabelas: list[str] = []

    def _guarda(m: re.Match) -> str:
        tabelas.append(_tabela_para_markdown(m.group(1)))
        return f"\n\n@@TABELA{len(tabelas) - 1}@@\n\n"

    t = re.sub(r"<(?:style|script)\b.*?</(?:style|script)>", "", texto_html, flags=re.I | re.S)
    t = re.sub(r"<table\b[^>]*>(.*?)</table>", _guarda, t, flags=re.I | re.S)
    t = re.sub(r"<h[1-6]\b[^>]*>(.*?)</h[1-6]>", lambda m: f"\n\n@@H@@{m.group(1)}\n\n", t,
               flags=re.I | re.S)
    t = _BLOCO_ATA.sub("\n\n", t)

    blocos: list[str] = []
    for bruto in re.split(r"\n\s*\n", t):
        bruto = bruto.strip()
        if not bruto:
            continue
        m = re.fullmatch(r"@@TABELA(\d+)@@", bruto)
        if m:
            if tabelas[int(m.group(1))]:
                blocos.append(tabelas[int(m.group(1))])
            continue
        titulo = bruto.startswith("@@H@@")
        linha = _inline(bruto.replace("@@H@@", "").replace("\n", " "))
        if not linha or linha in {"*", "**", "***"}:
            continue
        blocos.append(f"### {linha.strip('*').strip()}" if titulo else linha)
    return "\n\n".join(blocos)
