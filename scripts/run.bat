REM Hide the command prom pt window

@echo off
::auto-reiniciarse en segundo plano y minimizarse
if not "%1" == "h" ( 
    start /min cmd /C "%~dpnx0" h
    exit /b
)

title sempiterno-group-rpa-contabot-conciliacion-bancaria
cd ..
echo Changed to: %cd%

:loop

.\.venv\Scripts\python.exe -m src.contabot_conciliacion_bancaria

:: Esperar una hora antes de la próxima ejecución
timeout /t 60

:: Ir al comienzo del bucle
goto :loop
