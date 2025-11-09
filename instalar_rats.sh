#!/bin/bash
# Script universal para instalar dependencias del sistema RAT
# Úsalo en ambos servidores (controlador y víctima)

set -e

echo "[+] Actualizando sistema..."
sudo apt update
sudo apt upgrade -y

echo "[+] Instalando Python 3 y pip..."
sudo apt install python3 python3-pip -y

echo "[+] Instalando dependencias Python..."
pip3 install --upgrade pip
pip3 install requests psutil

echo "[+] Instalación completada. Puedes ejecutar server.py o agent.py según el rol del servidor."
