function initializeChat() {
    const searchInput = document.getElementById('searchInput');
    const messagesContainer = document.getElementById('messagesContainer');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const voiceButton = document.getElementById('voiceButton');
    const speakerButton = document.getElementById('speakerButton');
    const chatForm = document.getElementById('chatForm');
    let audioContext = null;
    
    // Initialize audio context on user interaction
    function initAudioContext() {
        if (!audioContext) {
            try {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
                console.log('AudioContext created');
                // Resume the audio context to ensure it's in the 'running' state
                if (audioContext.state === 'suspended') {
                    audioContext.resume().then(() => {
                        console.log('AudioContext resumed successfully');
                    });
                }
                return audioContext;
            } catch (error) {
                console.error('Error initializing AudioContext:', error);
                return null;
            }
        }
        return audioContext;
    }
    
    // Speech recognition setup
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition = null;
    let isListening = false;
    
    // Initialize speech recognition if supported
    if (SpeechRecognition) {
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'pt-BR';
        
        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            searchInput.value = transcript;
            // Auto-submit the form if there's text
            if (transcript.trim()) {
                chatForm.dispatchEvent(new Event('submit'));
            }
        };
        
        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            voiceButton.classList.remove('listening');
            isListening = false;
        };
        
        recognition.onend = () => {
            voiceButton.classList.remove('listening');
            isListening = false;
        };
    }
    
    // Toggle voice recognition
    function toggleVoiceRecognition() {
        if (!recognition) {
            console.warn('Speech recognition not supported in this browser');
            return;
        }
        
        if (isListening) {
            recognition.stop();
        } else {
            try {
                recognition.start();
                voiceButton.classList.add('listening');
                isListening = true;
                
                // Initialize audio context if not already done
                initAudioContext();
            } catch (error) {
                console.error('Error starting speech recognition:', error);
            }
        }
    }
    
    // Add welcome message if the chat is empty
    if (messagesContainer.children.length === 0) {
        const welcomeMessage = 'Olá, eu sou a Valéria. Como posso ajudar você hoje?';
        addMessage(welcomeMessage, false);
        
        // Auto-read the welcome message if speaker is enabled
        if (speakerButton && speakerButton.classList.contains('active')) {
            sendChatRequest('', true); // Empty message with audio response
        }
    }

    function showTypingIndicator() {
        // Remove any existing typing indicators
        const existingTyping = document.getElementById('typingIndicator');
        if (existingTyping) {
            existingTyping.remove();
        }
        
        // Create and show typing indicator
        const typingDiv = document.createElement('div');
        typingDiv.id = 'typingIndicator';
        typingDiv.className = 'message bot mb-4 p-3 inline-block';
        typingDiv.innerHTML = `
            <div class="flex space-x-1 items-center">
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
            </div>
        `;
        
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function hideTypingIndicator() {
        const typingIndicator = document.getElementById('typingIndicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    function addMessage(message, isUser = false, audioData = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'bot'} mb-4 p-3`;
        
        // Create message content container
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        contentDiv.textContent = message;
        
        messageDiv.appendChild(contentDiv);
        
        // Add speaker button for bot messages with audio support
        if (!isUser && audioData) {
            const audioButton = document.createElement('button');
            audioButton.className = 'speaker-button';
            audioButton.innerHTML = '🔊';
            audioButton.title = 'Ouvir mensagem';
            audioButton.onclick = () => playAudio(audioData);
            messageDiv.appendChild(audioButton);
        }
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // Play audio from base64 data
    function playAudio(base64Data) {
        return new Promise((resolve, reject) => {
            try {
                if (!audioContext) {
                    initAudioContext();
                }
                
                // Convert base64 to ArrayBuffer
                const binaryString = atob(base64Data);
                const bytes = new Uint8Array(binaryString.length);
                for (let i = 0; i < binaryString.length; i++) {
                    bytes[i] = binaryString.charCodeAt(i);
                }
                
                audioContext.decodeAudioData(bytes.buffer)
                    .then(decodedData => {
                        const source = audioContext.createBufferSource();
                        source.buffer = decodedData;
                        source.connect(audioContext.destination);
                        source.start(0);
                        
                        source.onended = () => {
                            resolve();
                        };
                    })
                    .catch(error => {
                        console.error('Error decoding audio:', error);
                        reject(error);
                    });
            } catch (error) {
                console.error('Error in playAudio:', error);
                reject(error);
            }
        });
    }
    
    // Send chat request to server
    function sendChatRequest(message, preferAudio = false) {
        showTypingIndicator();
        
        // Initialize audio context on first interaction if needed
        if (preferAudio && !audioContext) {
            initAudioContext();
        }
        
        fetch('/chat/api/chat/',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                message: message,
                response_type: preferAudio ? 'audio' : 'text'
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(async data => {
            hideTypingIndicator();
            
            if (data.status === 'success') {
                // Add bot response to chat
                const messageElement = addMessage(data.message, false, data.audio || null);
                
                // If we have audio data and audio is preferred, play it
                if (data.audio && preferAudio) {
                    try {
                        await playAudio(data.audio);
                    } catch (error) {
                        console.error('Error playing audio:', error);
                    }
                }
                return messageElement;
            } else {
                console.error('Server error:', data.message);
                addMessage('Desculpe, ocorreu um erro ao processar sua mensagem.', false);
            }
        })
        .catch(error => {
            console.error('Fetch error:', error);
            hideTypingIndicator();
            addMessage('Desculpe, ocorreu um erro na comunicação com o servidor.', false);
        });
    }

    // Toggle speaker mode
    if (speakerButton) {
        speakerButton.addEventListener('click', function() {
            this.classList.toggle('active');
            initAudioContext(); // Initialize audio context on first click
        });
    }

    // Handle form submission
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        const message = searchInput.value.trim();
        
        if (message) {
            // Add user message to chat
            addMessage(message, true);
            
            // Clear input
            searchInput.value = '';
            
            // Send message to server with preferred response type
            const preferAudio = speakerButton && speakerButton.classList.contains('active');
            sendChatRequest(message, preferAudio);
        }
        searchInput.focus();
    }

    // Event Listeners
    chatForm.addEventListener('submit', handleSubmit);
    voiceButton.addEventListener('click', toggleVoiceRecognition);
    
    // Auto-resize textarea
    searchInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });
    
    // Focus the input field when the page loads
    searchInput.focus();
    
    // Handle click outside to close any open menus
    document.addEventListener('click', function(e) {
        if (!e.target.closest('#chatForm') && !e.target.closest('.message')) {
            searchInput.focus();
        }
    });
}

// Initialize chat when DOM is fully loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeChat);
} else {
    initializeChat();
}