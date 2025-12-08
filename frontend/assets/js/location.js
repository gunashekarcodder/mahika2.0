// frontend/assets/js/location.js

const API_LOCATION_URL = 'http://127.0.0.1:8000/api/location/';
const LOCATION_UPDATE_INTERVAL_MS = 10000; 

// Global Map Variables
let map = null;
let userMarker = null;

// --- 1. Initialize Map IMMEDIATELY (Default View) ---
function initMap() {
    // Check if map is already initialized
    if (map) return;

    console.log("Initializing Map...");
    
    // Default view: Center of India (Zoom level 5)
    // This ensures the map appears even if GPS is slow
    map = L.map('map-display').setView([20.5937, 78.9629], 5);

    // Add Tiles (The visual map layer)
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);
}

// --- 2. Update Map Position (When GPS data arrives) ---
function updateMapLocation(lat, lng) {
    if (!map) initMap(); // Safety check

    const newLatLng = new L.LatLng(lat, lng);

    if (!userMarker) {
        // Create marker if it doesn't exist
        userMarker = L.marker(newLatLng).addTo(map)
            .bindPopup("<b>You are here</b><br>Live Tracking On").openPopup();
    } else {
        // Move existing marker
        userMarker.setLatLng(newLatLng);
    }

    // Smoothly pan map to user
    map.flyTo(newLatLng, 15);
}

// --- 3. Core Geolocation Function ---
function getAndSendLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            onLocationSuccess,
            onLocationError,
            { enableHighAccuracy: true, timeout: 5000, maximumAge: 0 }
        );
    } else {
        console.error("Geolocation not supported.");
    }
}

// --- 4. Success Callback ---
function onLocationSuccess(position) {
    const lat = position.coords.latitude;
    const lng = position.coords.longitude;
    const accuracy = position.coords.accuracy;

    console.log(`📍 GPS Success: ${lat}, ${lng}`);

    // Update the visual map
    updateMapLocation(lat, lng);

    // Send to Backend
    const statusText = document.getElementById('location-status');
    if(statusText) statusText.innerText = `✅ Live: ${lat.toFixed(4)}, ${lng.toFixed(4)}`;

    fetch(API_LOCATION_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ lat, lng, accuracy })
    }).catch(err => console.error("API Error:", err));
}

// --- 5. Error Callback ---
function onLocationError(error) {
    console.warn("GPS Waiting/Error:", error.message);
    const statusText = document.getElementById('location-status');
    if(statusText) statusText.innerText = "⚠️ Waiting for GPS...";
}

// --- 6. Start Tracking (Called by Dashboard) ---
function startLocationTracking() {
    // 1. Draw default map immediately
    initMap(); 

    // 2. Start GPS loop
    console.log("Starting location service...");
    getAndSendLocation(); 
    setInterval(getAndSendLocation, LOCATION_UPDATE_INTERVAL_MS);
}

// Expose globally
window.startLocationTracking = startLocationTracking;