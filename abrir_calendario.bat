@echo off
REM ---------------------------------------------------------------------------
REM Abre o Calendario de Divulgacoes com os botoes "Atualizar" funcionando.
REM
REM Basta dar dois cliques neste arquivo. Ele sobe o servidor local e abre o
REM navegador na pagina certa (http://127.0.0.1:8765).
REM
REM Deixe esta janela preta ABERTA enquanto usa o calendario -- e ela que roda o
REM ETL quando voce clica num botao. Para encerrar: feche a janela ou Ctrl+C.
REM
REM Abrir o reports/release_calendar.html direto (dois cliques no HTML) continua
REM funcionando, mas ai o botao so COPIA o comando -- o navegador nao deixa uma
REM pagina aberta como arquivo conversar com o servidor. Por isso este atalho.
REM ---------------------------------------------------------------------------

cd /d "%~dp0"

echo.
echo   Subindo o Calendario de Divulgacoes...
echo   (deixe esta janela aberta enquanto usar os botoes)
echo.

uv run python analytics\release_calendar\serve.py

REM Se cair aqui por erro, a janela nao some antes de voce ler a mensagem.
echo.
echo   Servidor encerrado.
pause
