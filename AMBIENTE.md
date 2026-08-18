# Ambiente de Desenvolvimento e Gerenciamento de Pacotes (uv)

Este documento explica como o ambiente Python deste projeto é montado e mantido.
O objetivo é que **qualquer pessoa, mesmo sem conhecer o `uv`**, consiga instalar,
rodar e atualizar o projeto sem quebrar nada.

Se você só quer "fazer funcionar numa máquina nova", pule direto para
[Setup numa máquina nova](#setup-numa-máquina-nova).

---

## 1. O que é o `uv` e por que usamos

[`uv`](https://docs.astral.sh/uv/) é um gerenciador de pacotes e ambientes
virtuais para Python (escrito em Rust pela Astral). Ele substitui, em uma única
ferramenta, o que antes exigia `pip` + `venv` + `pip-tools`.

**Por que adotamos:**

- **Reprodutibilidade.** O `uv` grava um *lockfile* (`uv.lock`) com a versão
  exata de **todos** os pacotes — diretos e transitivos. Toda máquina instala
  exatamente o mesmo conjunto. Acaba o "na minha máquina funciona".
- **Velocidade.** Resolução e instalação de dependências são ordens de grandeza
  mais rápidas que o `pip`.
- **Uma ferramenta só.** Cria o ambiente virtual, resolve dependências, instala,
  trava versões e roda scripts — sem precisar ativar/desativar venv manualmente.

> ⚠️ **Regra de ouro:** neste projeto **nunca** use `pip install` diretamente.
> Sempre `uv add` / `uv sync`. O `pip` instala sem atualizar o `pyproject.toml`
> nem o `uv.lock`, o que silenciosamente quebra a reprodutibilidade.

---

## 2. Os arquivos que compõem a configuração

| Arquivo / pasta | É commitado? | O que é | Quem edita |
|---|---|---|---|
| `pyproject.toml` | ✅ Sim | **A lista de desejos.** Declara as dependências *diretas* (com faixas de versão flexíveis) e os metadados do projeto. | Você (via `uv add`) |
| `uv.lock` | ✅ Sim | **A receita exata.** Versão pinada + hash de cada pacote (diretos *e* transitivos) e o grafo de dependências. Garante instalação idêntica em toda máquina. | Ninguém à mão — o `uv` gera |
| `.venv/` | ❌ Não | O ambiente virtual em si (os pacotes instalados de fato). É descartável e recriável a partir do `uv.lock`. | Ninguém — o `uv` gera |
| `.vscode/settings.json` | ❌ Não | Aponta o interpretador do VS Code para `.venv/Scripts/python.exe`. Path absoluto e específico de cada máquina — cada dev configura localmente. | Você, na sua máquina |
| `.env.example` | ✅ Sim | **Modelo** das variáveis de ambiente (chaves sem valores). Serve de base para criar o `.env`. | Você, ao adicionar uma var nova |
| `.env` | ❌ **Nunca** | Credenciais reais (banco, API keys). Local de cada máquina. | Você, manualmente |
| `sistema_de_dados.egg-info/` | ❌ Não | Metadado gerado pela instalação editável (`uv pip install -e .`). Descartável. | Ninguém — gerado |

### Relação entre os três arquivos centrais

```
pyproject.toml          uv.lock                    .venv/
"quero pandas, numpy"   "pandas==2.2.2 (hash...)"   pandas de fato instalado
"faixas flexíveis"  →   "versões exatas pinadas" →  "ambiente real e rodável"
 (o que você pede)       (o que foi resolvido)       (o que está no disco)
```

- Você edita o `pyproject.toml` (geralmente via `uv add`).
- O `uv` **resolve** as faixas em versões exatas e escreve o `uv.lock`.
- O `uv sync` lê o `uv.lock` e materializa tudo dentro do `.venv`.

---

## 3. Setup numa máquina nova

Pré-requisito: ter o `uv` instalado.
[Instruções oficiais](https://docs.astral.sh/uv/getting-started/installation/) —
no Windows, via PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Depois, dentro da pasta do projeto:

```powershell
# 1. Cria o .venv e instala TUDO exatamente como no uv.lock
uv sync

# 2. Instala o próprio projeto em modo editável (faz os imports funcionarem)
uv pip install -e .

# 3. Cria o arquivo de credenciais a partir do modelo e preenche com os valores reais
#    (peça os valores a alguém do time — o .env nunca é versionado)
cp .env.example .env
```

Pronto. Para conferir que deu certo:

```powershell
uv run python jobs\update_oraculo.py
```

### Por que o `uv pip install -e .` (modo editável)?

Este projeto **é também um pacote** (`connectors`, `domain`, `analytics`,
`utils`). A instalação editável cria um arquivo `.pth` dentro do `.venv` que
aponta para a raiz do projeto, fazendo com que esses imports funcionem de
qualquer lugar.

Sem esse passo, rodar `python jobs\update_oraculo.py` falha com:

```
ModuleNotFoundError: No module named 'analytics'
```

É um passo único por máquina (refazer só se recriar o `.venv` do zero).

> 📌 Para um diretório virar pacote importável, ele precisa de um `__init__.py`.
> Todas as pastas do projeto (`connectors/`, `domain/`, `analytics/`, `utils/`)
> já têm — mas se criar uma pasta-pacote nova, lembre de adicionar o `__init__.py`,
> senão o `setuptools.packages.find` não a encontra.

### Dependência de sistema opcional: compilador C++ (para PyMC)

`pymc` (usado em `analytics/exchange_rate/models/bayesian_deviation_model.py` e
futuros modelos bayesianos) roda via `pytensor`, que compila cada modelo para
C por padrão. **Sem compilador C++ no PATH, `pytensor` cai para um fallback em
Python puro** — funciona, mas cada `pm.sample()` fica ordens de magnitude mais
lento (minutos → potencialmente nunca termina em modelos maiores).

Instalado nesta máquina em 2026-07-23 via MSYS2 (não `conda`, para não
introduzir um segundo gerenciador de pacotes só por causa do compilador):

```powershell
winget install --id MSYS2.MSYS2 --source winget --accept-source-agreements --accept-package-agreements --silent
& "C:\msys64\usr\bin\bash.exe" -lc "pacman -S --noconfirm --needed mingw-w64-x86_64-gcc"
```

Depois, `C:\msys64\mingw64\bin` precisa estar no `PATH` (setado no `PATH` de
usuário via `[Environment]::SetEnvironmentVariable`, então persiste em
terminais/sessões *novas* — um terminal já aberto antes dessa mudança não
enxerga o PATH atualizado sem reiniciar).

Verificar se está funcionando:

```powershell
uv run python -c "import pytensor; print(pytensor.config.cxx)"
# deve imprimir o caminho do g++.exe, não uma string vazia
```

Numa máquina nova sem esse setup: os modelos PyMC ainda rodam (fallback Python),
só mais devagar — refazer o passo acima só se isso virar um gargalo real.

`pytensor` também avisa que não encontra uma instalação de BLAS ("PyTensor
could not link to a BLAS installation") — não bloqueia nada nesta escala de
modelo, mas para modelos bayesianos bem maiores no futuro, considerar
`OpenBLAS` ou um numpy linkado com BLAS via conda.

### Dependência de sistema opcional: X-13ARIMA-SEATS (ajuste sazonal)

O X-13ARIMA-SEATS do US Census Bureau é um **executável Fortran externo**, não um
pacote Python — não entra no `pyproject.toml` nem no `uv.lock`, e por isso o
`uv sync` não o instala. `statsmodels` só o encapsula: `x13_arima_analysis()`
escreve um arquivo `.spc`, chama o binário via subprocess, e lê o resultado de
volta. Sem o binário, qualquer chamada levanta exceção.

Instalado nesta máquina em 2026-08-17, build **ascii v1.1 Build 62**. Não tem
instalador, não pede admin, não precisa de compilador — é só descompactar:

```powershell
$dest = "$env:LOCALAPPDATA\x13as"
New-Item -ItemType Directory -Force $dest | Out-Null
Invoke-WebRequest -Uri "https://www2.census.gov/software/x-13arima-seats/x13as/windows/program-archives/x13as_ascii-v1-1-b62.zip" -OutFile "$dest\x13as_ascii-v1-1-b62.zip"
Expand-Archive -Path "$dest\x13as_ascii-v1-1-b62.zip" -DestinationPath $dest -Force

# O statsmodels procura os nomes de binario em ordem e "x13as.exe" e o primeiro
# da lista -- o zip traz "x13as_ascii.exe", entao duplique com o nome esperado.
Copy-Item "$dest\x13as\x13as_ascii.exe" "$dest\x13as\x13as.exe"

# Variavel de usuario (persiste em terminais NOVOS, igual ao PATH do MSYS2 acima)
[Environment]::SetEnvironmentVariable("X13PATH", "$dest\x13as", "User")
```

Verificar se está funcionando:

```powershell
uv run python -c "import os, numpy as np, pandas as pd; from statsmodels.tsa.x13 import x13_arima_analysis; r=np.random.default_rng(0); s=pd.Series(100+np.arange(120)*0.3+5*np.sin(np.arange(120)*2*np.pi/12)+r.normal(0,1,120), index=pd.period_range('2015-01',periods=120,freq='M')); print(x13_arima_analysis(s, x12path=os.environ['X13PATH'], prefer_x13=True).seasadj.iloc[-3:])"
# deve imprimir 3 valores dessazonalizados, nao uma excecao
```

Pontos de atenção:

- **Passe `prefer_x13=True`** nas chamadas. Sem isso o `statsmodels` consulta
  `X12PATH` (o programa antecessor) em vez de `X13PATH`.
- `KeyError: 'X13PATH'` num terminal que já estava aberto quando a variável foi
  criada é o comportamento esperado, não um erro de instalação — o processo herdou
  o ambiente antigo. Abra um terminal novo, ou leia o valor persistido direto:
  `$env:X13PATH = [Environment]::GetEnvironmentVariable("X13PATH","User")`.
- O ruído no comando de verificação acima não é decorativo: uma série sintética
  *perfeitamente* linear + sazonal faz o X-13 abortar com "Differencing has
  annihilated the series". Ver também "série com valores zero ou negativos" — o
  X-13 recusa transformação automática nesse caso.
- O `.zip` também traz `docs/docX13AS.pdf` e `docs/qrefX13ASpc.pdf` — a
  referência completa da linguagem de `.spc`, necessária para qualquer coisa que
  o wrapper do `statsmodels` não expõe (feriados móveis brasileiros via `genhol`,
  p. ex.).
- Numa máquina nova sem esse setup, o comportamento **não** é um fallback
  silencioso para STL: a chamada falha com exceção. Quem escreve código novo que
  usa X-13 é responsável por decidir o que fazer no `except` — e por registrar
  quando uma série caiu para STL, senão o resultado final mistura dois métodos
  sem marcador de qual é qual.

Contexto de quando usar X-13 em vez de STL, escopo por série, e os problemas
práticos conhecidos: [`analytics/seasonal_adjustment.md`](analytics/seasonal_adjustment.md).

---

## 4. Tarefas do dia a dia

Todos os comandos rodam na raiz do projeto. Você **não** precisa ativar o venv —
o `uv` cuida disso. Para rodar qualquer coisa dentro do ambiente, use `uv run`.

```powershell
# Rodar um script dentro do ambiente
uv run python jobs\update_db.py

# Adicionar um pacote (atualiza pyproject.toml E uv.lock E instala no .venv)
uv add nome-do-pacote

# Adicionar com versão mínima
uv add "pandas>=2.0"

# Adicionar uma dependência de desenvolvimento (grupo "dev": ipython, ipdb...)
uv add --optional dev nome-do-pacote

# Remover um pacote
uv remove nome-do-pacote

# Reinstalar/sincronizar o ambiente com o lock (após git pull, p.ex.)
uv sync
```

> Sempre que você der `git pull` e o `pyproject.toml`/`uv.lock` tiverem mudado,
> rode `uv sync` para alinhar seu `.venv`.

---

## 5. Como atualizar versões de pacotes

```powershell
# Atualizar UM pacote para a versão mais nova permitida pelo pyproject.toml
uv lock --upgrade-package pandas
uv sync

# Atualizar TODOS os pacotes (re-resolve o lock inteiro) — faça com cautela
uv lock --upgrade
uv sync
```

Depois de atualizar, **rode os testes / um job real** antes de commitar, e
**commite o `uv.lock` junto** com qualquer mudança. O lock atualizado é o que
propaga a nova versão para o resto do time.

---

## 6. Manutenção e regras

- ✅ **Commite sempre o `pyproject.toml` e o `uv.lock` juntos.** Eles andam em par.
- ❌ **Nunca edite o `uv.lock` à mão.** É gerado; edição manual corrompe os hashes.
- ❌ **Nunca use `pip install`** — sempre `uv add` (ver regra de ouro na [seção 1](#1-o-que-é-o-uv-e-por-que-usamos)).
- ❌ **Não commite `.venv/`, `.env` nem `*.egg-info/`.** São locais/gerados.
- 🔁 **Recriar o ambiente do zero** (quando algo "embola"):
  ```powershell
  Remove-Item -Recurse -Force .venv
  uv sync
  uv pip install -e .
  ```
- ⬆️ **Atualizar o próprio `uv`:** `uv self update`.

### Estado atual da configuração (para referência)

- `uv` testado na versão **0.11.16**.
- Lockfile no formato `version = 1`, `revision = 3`.
- `requires-python = ">=3.10"`.
- ~74 pacotes resolvidos no `uv.lock`.
- Build backend: `setuptools` (declarado no `pyproject.toml`).

---

## 7. Troubleshooting

| Sintoma | Causa provável | Solução |
|---|---|---|
| `ModuleNotFoundError: No module named 'analytics'` (ou `connectors`, etc.) | Faltou a instalação editável | `uv pip install -e .` |
| VS Code não acha os imports / usa o Python errado | Interpretador apontando para fora do `.venv` | Selecionar o interpretador `.venv\Scripts\python.exe` (já é o default em `.vscode/settings.json`) |
| Erro de credencial / conexão com o banco | `.env` ausente ou incompleto | Criar/preencher o `.env` na raiz |
| Ambiente "estranho" após `git pull` | `.venv` dessincronizado do lock | `uv sync` |
| Quero garantir que o `.venv` reflete exatamente o lock | — | `uv sync` (remove o que sobra e instala o que falta) |

---

## 8. Pendências e inconsistências conhecidas

Item opcional, não bloqueia o uso:

- **Não há `.python-version`.** O projeto roda em qualquer Python `>=3.10`. Se
  quiser fixar uma versão para todo o time, crie um `.python-version` na raiz.

> Resolvido em 2026-06: o `requirements.txt` legado (pré-`uv`, que contradizia o
> `pyproject.toml`) foi removido, e o `.env.example` foi criado como modelo de
> credenciais. A fonte de verdade das dependências é `pyproject.toml` + `uv.lock`.
