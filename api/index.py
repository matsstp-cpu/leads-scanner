from http.server import BaseHTTPRequestHandler
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # 1. Определяем путь к файлу (он должен лежать в папке api вместе с этим скриптом)
        template_path = os.path.join(os.path.dirname(__file__), 'index.html')
        
        try:
            # 2. Читаем дизайн
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 3. Отправляем ответ браузеру
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
            
        except Exception as e:
            # Если файл не нашелся или не открылся
            self.send_response(500)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            error_message = f"Ошибка загрузки интерфейса: {str(e)}"
            self.wfile.write(error_message.encode('utf-8'))

    def do_POST(self):
        # Сюда нужно будет вставить твой старый код поиска (тот, что с API-ключами)
        # Пока тут заглушка, чтобы сервер не падал
        self.send_response(200)
        self.end_headers()
        self.wfile.write("Поиск пока не настроен".encode('utf-8'))
