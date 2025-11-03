#!/usr/bin/env python3
"""
Script de ejemplo: Servidor web simple para pruebas HTTP_TEST
Ejecutar en un servidor separado para pruebas de carga
"""

from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime

class CustomHandler(SimpleHTTPRequestHandler):
    """Handler personalizado con logging"""
    
    request_count = 0
    
    def do_GET(self):
        """Maneja peticiones GET"""
        CustomHandler.request_count += 1
        
        # Log de petición
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] Request #{CustomHandler.request_count} from {self.client_address[0]}")
        
        # Responder con página simple
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        html = f"""
        <html>
        <head><title>Test Server</title></head>
        <body>
            <h1>Servidor de Prueba RAT</h1>
            <p>Request #{CustomHandler.request_count}</p>
            <p>Timestamp: {timestamp}</p>
            <p>Client: {self.client_address[0]}</p>
        </body>
        </html>
        """
        self.wfile.write(html.encode())
    
    def log_message(self, format, *args):
        """Suprimir logs automáticos (ya tenemos custom logging)"""
        pass


def run_server(port=8000):
    """Ejecuta el servidor"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, CustomHandler)
    
    print(f"""
    ╔════════════════════════════════════════════════════════════╗
    ║  Servidor Web de Prueba - Sistema RAT                     ║
    ║  Para pruebas de carga HTTP_TEST                          ║
    ╚════════════════════════════════════════════════════════════╝
    
    [+] Servidor iniciado en puerto {port}
    [+] Esperando peticiones HTTP...
    [+] Presiona Ctrl+C para detener
    
    Para acceder:
      - Local: http://localhost:{port}
      - Remoto: http://[tu-ip-pública]:{port}
    
    ⚠️  Recordar abrir puerto {port} en Security Group de AWS
    
    """)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n\n[!] Servidor detenido")
        print(f"[*] Total de peticiones recibidas: {CustomHandler.request_count}")
        httpd.shutdown()


if __name__ == "__main__":
    import sys
    
    # Puerto por defecto o especificado
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Puerto inválido. Usando 8000 por defecto.")
    
    run_server(port)
