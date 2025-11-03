# Sistema RAT - Remote Administration Tool
## Proyecto de Investigación - Seguridad de TI II

Sistema cliente-servidor de administración remota para entornos de práctica controlados.

---

## 📋 Descripción del Proyecto

Este sistema permite administrar remotamente múltiples equipos de prueba desde un servidor central mediante conexiones reversas (reverse shell controlado). Desarrollado específicamente para el curso de Seguridad de TI II.

### Componentes:

1. **Servidor** (`server.py`) - Ejecutar en Ubuntu Server (AWS)
2. **Agente** (`agent.py`) - Ejecutar en equipos de prueba

---

## 🚀 Instalación

### Requisitos del Sistema

**Servidor (Ubuntu Server en AWS):**
```bash
# Python 3.6 o superior
python3 --version

# Instalar dependencias (opcional, para métricas)
sudo apt update
sudo apt install python3-pip netdata -y
```

**Agente (Equipos de prueba):**
```bash
# Python 3.6 o superior
# Para funcionalidad completa, instalar:
pip install requests psutil
```

---

## 📖 Uso del Sistema

### 1. Configurar el Servidor en AWS

**En tu instancia de Ubuntu Server en AWS:**

```bash
# 1. Conectar por SSH
ssh -i tu-llave.pem ubuntu@tu-ip-aws

# 2. Crear directorio del proyecto
mkdir -p ~/rat-system
cd ~/rat-system

# 3. Subir el archivo server.py (usar scp o git)
# Ejemplo con scp desde tu PC:
# scp -i tu-llave.pem server.py ubuntu@tu-ip-aws:~/rat-system/

# 4. Dar permisos de ejecución
chmod +x server.py

# 5. Ejecutar el servidor
python3 server.py
```

**Configuración inicial:**
- Host: `0.0.0.0` (para escuchar en todas las interfaces)
- Puerto: `4444` (o el que prefieras)

**⚠️ IMPORTANTE: Configurar Security Group en AWS**
```
Regla de entrada personalizada:
- Tipo: TCP personalizado
- Puerto: 4444
- Origen: Tu IP o rango específico (NO usar 0.0.0.0/0 en producción)
```

---

### 2. Ejecutar Agentes en Equipos de Prueba

**En cada equipo de prueba (Windows, Linux, Mac):**

```bash
# 1. Navegar al directorio
cd ruta/al/proyecto

# 2. Instalar dependencias opcionales
pip install requests psutil

# 3. Ejecutar el agente
python agent.py

# O en Linux/Mac:
python3 agent.py
```

**Cuando se ejecute, ingresar:**
- IP del servidor: `tu-ip-aws` (la IP pública de tu instancia AWS)
- Puerto: `4444` (el mismo configurado en el servidor)

---

## 🎮 Menú del Servidor

Una vez que el servidor esté ejecutándose, verás este menú:

```
==============================================================
 Sistema RAT - Administración Remota (Entorno de Práctica)
==============================================================
 1. Listar agentes conectados
 2. Enviar PING a un agente
 3. Obtener SYSINFO de un agente
 4. Ejecutar HTTP_TEST (prueba de carga)
 5. Enviar comando a TODOS los agentes
 6. Desconectar un agente
 7. Ver logs de actividad
 8. Ejecutar comando personalizado (un agente)
 9. Ejecutar comando personalizado (TODOS)
 10. Salir y cerrar servidor
==============================================================
```

---

## 📝 Comandos Disponibles

### PING
Verifica conectividad de red desde el agente.
```
Uso: Opción 2 del menú
Parámetros: IP o hostname (default: google.com)
Ejemplo: ping google.com, ping 8.8.8.8
```

### SYSINFO
Obtiene información detallada del sistema del agente.
```
Uso: Opción 3 del menú
Información: OS, CPU, memoria, disco, arquitectura
```

### HTTP_TEST
Ejecuta prueba de carga HTTP contra un servidor web.
```
Uso: Opción 4 del menú
Parámetros:
  - URL del servidor de prueba
  - Número de peticiones (default: 100)
  
Ejemplo de uso para el proyecto:
  - Crear un servidor web simple en otra instancia AWS
  - Usar HTTP_TEST para enviar múltiples peticiones
  - Monitorear con netdata el uso de recursos
```

### CUSTOM (Comando Personalizado)
Ejecuta comandos del sistema operativo en el agente.
```
Uso: Opción 8 (un agente) u Opción 9 (todos)
⚠️ ADVERTENCIA: Solo usar en entornos controlados
Ejemplos:
  - Windows: dir, ipconfig, whoami, tasklist
  - Linux: ls -la, pwd, df -h, ps aux
  - Mac: ls -la, sw_vers, top -l 1
```

### EXIT
Desconecta un agente específico.

---

## 🧪 Demostración para el Proyecto

### Escenario de Prueba:

1. **Servidor de Administración** (AWS Ubuntu Server #1)
   - Ejecutar `server.py`
   - Puerto 4444 abierto

2. **Servidor Web de Prueba** (AWS Ubuntu Server #2)
   - Instalar servidor web simple:
     ```bash
     # Opción 1: Python simple HTTP server
     python3 -m http.server 8000
     
     # Opción 2: Nginx
     sudo apt install nginx
     ```
   - Instalar netdata para monitorear:
     ```bash
     sudo apt install netdata
     # Acceder en: http://tu-ip:19999
     ```

3. **Agentes** (3-5 equipos de prueba)
   - Ejecutar `agent.py` en múltiples máquinas:
     - PCs de laboratorio
     - Máquinas virtuales (VirtualBox, VMware)
     - Otros servidores AWS (t2.micro gratis)

4. **Prueba de Carga**
   - Desde el servidor de administración, seleccionar opción 4
   - Enviar comando HTTP_TEST a todos los agentes
   - URL: `http://ip-servidor-web:8000`
   - Peticiones: 100-1000
   - Monitorear en netdata el impacto

---

## 📊 Monitoreo con Netdata

**Instalar en el servidor web de prueba:**
```bash
sudo apt install netdata

# Permitir acceso externo (solo para pruebas)
sudo nano /etc/netdata/netdata.conf
# Cambiar: bind to = 0.0.0.0

sudo systemctl restart netdata
```

Acceder: `http://tu-ip-servidor-web:19999`

**Métricas importantes:**
- CPU usage
- Network traffic
- HTTP requests
- Memory usage

---

## 🔒 Consideraciones de Seguridad

⚠️ **IMPORTANTE - Solo para entornos de práctica:**

1. **NO ejecutar en sistemas de producción**
2. **NO dar acceso público** (configurar Security Groups correctamente)
3. **Solo comandos preaprobados** (PING, SYSINFO, HTTP_TEST, EXIT)
4. **Usar solo contra tus propios servidores** con autorización explícita
5. **NO implementar ejecución arbitraria de comandos**

### Mejoras de Seguridad (opcional para proyecto avanzado):
- Agregar autenticación con tokens
- Implementar SSL/TLS con certificados
- Logging de todas las acciones
- Rate limiting en comandos
- Whitelist de IPs permitidas

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────┐
│  Servidor de Administración (AWS Ubuntu)    │
│  - server.py escuchando en puerto 4444      │
│  - Menú interactivo para control            │
│  - Threading para múltiples conexiones      │
└──────────────┬──────────────────────────────┘
               │
               │ Conexiones reversas
               │
     ┌─────────┼─────────┬──────────┐
     │         │         │          │
┌────▼───┐ ┌──▼────┐ ┌──▼────┐ ┌──▼────┐
│Agente 1│ │Agente2│ │Agente3│ │Agente4│
│ PC Lab │ │  VM   │ │  AWS  │ │ Local │
└────┬───┘ └───┬───┘ └───┬───┘ └───┬───┘
     │         │         │         │
     └─────────┴─────────┴─────────┘
               │
      Ejecutan HTTP_TEST contra
               │
     ┌─────────▼──────────────────┐
     │ Servidor Web (AWS Ubuntu)  │
     │ - HTTP Server (nginx/python)│
     │ - Netdata monitoring        │
     └────────────────────────────┘
```

---

## 📝 Ejemplo de Sesión

```bash
# Terminal 1 - Servidor
ubuntu@aws-server:~/rat-system$ python3 server.py

Host (Enter para 0.0.0.0): 
Puerto (Enter para 4444): 

[+] Servidor iniciado en 0.0.0.0:4444
[+] Esperando conexiones de agentes...

[+] Nuevo agente conectado: ID=1 | 192.168.1.100:52341
    Sistema: Windows | Hostname: PC-LAB-01

[+] Nuevo agente conectado: ID=2 | 10.0.1.50:45123
    Sistema: Linux | Hostname: vm-ubuntu

# Terminal 2 - Agente 1
C:\> python agent.py

IP del servidor: 54.123.45.67
Puerto del servidor (Enter para 4444): 

[*] Intentando conectar a 54.123.45.67:4444 (intento 1/5)...
[+] Conectado exitosamente al servidor
[+] Agente activo. Esperando comandos del servidor...

[*] Comando recibido: SYSINFO
```

---

## 🎯 Cumplimiento de Requisitos del Proyecto

### ✅ Requisito 1 (20 pts): Servidor con menú
- Menú interactivo completo
- Administración de múltiples conexiones concurrentes
- Pruebas de carga contra servidor web controlado
- Registro de métricas

### ✅ Requisito 2 (20 pts): Agente con conexión segura
- Conexión reversa automática
- Permanece a la espera de instrucciones
- Manejo de reconexión

### ✅ Requisito 3 (15 pts): Comandos preaprobados
- PING: Verificación de conectividad
- SYSINFO: Información del sistema
- HTTP_TEST: Prueba de carga
- EXIT: Desconexión controlada
- Solo comandos seguros y predefinidos

---

## 🐛 Troubleshooting

**Problema: Agente no se conecta**
```bash
# Verificar que el puerto esté abierto en AWS Security Group
# Verificar que el servidor esté ejecutándose
# Verificar la IP pública de AWS (puede cambiar si se reinicia)
```

**Problema: HTTP_TEST falla**
```bash
# Instalar requests en el agente:
pip install requests

# Verificar que el servidor web esté corriendo
# Verificar que el puerto esté abierto
```

**Problema: SYSINFO limitado**
```bash
# Instalar psutil para información completa:
pip install psutil
```

---

## 📚 Recursos Adicionales

- **Netdata**: https://www.netdata.cloud/
- **AWS Security Groups**: https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html
- **Python Socket Programming**: https://docs.python.org/3/library/socket.html

---

## 👥 Equipo de Desarrollo

Proyecto de investigación - Seguridad de TI II
Universidad: IIIC 2025
Profesor: M.Sc. Roberto Escobar Agüero

---

## ⚖️ Disclaimer Legal

Este software es exclusivamente para fines educativos y de investigación en entornos controlados. El uso indebido de esta herramienta puede ser ilegal. Los autores no se hacen responsables del mal uso de este software.

**Usar únicamente:**
- En equipos propios
- Con autorización explícita
- En entornos de laboratorio controlados
- Para propósitos educativos

---

## 📞 Soporte

Para preguntas sobre el proyecto, consultar con el profesor o compañeros de clase.

**Fecha de entrega:** 11/11/2025
**Puntuación:** 55 pts (20% de la nota final)

---

¡Buena suerte con el proyecto! 🚀
