document.addEventListener('DOMContentLoaded', () => {

    const emailForm = document.getElementById('email-form');
    const emailText = document.getElementById('email-text');
    const fileInput = document.getElementById('file-upload');
    const fileNameDisplay = document.getElementById('file-name');
    const loader = document.getElementById('loader');
    const resultsDiv = document.getElementById('results');
    const classificationResult = document.getElementById('classification-result');
    const responseResult = document.getElementById('response-result');
    const submitButton = document.getElementById('submit-button');

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            fileNameDisplay.textContent = fileInput.files[0].name;
            emailText.disabled = true;
        } else {
            fileNameDisplay.textContent = '';
            emailText.disabled = false;
        }
    });
    
    emailText.addEventListener('input', () => {
        if (emailText.value.trim() !== '') {
            fileInput.value = null;
            fileNameDisplay.textContent = '';
        }
        if (fileInput.files.length > 0) {
            emailText.disabled = true;
        }
    });

    emailForm.addEventListener('submit', async function(event) {
        event.preventDefault();

        const formData = new FormData();
        const file = fileInput.files[0];
        const text = emailText.value;

        if (file) {
            formData.append('file_upload', file);
        } else if (text.trim() !== '') {
            formData.append('email_text', text);
        } else {
            alert('Por favor, cole um texto ou envie um arquivo .txt ou .pdf.');
            return;
        }

        loader.style.display = 'block';
        resultsDiv.style.display = 'none';
        submitButton.disabled = true;
        submitButton.textContent = 'Analisando...';

        try {
            const response = await fetch('/process', {
                method: 'POST',
                body: formData 
            });

            const data = await response.json();

            if (response.ok) {
                classificationResult.textContent = data.classification;
                
                classificationResult.className = 'badge';
                if (data.classification === 'Produtivo') {
                    classificationResult.classList.add('produtivo');
                } else {
                    classificationResult.classList.add('improdutivo');
                }
                
                responseResult.textContent = data.suggested_response;
                resultsDiv.style.display = 'block';
            } else {
                alert('Erro: ' + data.error);
            }
        } catch (error) {
            alert('Ocorreu um erro de conexão: ' + error.message);
        } finally {
            loader.style.display = 'none';
            submitButton.disabled = false;
            submitButton.textContent = 'Analisar Email';
        }
    });
});