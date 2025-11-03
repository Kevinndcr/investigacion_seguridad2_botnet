# Instalación para Windows
# Sistema RAT - Agente/Cliente

Write-Host "================================================" -ForegroundColor Cyan
Write-Host " Sistema RAT - Instalación del Agente (Windows)" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar Python
Write-Host "[1/2] Verificando Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1

if ($LASTEXITCODE -eq 0) {
    Write-Host "Python encontrado: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "Python no encontrado." -ForegroundColor Red
    Write-Host "Descargar desde: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "IMPORTANTE: Marcar 'Add Python to PATH' durante la instalación" -ForegroundColor Yellow
    exit 1
}

# Instalar dependencias
Write-Host ""
Write-Host "[2/2] Instalando dependencias..." -ForegroundColor Yellow
pip install requests psutil

if ($LASTEXITCODE -eq 0) {
    Write-Host "Dependencias instaladas correctamente" -ForegroundColor Green
} else {
    Write-Host "Error instalando dependencias" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host " Instalación completada" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Para ejecutar el agente:" -ForegroundColor Yellow
Write-Host "  python agent.py" -ForegroundColor White
Write-Host ""
Write-Host "Necesitarás la IP pública de tu servidor AWS." -ForegroundColor Yellow
Write-Host ""

pause
