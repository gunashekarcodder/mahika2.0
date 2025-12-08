// frontend/assets/js/auth.js

const API_BASE_URL = 'http://127.0.0.1:8000'; // Your Django Server URL

// API Endpoints
const LOGIN_URL = `${API_BASE_URL}/auth/login/`;
const SIGNUP_URL = `${API_BASE_URL}/auth/signup/`;

// --- Utility Functions ---
function saveAuthToken(token) {
    localStorage.setItem('mahika_jwt_token', token);
    console.log("Token saved. Redirecting to dashboard...");
    window.location.href = '/dashboard/'; 
}

// --- Handle Registration (Signup) ---
async function handleSignup(event) {
    event.preventDefault(); 
    console.log("Signup button clicked...");

    const usernameInput = document.getElementById('su_username');
    const emailInput = document.getElementById('su_email');
    const passwordInput = document.getElementById('su_password');

    if (!usernameInput || !emailInput || !passwordInput) {
        console.error("Error: Input fields not found in HTML!");
        return;
    }

    const username = usernameInput.value;
    const email = emailInput.value;
    const password = passwordInput.value;

    try {
        const response = await fetch(SIGNUP_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: username, email: email, password: password })
        });

        const data = await response.json();

        if (response.ok) {
            // ✅ FIX: Do NOT save token here.
            alert("✅ Registration Successful! Please login to continue.");
            
            // ✅ FIX: Redirect to Login Page (Root URL)
            window.location.href = '/'; 
        } else {
            alert(`❌ Error: ${data.detail || 'Registration failed'}`);
        }
    } catch (error) {
        console.error("Network Error:", error);
        alert("❌ Could not connect to the server.");
    }
}

// --- Handle Login ---
async function handleLogin(event) {
    event.preventDefault();
    console.log("Login button clicked...");

    const email = document.getElementById('li_email').value;
    const password = document.getElementById('li_password').value;

    try {
        const response = await fetch(LOGIN_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email, password: password })
        });

        const data = await response.json();

        if (response.ok) {
            // Login successful -> Save token -> Go to Dashboard
            saveAuthToken(data.token);
        } else {
            alert(`❌ Login Failed: ${data.detail || 'Check credentials'}`);
        }
    } catch (error) {
        console.error("Network Error:", error);
        alert("❌ Could not connect to the server.");
    }
}

// --- Attach Listeners when Page Loads ---
document.addEventListener('DOMContentLoaded', () => {
    const signupForm = document.getElementById('signupForm');
    const loginForm = document.getElementById('loginForm');

    if (signupForm) {
        signupForm.addEventListener('submit', handleSignup);
        console.log("Signup Listener Attached.");
    }

    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
        console.log("Login Listener Attached.");
    }
});