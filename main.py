import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

genai.configure(api_key="AIzaSyD5LLNc-oIpzW07MHRnmSze4pRW3bD7JPY")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/gerar_questoes', methods=['POST'])
def gerar():
    try:
        data = request.json
        qi = data.get('qi') or 100
        
        prompt = f"Gere 12 questões de múltipla escolha para QI {qi}. Responda APENAS o JSON puro: " + '[{"area": "Lógica", "q": "pergunta", "opt": ["a","b","c","d"], "correct": 0}]'
        
        response = model.generate_content(prompt)
        clean_text = response.text.replace('```json', '').replace('```', '').strip()
        
        return jsonify(json.loads(clean_text))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
