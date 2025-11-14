from flask import Flask, request, jsonify, render_template
import fitz
import os
import requests
import time

HF_TOKEN = os.environ.get("HF_TOKEN")

API_URL_CLASSIFY = "https://api-inference.huggingface.co/models/valhalla/distilbart-mnli-12-3"
API_URL_GENERATE = "https://api-inference.huggingface.co/models/pierreguillou/gpt2-small-portuguese"

HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

app = Flask(__name__, static_folder='static', template_folder='templates')

def query_api(url, payload):
    response = requests.post(url, headers=HEADERS, json=payload)
    
    if response.status_code == 503:
        wait_time = float(response.json().get('estimated_time', 20.0))
        print(f"Modelo está carregando. Aguardando {wait_time} segundos...")
        time.sleep(wait_time)
        response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code != 200:
        raise Exception(f"Erro na API {response.status_code}: {response.text}")
    
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_email():
    
    if not HF_TOKEN:
        return jsonify({'error': 'Token da API (HF_TOKEN) não configurado no servidor.'}), 500

    email_text = ""
    
    try:
        if 'file_upload' in request.files:
            file = request.files['file_upload']
            if file.filename == '':
                return jsonify({'error': 'Nenhum arquivo selecionado.'}), 400
            
            filename = file.filename
            extensao = os.path.splitext(filename)[1].lower()

            if extensao == '.txt':
                email_text = file.read().decode('utf-8')
            elif extensao == '.pdf':
                doc = fitz.open(stream=file.read(), filetype="pdf")
                for page in doc:
                    email_text += page.get_text()
                doc.close()
            else:
                return jsonify({'error': 'Formato de arquivo não suportado. Use .txt ou .pdf.'}), 400
        elif 'email_text' in request.form:
            email_text = request.form.get('email_text', '')
        if not email_text.strip():
            return jsonify({'error': 'Nenhum texto ou arquivo válido enviado.'}), 400

        
        print("Iniciando chamada de API (Classificação)...")
        class_payload = {
            "inputs": email_text,
            "parameters": {"candidate_labels": ["Produtivo", "Improdutivo"]}
        }
        api_result = query_api(API_URL_CLASSIFY, class_payload)
        classification = api_result['labels'][0]
        print(f"Resultado Classificação: {classification}")

        
        prompt = "" 
        if classification == 'Produtivo':
            prompt = f"Gerar uma resposta curta e profissional para um email importante com o seguinte conteúdo: '{email_text[:200]}...'\n\nResposta sugerida:"
        else: 
            prompt = f"Gerar uma resposta curta e amigável para um email não-urgente (como um agradecimento ou feliz natal).\n\nResposta sugerida:"
        
        print("Iniciando chamada de API (Geração)...")
        gen_payload = {
            "inputs": prompt,
            "parameters": {
                "max_new_tokens": 100,
                "no_repeat_ngram_size": 2
            }
        }
        api_result = query_api(API_URL_GENERATE, gen_payload)
        
        full_text = api_result[0]['generated_text']
        suggested_response = full_text.replace(prompt, "").strip()
        print("Geração concluída.")
        
        if not suggested_response:
             suggested_response = "Não foi possível gerar uma sugestão de resposta."
        
        
        response = {
            'classification': classification,
            'suggested_response': suggested_response
        }
        
        return jsonify(response)

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return jsonify({'error': f'Ocorreu um erro interno no servidor: {e}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')