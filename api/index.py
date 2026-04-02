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
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            import json
            import urllib.request
            
            # Получаем запрос от пользователя
            data = json.loads(post_data.decode('utf-8'))
            query = data.get('query', '')
            
            # Берем API-ключ из настроек Vercel
            api_key = os.environ.get("DADATA_API_KEY")
            
            # Настраиваем запрос к DaData
            url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/party"
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Token {api_key}"
            }
            body = json.dumps({"query": query, "count": 10}).encode('utf-8')
            
            req = urllib.request.Request(url, data=body, headers=headers)
            with urllib.request.urlopen(req) as response:
                result = response.read().decode('utf-8')
            
            # Отправляем результат обратно на черную страницу
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(result.encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        self.send_response(200)
        self.end_headers()
        self.wfile.write("Поиск пока не настроен".encode('utf-8'))
