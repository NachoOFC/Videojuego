@echo off
REM Script para iniciar El Jarl en Windows

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║        ^>^> Iniciando El Jarl - Servidor Web ^<^<          ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado o no está en el PATH
    echo.
    echo Soluciones:
    echo 1. Instala Python desde https://www.python.org/
    echo 2. Marca la opción "Add Python to PATH" durante la instalación
    echo 3. Reinicia PowerShell/CMD después de instalar Python
    echo.
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo.
echo 🚀 Iniciando servidor en http://localhost:8000
echo.
echo Presiona Ctrl+C para detener el servidor
echo.

python server.py

pause
