# 📩 InboxAI – Classificador Inteligente de Emails

Este projeto é uma aplicação web que **classifica emails como "Produtivos" ou "Improdutivos"** e **gera respostas automáticas usando Inteligência Artificial**.

A arquitetura é extremamente leve (**Flask + API de Inferência**), permitindo **deploy rápido e gratuito** em plataformas como **Vercel** ou **Render**.

---

## 🛠️ Tecnologias Utilizadas

### Backend
- Python
- Flask
- Gunicorn

### Frontend
- HTML
- CSS
- JavaScript (Fetch API assíncrono)

### Inteligência Artificial
- **Classificação:** `facebook/bart-large-mnli`
- **Geração de Resposta:** `moonshotai/Kimi-K2-Thinking` (endpoint compatível com OpenAI)
- **Plataforma:** Hugging Face Inference API
- **Bibliotecas Python:** `openai`, `requests`, `PyMuPDF`

### Hospedagem
- Vercel (recomendado)
- Render

---

## 🧠 Arquitetura e Decisões Técnicas

Plataformas gratuitas como Vercel e Render possuem **limite reduzido de RAM (~512MB)**, impossibilitando carregar modelos modernos localmente.

➡️ **Solução adotada:**  
Todo o processamento de IA é feito **externamente**, via Hugging Face.

### Fluxo do sistema:

1. O usuário envia o email (texto ou PDF) pelo frontend.
2. O backend Flask recebe o conteúdo.
3. O Flask faz **requisições POST** para a Inference API da Hugging Face.
4. A Hugging Face executa os modelos e retorna o JSON com:
   - Classificação (Produtivo ou Improdutivo)
   - Resposta automática sugerida
5. O Flask envia o resultado ao navegador.

Essa abordagem deixa o app:

✔️ Extremamente leve  
✔️ Escalável  
✔️ Ideal para deploy gratuito

---

## ⚙️ Como Executar Localmente

### 1️⃣ Pré-requisitos

- Python **3.10+**
- Conta gratuita no **Hugging Face**
- Um **API Token** com permissão *"Make calls to Inference Providers"*

---

### 2️⃣ Clonar o Repositório

```sh
git clone https://github.com/murillodmf/email-ai-classifier.git
cd email-ai-classifier
````

---

### 3️⃣ Criar Ambiente Virtual e Instalar Dependências

```sh
# Criar ambiente virtual
python -m venv venv

# Ativar (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Ativar (macOS/Linux)
# source venv/bin/activate

# Instalar bibliotecas
pip install -r requirements.txt
```

---

### 4️⃣ Configurar o Token de API

```sh
# Windows PowerShell
$env:HF_TOKEN = "hf_SEU_TOKEN_AQUI"

# macOS/Linux
export HF_TOKEN="hf_SEU_TOKEN_AQUI"
```

❗ **Sem esse token a aplicação NÃO funciona**

---

### 5️⃣ Executar o Servidor

```sh
python app.py
```

Depois acesse:

➡️ [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

---

## 🚀 Deploy Grátis (Vercel / Render)

O projeto já está preparado com:

✔️ `requirements.txt`
✔️ `vercel.json` *(se necessário)*
✔️ Uso de variáveis de ambiente

---

## 📜 Licença

Este projeto é open-source. Use, modifique e melhore como quiser.

---

## ✨ Autor

**Murillo de Moura Ferraz**
📧 Desenvolvimento de IA aplicada a produtividade
🔗 GitHub: [https://github.com/murillodmf](https://github.com/murillodmf)
