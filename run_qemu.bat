@echo off
setlocal enabledelayedexpansion
title SynapseOS - Demarrage QEMU

echo ====================================================================
echo  SynapseOS - Lanceur de Machine Virtuelle QEMU Windows 11
echo ====================================================================
echo.

set "SCRIPT_DIR=%~dp0"
set "LITE_ISO=%SCRIPT_DIR%iso\SynapseOS-Lite-x86_64.iso"
set "FULL_ISO=%SCRIPT_DIR%output\SynapseOS-Debian12-Potato-x86_64.iso"

set "TARGET_ISO="
set "RAM="

REM Verification de la presence de l ISO Full ou Lite
if exist "%FULL_ISO%" (
    set "TARGET_ISO=%FULL_ISO%"
    set "RAM=4096"
    echo [*] Image detectee : Full LLM ISO - 4096 Mo RAM
    goto iso_found
)

if exist "%LITE_ISO%" (
    set "TARGET_ISO=%LITE_ISO%"
    set "RAM=2048"
    echo [*] Image detectee : Lite ISO - 2048 Mo RAM
    goto iso_found
)

echo [ERREUR] Aucune image ISO trouvee !
echo Verifiez que le fichier iso\SynapseOS-Lite-x86_64.iso existe bien.
echo.
pause
exit /b 1

:iso_found
echo [*] Fichier ISO : !TARGET_ISO!
echo.

REM Detection de QEMU Windows natif
set "QEMU_EXE="
if exist "C:\Users\djiby\qemu\qemu-system-x86_64.exe" (
    set "QEMU_EXE=C:\Users\djiby\qemu\qemu-system-x86_64.exe"
) else (
    if exist "C:\Program Files\qemu\qemu-system-x86_64.exe" (
        set "QEMU_EXE=C:\Program Files\qemu\qemu-system-x86_64.exe"
    )
)

if not defined QEMU_EXE (
    where qemu-system-x86_64.exe >nul 2>&1
    if not errorlevel 1 (
        for /f "delims=" %%i in ('where qemu-system-x86_64.exe') do set "QEMU_EXE=%%i"
    )
)

if defined QEMU_EXE (
    echo [*] QEMU Windows natif detecte : !QEMU_EXE!
    echo [*] Lancement de SynapseOS avec acceleration materielle...
    echo.
    echo --------------------------------------------------------------------
    echo  Astuce QEMU : Appuyez sur Ctrl + Alt + G pour liberer la souris.
    echo --------------------------------------------------------------------
    echo.
    start "SynapseOS VM" "!QEMU_EXE!" -accel whpx -accel tcg -m !RAM! -smp 2 -cdrom "!TARGET_ISO!" -vga std -net nic,model=virtio -net user -boot d
    echo [OK] Machine virtuelle demarree dans sa fenetre graphique !
) else (
    echo [*] QEMU Windows natif non trouve, bascule sur WSL2...
    wsl bash -c "cd /mnt/c/Users/djiby/.gemini/antigravity/scratch/SynapseOS; chmod +x scripts/boot_qemu.sh; ./scripts/boot_qemu.sh"
)

echo.
echo Cette fenetre d information peut etre fermee.
echo.
pause
