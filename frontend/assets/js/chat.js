// frontend/assets/js/chat.js

// --- Configuration ---
// Make sure this matches the path defined in mahika_project/urls.py (api/ + chat/)
const CHAT_API_URL = 'http://127.0.0.1:8000/api/chat/'; 
// Use the ID of the character you just created in the admin panel
const DEFAULT_CHAR_ID = 1; 

// ... (rest of the file remains the same until handleChatSubmit)

// Inside the handleChatSubmit function:
function handleChatSubmit(event) {
    // ... (existing code to display message and scroll)

    // 3. Send message to Django API
    sendToChatAPI(messageText);
}


// Modified function to use Fetch API
function sendToChatAPI(message) {
    // ⚠️ IMPORTANT: Authentication is not fully set up (Member A/E's task)
    // We are using a dummy token or relying on the browser session for this test.
    const token = localStorage.getItem('mahika_jwt_token') || 'dummy_token'; 
    const currentCharacterId = DEFAULT_CHAR_ID; // Should come from a selector later

    // Payload includes message and character ID
    const payload = { 
        message: message, 
        char_id: currentCharacterId 
        // NOTE: We omit lat/lng for now, but your location.js should provide this later
    };

    // Placeholder response for now
    appendMessage("...Mahika is thinking...", 'bot');

    fetch(CHAT_API_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            // REQUIRED: Authorization header (only works if Auth Module is done)
            // For now, this might fail unless you are logged into admin in the same browser session.
            'Authorization': `Bearer ${token}` 
        },
        body: JSON.stringify(payload)
    })
    .then(response => {
        // Handle unauthorized (401) or other errors (400, 500)
        if (response.status === 401) {
             alert("Authentication failed. Please log in.");
             window.location.href = '/'; 
        }
        if (!response.ok) {
            throw new Error(`Chat API failed with status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        // Remove the thinking bubble
        const thinkingBubble = chatWindow.querySelector('.message.bot:last-child');
        if (thinkingBubble && thinkingBubble.innerText.includes('thinking')) {
             thinkingBubble.remove();
        }

        // Display the real response from the backend
        const botReplyText = data.bot_reply.text;
        appendMessage(botReplyText, 'bot');
        
        console.log(`Risk Score: ${data.current_risk_score}, Alert Triggered: ${data.alert_triggered}`);
        
        // If high risk is detected, show a visual warning (Module 6 integration)
        if (data.alert_triggered) {
            alert("⚠️ URGENT RISK DETECTED! Prepare for emergency dispatch.");
        }
    })
    .catch(error => {
        // Remove the thinking bubble and show network error
        const thinkingBubble = chatWindow.querySelector('.message.bot:last-child');
        if (thinkingBubble) thinkingBubble.remove();
        appendMessage(`Error: Could not connect to the API. ${error.message}`, 'bot');
        console.error('Chat API Error:', error);
    });
}