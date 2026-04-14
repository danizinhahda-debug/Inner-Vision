import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import json

app = Flask(__name__)
CORS(app)

# Configure sua chave aqui
genai.configure(api_key="COLOQUE_SUA_CHAVE_AQUI")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/analisar', methods=['POST'])
def analisar():
    file = request.files['file']
    img_data = [{"mime_type": "image/jpeg", "data": file.read()}]
    
    prompt = """
    Você é um especialista em trading. Analise a imagem deste gráfico.
    Responda APENAS um JSON puro (sem markdown) com:
    {"sinal": "COMPRA ou VENDA", "confianca": 0-100, "tendencia": "ALTA ou BAIXA", "par": "Nome do Par"}
    """
    
    response = model.generate_content([prompt, img_data[0]])
    return response.text

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
