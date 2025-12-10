// frontend/assets/js/chat.js

// ✅ CORRECT: This points to YOUR Django server. No key needed here.
const CHAT_API_URL = '/api/chat/';

document.addEventListener('DOMContentLoaded', () => {
    const sendBtn = document.getElementById('send-btn');
    const chatInput = document.getElementById('chat-message');
    const chatForm = document.getElementById('chat-form');

    // Function to handle sending
    async function sendMessage(e) {
        if (e) e.preventDefault(); 
        
        const text = chatInput.value.trim();
        if (!text) return;

        // 1. Show User Text
        addBubble(text, 'user');
        chatInput.value = ''; 

        // 2. Show "Typing..."
        const loadingId = addBubble("Typing...", 'bot', true);

        // ✅ GET USER TOKEN (This is the only "Key" the frontend needs)
        const token = localStorage.getItem('mahika_jwt_token'); 

        try {
            const response = await fetch(CHAT_API_URL, {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    // If you are logged in, this sends your ID securely:
                    'Authorization': token ? `Bearer ${token}` : '' 
                },
                body: JSON.stringify({
                    message: text,
                    // ✅ READ THE ID FROM STORAGE
                    char_id: localStorage.getItem('selected_char_id') || 1
                })
            });

            removeBubble(loadingId);

            if (response.ok) {
                const data = await response.json();
                // 3. Show Real AI Reply
                addBubble(data.bot_reply.text, 'bot');
                
                // 4. Handle Alerts
                if(data.alert_triggered) {
                    alert("⚠️ SAFETY ALERT TRIGGERED");
                    document.body.style.border = "5px solid red";
                }
            } else {
                addBubble("Server Error: I can't reply right now.", 'bot');
            }
        } catch (error) {
            removeBubble(loadingId);
            addBubble("Network Error: Check your connection.", 'bot');
            console.error(error);
        }
    }

    // Attach Listeners
    if(sendBtn) sendBtn.addEventListener('click', sendMessage);
    if(chatForm) chatForm.addEventListener('submit', sendMessage);
});

// UI Helpers
function addBubble(text, sender, isTemp=false) {
    const chatWindow = document.getElementById('chat-window');
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', sender);
    if (isTemp) msgDiv.id = 'temp-loading';
    
    const bubble = document.createElement('div');
    bubble.classList.add('bubble');
    bubble.innerText = text;
    
    msgDiv.appendChild(bubble);
    chatWindow.appendChild(msgDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    return 'temp-loading';
}

function removeBubble(id) {
    const el = document.getElementById(id);
    if(el) el.remove();
}

