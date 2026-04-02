from http.server import BaseHTTPRequestHandler
import os
import json
import urllib.request

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            query = data.get('query', '')
            offset = data.get('offset', 0)
            api_key = os.environ.get("DADATA_API_KEY")
            
            # Используем метод 'findById' или 'suggest' с фильтрами для реестра
            url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/party"
            headers = {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Token {api_key}"
            }
            
            # ФИЛЬТР: Мы просим только активные компании (ACTIVE)
            # и ограничиваем поиск конкретным типом данных
            body = json.dumps({
                "query": query,
                "count": 20,
                "offset": offset,
                "status": ["ACTIVE"],
                "from_bound": {"value": "party"},
                "to_bound": {"value": "party"}
            }).encode('utf-8')
            
            req = urllib.request.Request(url, data=body, headers=headers)
            with urllib.request.urlopen(req) as response:
                res = json.loads(response.read().decode('utf-8'))

            leads = []
            for item in res.get('suggestions', []):
                d = item.get('data', {})
                # Берем только важные для бизнеса поля
                leads.append({
                    "inn": d.get('inn'),
                    "name": item.get('value'),
                    "city": d.get('address', {}).get('data', {}).get('city') or "РФ",
                    "okved": d.get('okved', 'Не указан'),
                    "ogrn": d.get('ogrn', '-')
                })

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"leads": leads}).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
