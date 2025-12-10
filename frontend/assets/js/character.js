// frontend/assets/js/character.js

// 1. Handle Card Selection
function selectCharacter(id, name) {
    // Remove 'active' class from all cards
    document.querySelectorAll('.character-card').forEach(card => {
        card.classList.remove('active');
        // Reset button text
        const btn = card.querySelector('.select-btn');
        if (btn) btn.innerText = "Select";
    });

    // Add 'active' class to the clicked card
    const activeCard = document.querySelector(`.character-card[data-id="${id}"]`);
    if (activeCard) {
        activeCard.classList.add('active');
        // Change button text
        const btn = activeCard.querySelector('.select-btn');
        if (btn) btn.innerText = "Selected";
    }

    // Save choice to LocalStorage (This connects to chat.js)
    localStorage.setItem('selected_char_id', id);
    localStorage.setItem('selected_char_name', name);
    
    console.log(`Character Selected: ${name} (ID: ${id})`);
}

// 2. Handle "Start Chatting" Button
function confirmAndGoToChat() {
    const charId = localStorage.getItem('selected_char_id');
    
    if (!charId) {
        alert("Please select a companion first.");
        return;
    }
    
    // Redirect to the Chat Page
    window.location.href = '/chat/';
}

// 3. Initialize (Restore previous selection)
document.addEventListener('DOMContentLoaded', () => {
    const savedId = localStorage.getItem('selected_char_id');
    const savedName = localStorage.getItem('selected_char_name');
    
    if (savedId && savedName) {
        selectCharacter(savedId, savedName);
    } else {
        // Default to ID 1 (Mahika)
        selectCharacter(1, 'Mahika - Safety Buddy');
    }
    
    // Handle the "Create New" button (Future Feature)
    const createBtn = document.querySelector('.create-new .select-btn');
    if(createBtn) {
        createBtn.onclick = (e) => {
            e.stopPropagation(); // Prevent bubbling
            alert("Custom Character Creation is coming in Version 2.0!");
        };
    }
});