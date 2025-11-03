# Ejemplos de Comandos Personalizados - Sistema RAT

## ⚠️ IMPORTANTE
**Los comandos personalizados solo deben usarse en entornos de práctica controlados con autorización explícita.**

---

## 🪟 Windows

### Información del Sistema
```cmd
# Información completa del sistema
systeminfo

# Usuario actual
whoami

# Nombre del equipo
hostname

# Versión de Windows
ver

# Variables de entorno
set
```

### Red y Conectividad
```cmd
# Configuración de red
ipconfig

# Configuración detallada
ipconfig /all

# Tabla de rutas
route print

# Conexiones activas
netstat -an

# Comprobar conectividad
ping google.com -n 4
```

### Archivos y Directorios
```cmd
# Listar archivos
dir

# Listar con detalles
dir /s /b

# Árbol de directorios
tree /F

# Directorio actual
cd

# Contenido de archivo
type archivo.txt
```

### Procesos y Servicios
```cmd
# Lista de procesos
tasklist

# Procesos con detalles
tasklist /v

# Servicios en ejecución
sc query state= all

# Matar un proceso (cuidado)
taskkill /PID 1234 /F
```

### Recursos del Sistema
```cmd
# Espacio en disco
wmic logicaldisk get name,size,freespace

# Información de CPU
wmic cpu get name,numberofcores

# Memoria RAM
wmic memorychip get capacity

# Lista de programas instalados
wmic product get name,version
```

---

## 🐧 Linux / Ubuntu

### Información del Sistema
```bash
# Información del kernel
uname -a

# Distribución
cat /etc/os-release

# Información de hardware
lscpu

# Usuario actual
whoami

# Hostname
hostname

# Uptime del sistema
uptime
```

### Red y Conectividad
```bash
# Configuración de red
ifconfig
# o en sistemas modernos:
ip addr show

# Rutas de red
ip route

# Conexiones activas
netstat -tulpn
# o:
ss -tulpn

# Ping
ping -c 4 google.com

# Puertos abiertos
ss -lntu
```

### Archivos y Directorios
```bash
# Listar archivos
ls -la

# Directorio actual
pwd

# Espacio en disco
df -h

# Uso de directorio
du -sh *

# Buscar archivos
find . -name "*.txt"

# Contenido de archivo
cat archivo.txt

# Primeras líneas
head -n 10 archivo.txt

# Últimas líneas
tail -n 10 archivo.txt
```

### Procesos
```bash
# Procesos en ejecución
ps aux

# Top procesos por CPU
top -b -n 1 | head -20

# Procesos de un usuario
ps -u usuario

# Árbol de procesos
pstree
```

### Recursos del Sistema
```bash
# Memoria RAM
free -h

# CPU info
cat /proc/cpuinfo

# Espacio en disco
df -h

# Uso de memoria por proceso
ps aux --sort=-%mem | head -10

# Información de red
ip link show
```

### Logs y Monitoreo
```bash
# Últimos logins
last -n 10

# Usuarios conectados
who

# Logs del sistema
tail -n 50 /var/log/syslog

# Espacio usado por logs
du -sh /var/log/*
```

---

## 🍎 macOS

### Información del Sistema
```bash
# Versión de macOS
sw_vers

# Información del hardware
system_profiler SPHardwareDataType

# Usuario actual
whoami

# Hostname
hostname

# Uptime
uptime
```

### Red
```bash
# Configuración de red
ifconfig

# Ping
ping -c 4 google.com

# Puertos abiertos
lsof -i -P
```

### Archivos
```bash
# Listar archivos
ls -la

# Espacio en disco
df -h

# Directorio actual
pwd
```

### Procesos
```bash
# Procesos
ps aux

# Top procesos
top -l 1
```

---

## 🎯 Ejemplos de Uso en el Proyecto

### Escenario 1: Inventario de Equipos
```
Opción 9 (todos los agentes):
Comando: whoami && hostname
```
**Resultado:** Obtener lista de usuarios y nombres de equipos conectados

### Escenario 2: Verificar Conectividad
```
Opción 9 (todos los agentes):
Windows: ping google.com -n 2
Linux: ping -c 2 google.com
```
**Resultado:** Verificar que todos los agentes tengan internet

### Escenario 3: Estado de Recursos
```
Opción 9 (todos los agentes):
Windows: wmic logicaldisk get name,freespace,size
Linux: df -h
```
**Resultado:** Verificar espacio disponible en cada equipo

### Escenario 4: Listar Procesos Específicos
```
Opción 8 (agente específico):
Windows: tasklist | findstr python
Linux: ps aux | grep python
```
**Resultado:** Ver procesos Python en ejecución

### Escenario 5: Información de Red
```
Opción 9 (todos los agentes):
Windows: ipconfig | findstr IPv4
Linux: ip addr show | grep inet
```
**Resultado:** Obtener IPs de todos los agentes

---

## ⚠️ Comandos que NO se Recomienda Usar

### ❌ Peligrosos / Destructivos
```bash
# NO USAR - Eliminan archivos
rm -rf /
del /F /S /Q C:\*

# NO USAR - Apagan el sistema
shutdown -h now
shutdown /s /t 0

# NO USAR - Matan procesos críticos
taskkill /F /IM explorer.exe

# NO USAR - Modifican configuración
regedit
```

### ❌ Comandos Interactivos (No funcionan bien)
```bash
# NO USAR - Requieren entrada del usuario
vim
nano
top (sin -b -n 1)
more
less
```

### ❌ Comandos de Larga Duración
```bash
# NO USAR - Timeout de 30s
sleep 60
ping -t
```

---

## 🛡️ Mejores Prácticas

1. **Siempre confirmar** antes de ejecutar en todos los agentes
2. **Probar primero** en un solo agente
3. **Usar comandos simples** que no requieran interacción
4. **Evitar comandos destructivos** (rm, del, format, etc.)
5. **Documentar** los comandos ejecutados
6. **Limitar timeout** a 30 segundos por comando
7. **Solo usar** en equipos de prueba autorizados

---

## 📊 Comandos Útiles para Demostración

### Para mostrar al profesor:
```bash
# 1. Ver info de todos los equipos
whoami && hostname && uname -a  # Linux
whoami & hostname & ver         # Windows

# 2. Listar directorios
ls -la ~    # Linux/Mac
dir C:\     # Windows

# 3. Verificar conectividad
ping -c 2 8.8.8.8      # Linux/Mac
ping 8.8.8.8 -n 2      # Windows

# 4. Ver uso de recursos
free -h && df -h       # Linux
systeminfo | findstr Memory  # Windows
```

---

## 🔍 Troubleshooting

**Problema: Comando no devuelve salida**
- Algunos comandos no generan output
- Revisar código de retorno en la respuesta

**Problema: Timeout**
- Comandos tardan más de 30 segundos
- Usar comandos más específicos o rápidos

**Problema: Error de permisos**
- Algunos comandos requieren admin/root
- Ejecutar agente con permisos elevados (solo en pruebas)

---

## 📚 Recursos Adicionales

- **Windows Commands**: https://ss64.com/nt/
- **Linux Commands**: https://ss64.com/bash/
- **PowerShell**: https://ss64.com/ps/

---

**Recuerda:** Este sistema es solo para fines educativos y de práctica en entornos controlados.
