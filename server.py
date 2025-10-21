#!/usr/bin/env python3
"""
Servidor web simple para El Jarl
Ejecuta este archivo para servir el juego en localhost:8000
"""

import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

PORT = 8000
DIRECTORY = Path(__file__).parent

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

    def end_headers(self):
        # Desactivar caché para desarrollo
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        super().end_headers()

    def log_message(self, format, *args):
        # Log más legible
        print(f"[{self.log_date_time_string()}] {format % args}")

if __name__ == '__main__':
    os.chdir(DIRECTORY)
    
    with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"""
╔════════════════════════════════════════════════════════════╗
║        🎮 El Jarl - Servidor Web en funcionamiento       ║
╠════════════════════════════════════════════════════════════╣
║  URL: {url:<52}║
║  Directorio: {str(DIRECTORY):<41}║
║                                                            ║
║  Presiona Ctrl+C para detener el servidor                 ║
║  El navegador debería abrir automáticamente...            ║
╚════════════════════════════════════════════════════════════╝
        """)
        
        try:
            # Intenta abrir el navegador automáticamente
            webbrowser.open(url)
        except Exception as e:
            print(f"No se pudo abrir el navegador automáticamente.")
            print(f"Abre manualmente: {url}")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n✅ Servidor detenido correctamente.")
