document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('pdfFile');
    const statusDiv = document.getElementById('uploadStatus');
    const queryInput = document.getElementById('userQuery');
    const sendBtn = document.getElementById('sendBtn');
    
    if (!fileInput.files[0]) return;
    
    statusDiv.textContent = "Uploading and processing...";
    
    const formData = new FormData();
    formData.append("file", fileInput.files[0]);
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            statusDiv.textContent = "Upload successful! You can now ask questions.";
            queryInput.disabled = false;
            sendBtn.disabled = false;
        } else {
            statusDiv.textContent = "Upload failed.";
        }
    } catch (error) {
        statusDiv.textContent = "Error: " + error.message;
    }
});

document.getElementById('sendBtn').addEventListener('click', sendMessage);
document.getElementById('userQuery').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

async function sendMessage() {
    const queryInput = document.getElementById('userQuery');
    const chatHistory = document.getElementById('chatHistory');
    const query = queryInput.value.trim();
    
    if (!query) return;
    
    // Add user message
    appendMessage(query, 'user-message');
    queryInput.value = "";
    
    // Add loading placeholder
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message ai-message';
    loadingDiv.textContent = "Thinking...";
    chatHistory.appendChild(loadingDiv);
    chatHistory.scrollTop = chatHistory.scrollHeight;
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        });
        
        const data = await response.json();
        chatHistory.removeChild(loadingDiv);
        
        if (response.ok) {
            appendMessage(data.answer, 'ai-message');
        } else {
            appendMessage("Error: " + data.message, 'ai-message');
        }
    } catch (error) {
        chatHistory.removeChild(loadingDiv);
        appendMessage("Error: " + error.message, 'ai-message');
    }
}

function appendMessage(text, className) {
    const chatHistory = document.getElementById('chatHistory');
    const div = document.createElement('div');
    div.className = `message ${className}`;
    div.textContent = text;
    chatHistory.appendChild(div);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}
