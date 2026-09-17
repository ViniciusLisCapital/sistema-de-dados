@echo off
REM ---------------------------------------------------------------------------
REM Atalho MANUAL para o passe diario das series de mercado (schemas macro_*).
REM
REM A tarefa agendada "Macro - series diarias" NAO usa este arquivo -- ela chama
REM .venv\Scripts\pythonw.exe jobs\atualizar_diario.py direto, para nao abrir
REM janela nenhuma (um .bat e executado pelo cmd.exe, que e binario de console,
REM e a cada disparo pipocaria um prompt preto na frente de quem estiver usando
REM a maquina).
REM
REM Este atalho existe para o caso de dois cliques: mesma logica, mesmo log, com
REM `python` em vez de `pythonw` para voce ver o andamento na tela.
REM
REM O QUE RODA: jobs\atualizar_diario.py, que e um envelope em volta de
REM `update_db.py --continuous`. A lista de tabelas vem de
REM `no_release.continuous` em domain\release_calendar\calendar_2026.yaml --
REM acrescentar ou tirar tabela e editar aquele YAML, nunca este arquivo.
REM
REM LOG: logs\continuous_AAAA-MM-DD.log (o proprio Python escreve; poda em 30
REM dias). Codigo de saida propagado.
REM ---------------------------------------------------------------------------

setlocal
REM Este .bat vive em jobs\, mas os caminhos abaixo sao relativos a RAIZ do
REM repo: %~dp0 e a pasta DESTE arquivo (...\jobs\), entao %~dp0.. sobe um nivel.
cd /d "%~dp0.."

echo.
echo   Atualizando as series de mercado (macro_*)...
echo   Log: logs\continuous_^<hoje^>.log
echo.

REM Caminho absoluto: uma tarefa agendada nao herda o PATH da sessao
REM interativa, entao `uv` puro falha com "nao reconhecido" quando roda pelo
REM Agendador e funciona quando voce da dois cliques -- exatamente o tipo de
REM erro que so aparece no agendamento. Aqui usamos o python do proprio venv,
REM que e o que a tarefa usa, para os dois caminhos serem o mesmo.
set PY=%~dp0..\.venv\Scripts\python.exe
if not exist "%PY%" set PY=python

"%PY%" jobs\atualizar_diario.py
set RC=%ERRORLEVEL%

echo.
if "%RC%"=="0" (echo   OK.) else (echo   FALHOU -- codigo %RC%. Veja o log.)
echo.
pause

exit /b %RC%
