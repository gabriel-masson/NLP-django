function initializeChat() {
    const chatForm = document.getElementById('chatForm');
    const searchInput = document.getElementById('searchInput');
    const messagesContainer = document.getElementById('messagesContainer');
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    // Add welcome message if the chat is empty
    if (messagesContainer.children.length === 0) {
        addMessage('Hello! I\'m Valeria. How can I help you today?', false);
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

    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user' : 'bot'} mb-4 p-3`;
        messageDiv.textContent = message;
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    async function sendMessageToAPI(message) {
        try {
            showTypingIndicator();
            
            const response = await fetch('/chat/api/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                },
                body: JSON.stringify({ message: message })
            });

            alert(response.status);
            console.log(response);
            const data = await response.json();
            
            if (data.status === 'success') {
                // Remove typing indicator before showing the response
                hideTypingIndicator();
                addMessage(data.message, false);
            } else {
                console.error('Error from server:', data.message);
                hideTypingIndicator();
                addMessage('Sorry, I encountered an error. Please try again.', false);
            }
        } catch (error) {
            console.error('Error sending message:', error);
            hideTypingIndicator();
            addMessage('Sorry, I\'m having trouble connecting to the server.', false);
        }
    }

    function handleSubmit(e) {
        e.preventDefault();
        const message = searchInput.value.trim();
        if (message) {
            addMessage(message, true);
            searchInput.value = '';
            sendMessageToAPI(message);
        }
        searchInput.focus();
    }

    // Event Listeners
    chatForm.addEventListener('submit', handleSubmit);
    
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
