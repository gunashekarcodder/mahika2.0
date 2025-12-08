document.addEventListener('DOMContentLoaded', () => {
    loadContacts();
    document.getElementById('addContactForm').addEventListener('submit', addContact);
});

async function loadContacts() {
    const list = document.getElementById('contactList');
    try {
        const response = await fetch('/api/contacts/');
        const data = await response.json();

        if (response.status === 401) {
            alert("Please login first.");
            window.location.href = '/';
            return;
        }

        list.innerHTML = ''; // Clear list
        if (data.contacts.length === 0) {
            list.innerHTML = '<li style="color:#94a3b8">No contacts added yet.</li>';
            return;
        }

        data.contacts.forEach(contact => {
            const li = document.createElement('li');
            li.className = 'contact-item';
            li.innerHTML = `
                <div>
                    <strong>${contact.name}</strong><br>
                    <small>${contact.email} ${contact.phone ? ' | ' + contact.phone : ''}</small>
                </div>
                <button class="btn-delete" onclick="deleteContact(${contact.id})">Remove</button>
            `;
            list.appendChild(li);
        });
    } catch (error) {
        console.error("Error loading contacts:", error);
    }
}

async function addContact(e) {
    e.preventDefault();
    const name = document.getElementById('c_name').value;
    const email = document.getElementById('c_email').value;
    const phone = document.getElementById('c_phone').value;

    try {
        const response = await fetch('/api/contacts/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, phone })
        });
        
        if (response.ok) {
            // Clear inputs and reload list
            document.getElementById('c_name').value = '';
            document.getElementById('c_email').value = '';
            document.getElementById('c_phone').value = '';
            loadContacts();
        } else {
            alert("Failed to add contact.");
        }
    } catch (error) {
        console.error(error);
    }
}

async function deleteContact(id) {
    if(!confirm("Remove this contact?")) return;
    
    await fetch(`/api/contacts/${id}/delete/`, { method: 'DELETE' });
    loadContacts();
}