from flask import Flask, request, jsonify, render_template
import fitz
import os
import requests
import time
from openai import OpenAI 

HF_TOKEN = os.environ.get("HF_TOKEN")

API_URL_CLASSIFY = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

KIMI_BASE_URL = "https://router.huggingface.co/v1" 
KIMI_MODEL = "moonshotai/Kimi-K2-Thinking" 

kimi_client = OpenAI(
    base_url=KIMI_BASE_URL,
    api_key=HF_TOKEN 
)

app = Flask(__name__, static_folder='static', template_folder='templates')

def query_api_classify(url, payload):
    """Função para a API de Classificação (padrão)."""
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
    """Renderiza a página inicial."""
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_email():
    """Processa o email (texto ou arquivo) e retorna a classificação/resposta."""
    
    if not HF_TOKEN:
        return jsonify({'error': 'Token da API (HF_TOKEN) não configurado no servidor.'}), 500

    email_text = ""
    api_result_classify = None
    
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

        print("Iniciando chamada de API (Classificação com bart-large)...")
        
        label_produtivo = "E-mail de trabalho que requer uma ação"
        label_improdutivo = "Saudação social ou e-mail sem ação necessária"
        
        class_payload = {
            "inputs": email_text,
            "parameters": {"candidate_labels": [label_produtivo, label_improdutivo]}
        }

        api_result_classify = query_api_classify(API_URL_CLASSIFY, class_payload)
        
        if not api_result_classify or not isinstance(api_result_classify, list) or not api_result_classify[0]:
             raise Exception("Resposta inesperada da API de Classificação (não é uma lista ou está vazia).")
        
        result_dict = api_result_classify[0]
        
        print(f"RESPOSTA DA API (Classificação): {result_dict}") 
        
        if 'label' in result_dict:
            label_recebida = result_dict['label']
            
            if label_recebida == label_produtivo:
                classification = "Produtivo"
            else:
                classification = "Improdutivo"
                
        elif 'error' in result_dict:
            raise Exception(f"Erro da API (Classificação): {result_dict['error']}")
        else:
            raise Exception(f"Resposta inesperada da API (Classificação). Não continha 'label' ou 'error'. Recebido: {str(result_dict)}")
            
        print(f"Resultado Classificação: {classification}")
        
        prompt_para_ia = "" 
        if classification == 'Produtivo':
            prompt_para_ia = f"Gere uma resposta curta e profissional para um email importante com o seguinte conteúdo: '{email_text[:200]}...'\n\nResposta sugerida:"
        else: 
            prompt_para_ia = f"Gere uma resposta curta e amigável para este email social/não-urgente: '{email_text[:200]}...'\n\nResposta sugerida:"
        
        print("Iniciando chamada de API (Geração com Kimi-K2)...")
        
        messages = [
            {"role": "user", "content": prompt_para_ia}
        ]

        try:
            completion = kimi_client.chat.completions.create(
                model=KIMI_MODEL,
                messages=messages
            )
            suggested_response = completion.choices[0].message.content.strip()

        except Exception as gen_error:
            print(f"Erro na API de Geração (Kimi): {gen_error}")
            raise Exception(f"Erro da API (Geração): {str(gen_error)}")

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