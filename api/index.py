import os
import json
import requests
from http.server import BaseHTTPRequestHandler

# Наш бесплатный умный фильтр
def analyze_lead_free(company_name, description):
    # Слова-маркеры для тех, кому нужны масштабные переводы
    high_priority = ['it', 'информационн', 'разработка', 'экспорт', 'вэд', 'международн', 'софт', 'программн']
    medium_priority = ['торговля', 'производство', 'логистика']
    
    score = 1
    desc_lower = str(description).lower()
    name_lower = str(company_name).lower()
    
    for word in high_priority:
        if word in desc_lower or word in name_lower:
            score += 3
    for word in medium_priority:
        if word in desc_lower or word in name_lower:
            score += 1
            
    return min(score, 10) # Максимум 10 баллов

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        body = json.loads(post_data)
        query = body.get('query', '')
        dadata_key = os.environ.get("DADATA_API_KEY")

        url = "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/party"
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Token {dadata_key}"
        }
        payload = {"query": query, "count": 15} 

        try:
            response = requests.post(url, headers=headers, json=payload)
            results = response.json().get('suggestions', [])
        except:
            results = []

        leads = []
        for item in results:
            data = item.get('data', {})
            name = item.get('value', 'N/A')
            inn = data.get('inn', 'N/A')
            okved = data.get('okved', '')
            description = f"ОКВЭД: {okved}"
            
            emails = data.get('emails', [])
            phones = data.get('phones', [])
            email_str = emails[0]['value'] if emails else "Нет в базе"
            phone_str = phones[0]['value'] if phones else "Нет в базе"
            
            score = analyze_lead_free(name, description)

            leads.append({
                "inn": inn,
                "name": name,
                "description": description,
                "email": email_str,
                "phone": phone_str,
                "score": score
            })

        leads = sorted(leads, key=lambda x: x['score'], reverse=True)

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"status": "success", "leads": leads}).encode('utf-8'))
