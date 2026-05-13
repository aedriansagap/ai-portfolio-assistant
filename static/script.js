document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chat-form');
    const queryInput = document.getElementById('query-input');
    const chatContainer = document.getElementById('chat-container');

    function createMessageElement(content, isUser = false) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${isUser ? 'user-msg' : 'system-msg'}`;
        
        const avatar = document.createElement('div');
        avatar.className = `avatar ${isUser ? 'user-avatar' : 'system-avatar'}`;
        avatar.textContent = isUser ? 'U' : 'A'; // 'U' for User, 'A' for Assistant

        const contentDiv = document.createElement('div');
        contentDiv.className = 'msg-content';
        
        if (typeof content === 'string') {
            // Apply Markdown parsing so things like **bold** naturally format
            contentDiv.innerHTML = marked.parse(content);
        } else {
            contentDiv.appendChild(content); // For DOM elements like typing indicator
        }

        msgDiv.appendChild(avatar);
        msgDiv.appendChild(contentDiv);
        return msgDiv;
    }

    function createTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'typing-indicator';
        for(let i=0; i<3; i++) {
            const dot = document.createElement('div');
            dot.className = 'dot';
            indicator.appendChild(dot);
        }
        return indicator;
    }

    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const query = queryInput.value.trim();
        if (!query) return;

        // Add user message
        chatContainer.appendChild(createMessageElement(query, true));
        queryInput.value = '';
        scrollToBottom();

        // Add typing indicator
        const typingIndicator = createTypingIndicator();
        const typingMsg = createMessageElement(typingIndicator, false);
        chatContainer.appendChild(typingMsg);
        scrollToBottom();

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query })
            });

            const data = await response.json();
            
            // Remove typing indicator
            chatContainer.removeChild(typingMsg);

            if (data.error) {
                chatContainer.appendChild(createMessageElement("System Error: " + data.error, false));
            } else {
                chatContainer.appendChild(createMessageElement(data.response, false));
            }
        } catch (err) {
            chatContainer.removeChild(typingMsg);
            chatContainer.appendChild(createMessageElement("Connection Error. Unable to reach AI core.", false));
        }
        
        scrollToBottom();
    });
});
