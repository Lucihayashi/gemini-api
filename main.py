import os
from flask import Flask, request, jsonify
import json
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

genai.configure(api_key="AIzaSyD5LLNc-oIpzW07MHRnmSze4pRW3bD7JPY")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/gerar_questoes', methods=['POST'])
def generate():
    try:
        data = request.json
        # Ajustado para aceitar 'qi' ou 'qiAtual'
        qi = data.get('qi') or data.get('qiAtual') or 100
        
        prompt = (
            f"Gere 12 questões de múltipla escolha para nível de QI {qi}. "
            "Responda APENAS o JSON puro, sem explicações ou markdown. "
            "Formato: " + '[{"area": "...", "q": "...", "opt": ["..."], "correct": 0}]'
        )
        
        response = model.generate_content(prompt)
        # Limpa possíveis textos extras da IA
        text = response.text.replace('```json', '').replace('```', '').strip()
        
        # Converte para JSON real antes de enviar
        return jsonify(json.loads(text))
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
