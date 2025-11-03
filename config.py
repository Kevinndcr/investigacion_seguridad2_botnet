# Configuración del Sistema RAT
# Archivo de configuración para servidor y agente

# Configuración del Servidor
SERVER_CONFIG = {
    'host': '0.0.0.0',  # Escuchar en todas las interfaces
    'port': 4444,       # Puerto del servidor
    'max_connections': 10,  # Máximo de agentes concurrentes
    'timeout': 30,      # Timeout para comandos (segundos)
}

# Configuración del Agente
AGENT_CONFIG = {
    'server_host': '',  # IP del servidor (configurar al ejecutar)
    'server_port': 4444,
    'retry_attempts': 5,  # Intentos de reconexión
    'retry_delay': 5,     # Segundos entre reintentos
}

# Comandos Permitidos (preaprobados)
ALLOWED_COMMANDS = [
    'PING',      # Verificar conectividad
    'SYSINFO',   # Información del sistema
    'HTTP_TEST', # Prueba de carga HTTP
    'EXIT',      # Desconectar agente
]

# Configuración de HTTP_TEST
HTTP_TEST_CONFIG = {
    'default_requests': 100,
    'max_requests': 10000,
    'timeout': 10,  # Timeout por petición (segundos)
}

# Configuración de Seguridad
SECURITY_CONFIG = {
    'enable_ssl': False,  # Activar SSL/TLS (requiere certificados)
    'cert_file': 'server.crt',
    'key_file': 'server.key',
    'require_auth': False,  # Autenticación con token
    'auth_token': 'your-secret-token-here',
}

# Configuración de Logging
LOGGING_CONFIG = {
    'enable_logging': True,
    'log_file': 'rat_server.log',
    'log_level': 'INFO',  # DEBUG, INFO, WARNING, ERROR
}

# URLs de prueba sugeridas para HTTP_TEST
TEST_URLS = {
    'local_server': 'http://localhost:8000',
    'aws_server': '',  # Configurar con tu servidor AWS
    'test_api': 'https://httpbin.org/get',
}

# Notas de Seguridad
SECURITY_NOTES = """
IMPORTANTE - LEER ANTES DE USAR:

1. Este sistema es SOLO para entornos de práctica controlados
2. NO ejecutar en sistemas de producción
3. Solo usar contra servidores propios con autorización
4. NO implementar ejecución arbitraria de comandos
5. Configurar correctamente Security Groups en AWS
6. NO exponer públicamente sin protección

Para uso académico únicamente.
"""
