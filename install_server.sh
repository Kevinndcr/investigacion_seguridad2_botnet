#!/bin/bash
# Script de instalación para Ubuntu Server (AWS)
# Sistema RAT - Servidor

echo "================================================"
echo " Sistema RAT - Instalación del Servidor"
echo " Para Ubuntu Server en AWS"
echo "================================================"
echo ""

# Actualizar sistema
echo "[1/5] Actualizando sistema..."
sudo apt update
sudo apt upgrade -y

# Instalar Python 3 y pip
echo "[2/5] Instalando Python 3 y pip..."
sudo apt install python3 python3-pip -y

# Instalar dependencias opcionales
echo "[3/5] Instalando dependencias opcionales..."
pip3 install requests psutil

# Instalar netdata para monitoreo
echo "[4/5] Instalando netdata (opcional)..."
read -p "¿Desea instalar netdata para monitoreo? (s/n): " install_netdata
if [ "$install_netdata" = "s" ] || [ "$install_netdata" = "S" ]; then
    sudo apt install netdata -y
    echo "Netdata instalado. Acceder en: http://tu-ip:19999"
fi

# Configurar firewall
echo "[5/5] Configuración del firewall..."
echo "RECORDATORIO: Configurar AWS Security Group:"
echo "  - Tipo: TCP personalizado"
echo "  - Puerto: 4444"
echo "  - Origen: Tu IP específica (NO 0.0.0.0/0)"
echo ""

# Dar permisos de ejecución
chmod +x server.py

echo ""
echo "================================================"
echo " ✓ Instalación completada"
echo "================================================"
echo ""
echo "Para ejecutar el servidor:"
echo "  python3 server.py"
echo ""
echo "Configuración AWS Security Group:"
echo "  1. Ir a EC2 → Security Groups"
echo "  2. Agregar regla de entrada:"
echo "     - Tipo: TCP personalizado"
echo "     - Puerto: 4444"
echo "     - Origen: Tu IP"
echo ""
