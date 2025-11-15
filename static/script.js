document.addEventListener('DOMContentLoaded', () => {

    const emailForm = document.getElementById('email-form');
    const emailText = document.getElementById('email-text');
    const fileInput = document.getElementById('file-upload');
    const loader = document.getElementById('loader');
    const resultsDiv = document.getElementById('results');
    const classificationResult = document.getElementById('classification-result');
    const responseResult = document.getElementById('response-result');
    const submitButton = document.getElementById('submit-button');

    const clearTextBtn = document.getElementById('clear-text-btn');
    const removeFileBtn = document.getElementById('remove-file-btn');
    const fileDisplayContainer = document.getElementById('file-display-container');
    const fileNameDisplay = document.getElementById('file-name');


    clearTextBtn.addEventListener('click', () => {
        emailText.value = '';
        emailText.disabled = false;
        fileInput.disabled = false; 
    });

    function clearFileInput() {
        fileInput.value = null;
        fileNameDisplay.textContent = '';
        fileDisplayContainer.style.display = 'none';
        emailText.disabled = false;
    }
    
    removeFileBtn.addEventListener('click', clearFileInput);

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            fileNameDisplay.textContent = fileInput.files[0].name;
            fileDisplayContainer.style.display = 'flex';
            emailText.disabled = true;
        } else {
            clearFileInput();
        }
    });
    
    emailText.addEventListener('input', () => {
        if (emailText.value.trim() !== '') {
            clearFileInput();
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
            
            clearFileInput();
            emailText.disabled = false;
        }
    });
});