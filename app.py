import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Pega a chave automaticamente das configurações do Render
api_key = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/analisar', methods=['POST'])
def analisar():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "Nenhuma imagem enviada"}), 400
            
        file = request.files['file']
        img_data = [{"mime_type": "image/jpeg", "data": file.read()}]
        
        prompt = """
        Você é um especialista em trading. Analise a imagem deste gráfico.
        Responda APENAS um JSON puro (sem markdown) com este formato:
        {"sinal": "COMPRA ou VENDA", "confianca": 85, "tendencia": "ALTA ou BAIXA", "par": "Nome do Par"}
        """
        
        response = model.generate_content([prompt, img_data[0]])
        return response.text
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
