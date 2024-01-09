const searchInput = document.getElementById('search-input');
const searchButton = document.getElementById('search-button');
const contextArea = document.getElementById('context-area');
const micButton = document.getElementById('microphone-button');
const recognition = new webkitSpeechRecognition();

searchButton.addEventListener('click', handleUserInput);
micButton.addEventListener('click', startSpeechRecognition);

recognition.onresult = function (event) {
    const result = event.results[0][0].transcript;
    searchInput.value = result;
    handleUserInput();
};

recognition.onerror = function (event) {
    console.error('Speech recognition error:', event.error);
};

recognition.onend = function () {
    alert('Speech recognition completed!');
};

function startSpeechRecognition() {
    recognition.start();
}

function handleUserInput() {
    const userMessage = searchInput.value.trim();
    if (userMessage !== '') {
        appendMessage('user', userMessage);
        searchInput.value = '';
        const botResponse = simulateBotResponse(userMessage);
        appendMessage('bot', botResponse);
    }
}

function appendMessage(sender, message) {
    const messageElement = document.createElement('div');
    messageElement.className = sender === 'user' ? 'user-message' : 'bot-message';
    messageElement.textContent = message;
    contextArea.appendChild(messageElement);
    contextArea.scrollTop = contextArea.scrollHeight;
}

function simulateBotResponse(userMessage) {
    const language = document.getElementById('language').value;
    // Example translations
    const translations = {
        'english': 'It shall come into force on...',
        'Hindi': 'yah is din se laagoo hoga...',
        'Tamil': 'Itu amalukku varum...',
        'Marati': 'te lagu hoila...',
        'Telugu': 'Idhi pravesindhipotundhi...',
        'Bengali': 'Eta karyakara habe...'
        // Add more translations as needed
    };
    return translations[language];
}