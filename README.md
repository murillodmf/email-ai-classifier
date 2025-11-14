# Classificador de Emails com IA 🚀

Este projeto é uma aplicação web desenvolvida para o Desafio da [Nome da Empresa], que classifica emails como "Produtivos" ou "Improdutivos" e sugere respostas automáticas usando IA.

**[Link para a Aplicação na Nuvem]**
(ex: https://meu-app-incrivel.onrender.com)

**[Link para o Vídeo de Demonstração]**
(ex: https://www.youtube.com/watch?v=seu-video)

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python, Flask
* **Frontend:** HTML, CSS, JavaScript
* **Inteligência Artificial:**
    * Biblioteca `transformers` (Hugging Face)
    * **Classificação:** `valhalla/distilbart-mnli-12-3` (Zero-Shot Classification)
    * **Geração de Resposta:** `pierreguillou/gpt2-small-portuguese` (Text Generation)
* **Processamento de Arquivos:** `PyMuPDF` (para .pdf)
* **Deploy (Exemplo):** Render / Vercel / Heroku

## ⚙️ Como Executar Localmente

Siga os passos abaixo para rodar o projeto na sua máquina.

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd seu-repositorio
    ```

2.  **Crie e ative um ambiente virtual (Recomendado):**
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    
    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute o servidor Flask:**
    ```bash
    python app.py
    ```
    *O NLTK pode precisar baixar alguns pacotes na primeira execução.*

5.  **Acesse no seu navegador:**
    Abra [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## 🧠 Decisões Técnicas

*(Esta seção é ótima para o critério "Autonomia e Resolução de Problemas")*

* **Modelos de IA:** Escolhi modelos da Hugging Face por serem open-source e fáceis de integrar com a biblioteca `pipeline`. O `distilbart-mnli` é leve e eficaz para classificação zero-shot.
* **Processamento de NLP:** Embora o desafio mencione stemming/stopwords, optei por *não aplicar* esse pré-processamento no texto enviado aos modelos Transformer, pois eles são treinados com sentenças completas e perdem performance com essa limpeza (a função `preprocess_text` está no código para demonstrar conhecimento da técnica).
* **Frontend:** Utilizei `FormData` e `fetch` em JavaScript para criar uma experiência de usuário assíncrona (sem recarregar a página) que aceita tanto texto quanto upload de arquivos.