@echo off
set "multiMCPath=C:\Windows\tracing\KobiWare\MultiMC"
set "ultimMCPath=C:\Windows\tracing\KobiWare\UltimMC"

if exist "%multiMCPath%" (
    start "" "%multiMCPath%\MultiMC.exe"
) else if exist "%ultimMCPath%" (
    start "" "%ultimMCPath%\UltimMC.exe"
)