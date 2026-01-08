import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Sua chave que já temos
genai.configure(api_key="AIzaSyD5LLNc-oIpzW07MHRnmSze4pRW3bD7JPY")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.json
        qi_atual = data.get('qiAtual', 100)
        
        prompt = f"Gere 12 questões inéditas JSON de múltipla escolha para QI {qi_atual}. Formato: " + '[{"area": "Lógica", "q": "pergunta", "opt": ["a","b","c","d"], "correct": 0}]'
        
        response = model.generate_content(prompt)
        text = response.text.replace('```json', '').replace('```', '').strip()
        return text, 200, {'Content-Type': 'application/json'}
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
