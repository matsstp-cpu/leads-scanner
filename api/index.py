from http.server import BaseHTTPRequestHandler
import os
import json
import urllib.request

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        template_path = os.path.join(os.path.dirname(__file__), 'index.html')
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(content.encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            query = data.get('query', '')
            api_key = os.environ.get("DADATA_API_KEY")
            
            # Запрос к DaData
            url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/party"
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Token {api_key}"
            }
            body = json.dumps({"query": query, "count": 10}).encode('utf-8')
            
            req = urllib.request.Request(url, data=body, headers=headers)
            with urllib.request.urlopen(req) as response:
                dadata_res = json.loads(response.read().decode('utf-8'))

            # ПЕРЕВОДЧИК: превращаем формат DaData в формат твоего интерфейса
            formatted_leads = []
            for item in dadata_res.get('suggestions', []):
                data_info = item.get('data', {})
                formatted_leads.append({
                    "inn": data_info.get('inn', '-'),
                    "name": item.get('value', 'Без названия'),
                    "description": data_info.get('okved', 'ОКВЭД не указан'),
                    "phone": "Контакт скрыт",
                    "email": "Скрыто",
                    "score": 8 # Заглушка рейтинга
                })

            # Отправляем JSON, который ждет твой HTML
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"leads": formatted_leads}).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
