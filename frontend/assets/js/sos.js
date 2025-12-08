document.addEventListener('DOMContentLoaded', () => {
    const sosBtn = document.getElementById('sos-trigger-btn');
    if (sosBtn) {
        sosBtn.addEventListener('click', handleSOS);
    }
});

function handleSOS() {
    const btn = document.getElementById('sos-trigger-btn');
    
    // 1. Confirm Intent
    if (!confirm("🚨 Are you sure you want to send an Emergency Alert?")) {
        return;
    }

    // 2. Visual Feedback
    btn.innerText = "📍 Getting Location...";
    btn.style.background = "linear-gradient(45deg, #f59e0b, #d97706)"; // Orange
    btn.disabled = true;

    // 3. Get Location & Send
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                sendAlertToBackend(position.coords.latitude, position.coords.longitude);
            },
            (error) => {
                console.warn("Location failed:", error);
                alert("⚠️ Could not get precise location. Sending alert with last known data.");
                sendAlertToBackend(null, null);
            },
            { enableHighAccuracy: true, timeout: 5000 }
        );
    } else {
        alert("Geolocation not supported.");
        sendAlertToBackend(null, null);
    }
}

async function sendAlertToBackend(lat, lng) {
    const btn = document.getElementById('sos-trigger-btn');
    btn.innerText = "📡 Sending Email...";

    try {
        const response = await fetch('/api/sos/trigger/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ lat, lng })
        });

        const data = await response.json();

        if (response.ok) {
            btn.innerText = "✅ HELP SENT!";
            btn.style.background = "linear-gradient(45deg, #10b981, #059669)"; // Green
            alert(data.message);
        } else {
            btn.innerText = "❌ FAILED";
            btn.style.background = "linear-gradient(45deg, #ef4444, #b91c1c)"; // Red
            alert("Error: " + (data.error || data.message));
            btn.disabled = false;
        }
    } catch (error) {
        console.error(error);
        btn.innerText = "❌ Network Error";
        alert("Network Error: Check server connection.");
        btn.disabled = false;
    }
}