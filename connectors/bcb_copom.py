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

As atas NAO saem por este endpoint. Sao PDF, listados em
`api/servico/sitebcb/atascopom/ultimas?quantidade=N&filtro=`, com o caminho do arquivo no
campo `Url`. Nao implementado aqui.

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
