from http.server import BaseHTTPRequestHandler
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Читаем наш дизайн из файла index.html
        try:
            # Теперь файл лежит прямо в той же папке, что и этот скрипт
        template_path = os.path.join(os.path.dirname(__file__), 'index.html')
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Ошибка загрузки интерфейса: {str(e)}".encode('utf-8'))

    def do_POST(self):
        # Здесь остается твоя логика поиска (старый код do_POST)
        # Просто убедись, что do_POST идет следом за do_GET
        pass
