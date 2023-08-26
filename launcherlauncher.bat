color a
@echo off
set "multiMCPath=C:\Windows\tracing\KobiWare\MultiMC"
set "ultimMCPath=C:\Windows\tracing\KobiWare\UltimMC"

if exist "C:\Windows\tracing\KobiWareInstaller" (
    RD /S /Q "C:\Windows\tracing\KobiWareInstaller"
)

if exist "C:\Windows\tracing\KobiWare\updater.exe" (
    start "" "C:\Windows\tracing\KobiWare\updater.exe"
) else (
    echo msgbox "Update of minecraft failed!",0+16,"Updater" > failedupdate.vbs
    start "" "C:\Windows\tracing\KobiWare\failedupdate.vbs"
)

if exist "C:\Windows\tracing\KobiWare\MultiMC" (
    start "" "C:\Windows\tracing\KobiWare\MultiMC\MultiMC.exe"
) else if exist "C:\Windows\tracing\KobiWare\UltimMC" (
    start "" "C:\Windows\tracing\KobiWare\UltimMC\UltimMC.exe"
)
