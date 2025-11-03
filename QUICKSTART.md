# Guía Rápida de Inicio - Sistema RAT

## 🚀 Inicio Rápido (5 minutos)

### Paso 1: Configurar Servidor en AWS

```bash
# SSH a tu servidor AWS
ssh -i tu-llave.pem ubuntu@tu-ip-aws

# Subir el archivo server.py
# Ejecutar servidor
python3 server.py
```

**Configuración:**
- Host: `0.0.0.0`
- Puerto: `4444`

**⚠️ NO OLVIDAR: Abrir puerto en AWS Security Group (TCP 4444)**

---

### Paso 2: Ejecutar Agentes

**En Windows:**
```cmd
python agent.py
```

**En Linux/Mac:**
```bash
python3 agent.py
```

**Configuración:**
- IP del servidor: `[tu-ip-pública-aws]`
- Puerto: `4444`

---

### Paso 3: Probar el Sistema

**En el menú del servidor:**

1. Opción `1`: Ver agentes conectados
2. Opción `3`: Obtener info del sistema (SYSINFO)
3. Opción `2`: Hacer PING
4. Opción `4`: Prueba de carga HTTP

---

## 📝 Comandos del Menú

| Opción | Comando | Descripción |
|--------|---------|-------------|
| 1 | Listar agentes | Ver todos los agentes conectados |
| 2 | PING | Hacer ping desde el agente |
| 3 | SYSINFO | Info del sistema del agente |
| 4 | HTTP_TEST | Prueba de carga HTTP |
| 5 | Comando a todos | Enviar comando a todos los agentes |
| 6 | Desconectar | Desconectar un agente |
| 7 | Logs | Ver logs de actividad |
| 8 | Comando personalizado | Ejecutar comando en un agente |
| 9 | Comando personalizado (todos) | Ejecutar comando en todos |
| 10 | Salir | Cerrar servidor |

---

## 💻 Ejemplos de Comandos Personalizados

### Windows:
```cmd
dir                    # Listar archivos
ipconfig              # Configuración de red
whoami                # Usuario actual
tasklist              # Procesos en ejecución
systeminfo            # Info del sistema
```

### Linux/Ubuntu:
```bash
ls -la                # Listar archivos
pwd                   # Directorio actual
df -h                 # Espacio en disco
ps aux                # Procesos
uname -a              # Info del sistema
```

### Mac:
```bash
ls -la                # Listar archivos
sw_vers               # Versión del SO
top -l 1              # Procesos
```

---

## 🎯 Ejemplo de Prueba de Carga

### 1. Crear servidor web simple:

**En otra terminal o servidor AWS:**
```bash
python3 -m http.server 8000
```

### 2. Desde el servidor RAT:

- Seleccionar opción `4`
- Ingresar URL: `http://tu-ip-servidor-web:8000`
- Número de peticiones: `100`

### 3. Monitorear con netdata:

```bash
# Instalar en servidor web
sudo apt install netdata

# Acceder en navegador:
# http://tu-ip-servidor-web:19999
```

---

## ⚠️ Checklist de Seguridad AWS

- [ ] Security Group configurado con puerto 4444
- [ ] Origen del Security Group limitado a tu IP (NO 0.0.0.0/0)
- [ ] Servidor web de prueba en instancia separada
- [ ] Netdata instalado para monitoreo
- [ ] Probado con múltiples agentes simultáneos

---

## 🐛 Problemas Comunes

**"Connection refused"**
- Verificar Security Group en AWS
- Verificar que server.py esté corriendo
- Verificar la IP pública del servidor

**"Module 'requests' not found"**
```bash
pip install requests psutil
```

**"Permission denied"**
```bash
chmod +x server.py agent.py
```

---

## 📊 Para la Demostración en Clase

1. **Mostrar arquitectura** (dibujar en pizarra)
2. **Conectar 3-5 agentes** (PCs, VMs, AWS)
3. **Ejecutar SYSINFO en todos** (Opción 5)
4. **Prueba de carga coordinada** (HTTP_TEST a todos)
5. **Mostrar netdata** con el impacto en recursos
6. **Explicar comandos preaprobados** (seguridad)

---

## 📞 Ayuda Rápida

**Ver IP pública de AWS:**
```bash
curl http://checkip.amazonaws.com
```

**Ver agentes conectados:**
- Opción 1 en el menú del servidor

**Detener todo:**
- En servidor: Opción 8
- Agentes se desconectarán automáticamente

---

**Fecha límite:** 11/11/2025  
**Puntos:** 55 pts (20% nota final)

¡Éxito con el proyecto! 🚀
