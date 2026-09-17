# -*- coding: utf-8 -*-
"""Template de analise exploratoria -- COPIE para a pasta onde o modelo vai morar.

Nao rode a partir daqui: `utils/` e biblioteca, nao lugar de analise. O destino
e `analytics/<pais>/<area>/models/`, junto do modelo que esta sendo construido.

Como usar no VS Code: abra o arquivo copiado e aperte Shift+Enter dentro de uma
celula `# %%`. A primeira execucao pede o kernel -- escolha o `.venv` do projeto
(`.venv\\Scripts\\python.exe`). O grafico sai no painel da direita.

Pelo terminal (`uv run python <arquivo>.py`) o `# %%` e comentario comum e nada
aparece: ali o grafico precisa de `.show(config=ex.CONFIG)`, que abre no browser.
"""

# %% Setup
from utils import explore as ex

# %% O que existe
ex.tables("macro_brasil")          # sem argumento: lista os schemas
# ex.columns("macro_brasil", "atv_pib")

# %% Carregar
# `wide=True` pivota para uma coluna por serie; filtros viram WHERE.
df = ex.load("macro_brasil", "atv_pib", wide=True, seasonal_adjs="Y")
ex.peek(df)                        # inicio, fim, n pontos, ultimo valor

# %% Olhar
ex.plot(df, ["industria", "servicos"], title="PIB — setores")
# .show(config=ex.CONFIG) no fim se quiser zoom de scroll

# %% Consulta livre, quando a leitura precisa de join ou agregacao
# ex.q("SELECT date, value FROM atv_pib WHERE name = %(n)s",
#      schema="macro_brasil", params={"n": "industria"})

# %% Modelo
# A partir daqui e o seu trabalho. Os dados ja chegam com `value` em float e
# `date` em Timestamp, entao numpy/statsmodels funcionam direto.
