// frontend/assets/js/character.js

function selectCharacter(id, name) {
    // 1. Visually update cards: remove active class from all
    document.querySelectorAll('.character-card').forEach(card => {
        card.classList.remove('active');
        const btn = card.querySelector('.select-btn');
        if(btn) btn.innerText = "Select";
    });

    // 2. Add active class to clicked card
    const activeCard = document.querySelector(`.character-card[data-id="${id}"]`);
    if (activeCard) {
        activeCard.classList.add('active');
        activeCard.querySelector('.select-btn').innerText = "Selected";
    }

    // 3. Save selection to LocalStorage (so chat.js can read it)
    localStorage.setItem('selected_char_id', id);
    localStorage.setItem('selected_char_name', name);
    
    console.log(`Selected character: ${name} (ID: ${id})`);
}

function confirmAndGoToChat() {
    const charId = localStorage.getItem('selected_char_id');
    if (!charId) {
        alert("Please select a companion first.");
        return;
    }
    // Redirect to chat page
    window.location.href = '/chat/';
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Restore previous selection if exists
    const savedId = localStorage.getItem('selected_char_id');
    if (savedId) {
        const name = localStorage.getItem('selected_char_name');
        selectCharacter(savedId, name);
    } else {
        // Default to ID 1 (Mahika)
        selectCharacter(1, 'Mahika - Safety Buddy');
    }
});