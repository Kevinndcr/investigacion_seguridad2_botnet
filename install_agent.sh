#!/bin/bash
# Script de instalación para Agentes
# Sistema RAT - Cliente

echo "================================================"
echo " Sistema RAT - Instalación del Agente"
echo "================================================"
echo ""

# Detectar sistema operativo
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Sistema detectado: Linux"
    
    # Instalar Python 3 y pip
    echo "[1/2] Instalando Python 3 y pip..."
    sudo apt update
    sudo apt install python3 python3-pip -y
    
    # Instalar dependencias
    echo "[2/2] Instalando dependencias..."
    pip3 install requests psutil
    
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Sistema detectado: macOS"
    
    # Verificar que Python 3 esté instalado
    if ! command -v python3 &> /dev/null; then
        echo "Python 3 no encontrado. Instalar desde: https://www.python.org/"
        exit 1
    fi
    
    # Instalar dependencias
    echo "Instalando dependencias..."
    pip3 install requests psutil
    
else
    echo "Sistema no compatible con este script de instalación."
    echo "Para Windows, ejecutar manualmente:"
    echo "  pip install requests psutil"
    exit 1
fi

# Dar permisos de ejecución
chmod +x agent.py

echo ""
echo "================================================"
echo " ✓ Instalación completada"
echo "================================================"
echo ""
echo "Para ejecutar el agente:"
echo "  python3 agent.py"
echo ""
echo "Necesitarás la IP pública de tu servidor AWS."
echo ""
