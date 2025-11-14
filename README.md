# Classificador de Emails com IA 🚀

Este projeto é uma aplicação web desenvolvida para o Desafio [Nome da Empresa], que classifica emails como "Produtivos" ou "Improdutivos" e sugere respostas automáticas usando IA.

A aplicação é construída com uma arquitetura leve (Flask + API de Inferência), permitindo que seja hospedada de forma rápida e gratuita em plataformas como Render ou Hugging Face Spaces.

**[Link para a Aplicação na Nuvem]**
(ex: https://email-ai-classifier.onrender.com)

**[Link para o Vídeo de Demonstração]**
(ex: https://www.youtube.com/watch?v=seu-video)

## 🛠️ Tecnologias Utilizadas

* **Backend:** Python, Flask
* **Frontend:** HTML, CSS, JavaScript (com `fetch` assíncrono)
* **Inteligência Artificial:**
    * **Arquitetura:** API de Inferência (sem carregar modelos localmente).
    * **Plataforma de IA:** [Hugging Face Inference API](https://huggingface.co/inference-api)
    * **Classificação:** `valhalla/distilbart-mnli-12-3`
    * **Geração de Resposta:** `pierreguillou/gpt2-small-portuguese`
* **Processamento de Arquivos:** `PyMuPDF` (para .pdf)
* **Hospedagem:** Render (ou Hugging Face Spaces)
* **Servidor de Produção:** `gunicorn`

---

## 🧠 Arquitetura e Decisões Técnicas

Para atender aos requisitos de uso de IA e hospedagem gratuita na nuvem, optei por **não carregar os modelos de IA na memória do servidor**.

Plataformas de hospedagem gratuita (como Render Free Tier) têm limites de RAM muito baixos (ex: 512MB), o que é insuficiente para carregar modelos de linguagem modernos.

A solução foi implementar uma **arquitetura baseada em API**:

1.  O usuário envia o texto/arquivo para o backend Flask.
2.  O backend Flask (Python) **não processa** a IA. Ele simplesmente faz duas chamadas `POST` para a API de Inferência da Hugging Face.
3.  A API da Hugging Face executa os modelos de classificação e geração em seus próprios servidores e retorna o resultado em JSON.
4.  Nosso app Flask recebe esse JSON e o envia para o frontend.

Essa abordagem torna nosso app **extremamente leve** (< 100MB de RAM), rápido e ideal para o deploy gratuito.



---

## ⚙️ Como Executar Localmente

Siga os passos abaixo para rodar o projeto na sua máquina.

### 1. Pré-requisitos

* Python 3.10+
* Uma conta gratuita no [Hugging Face](https://huggingface.co/)
* Um Token de Acesso (API Token) do Hugging Face.

### 2. Clonar o Repositório

```bash
git clone [https://github.com/murillodmf/email-ai-classifier.git](https://github.com/murillodmf/email-ai-classifier.git)
cd email-ai-classifier
```

### 3. Configurar Ambiente Virtual e Dependências

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Ativar (macOS/Linux)
# source venv/bin/activate

# Instalar bibliotecas
pip install -r requirements.txt
```

### 4. Configurar o Token de API

O aplicativo precisa do seu token da Hugging Face para funcionar.

```bash
# Windows PowerShell
$env:HF_TOKEN = "hf_SEU_TOKEN_SECRETO_VAI_AQUI"

# macOS/Linux
# export HF_TOKEN="hf_SEU_TOKEN_SECRETO_VAI_AQUI"
```

### 5. Executar o Servidor

```bash
python app.py
```

Acesse [http://127.0.0.1:5000/](http://127.0.0.1:5000/) no seu navegador.

---

## 🚀 Como Fazer o Deploy (Render.com)

Esta aplicação está pronta para o deploy gratuito no Render.

1.  **Crie uma conta** no [Render](https://render.com/) (use o login do GitHub).
2.  No painel, clique em **New+** > **Web Service**.
3.  Conecte seu repositório do GitHub.
4.  Configure o serviço:
    * **Runtime:** `Python 3`
    * **Build Command:** `pip install -r requirements.txt`
    * **Start Command:** `gunicorn app:app`
    * **Instance Type:** `Free`
5.  Clique em **"Advanced Settings"**.
6.  Vá em **"Add Environment Variable"**:
    * **Key:** `HF_TOKEN`
    * **Value:** `hf_SEU_TOKEN_SECRETO_VAI_AQUI`
7.  Clique em **"Create Web Service"** e aguarde o build.