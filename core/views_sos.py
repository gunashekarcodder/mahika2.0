import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import UserLocation # To save the final location
# NOTE: We need to import the alert dispatcher function from the sos app later

@login_required # Ensures only logged-in users can trigger SOS (requires Auth Module)
def trigger_sos_alert(request):
    """Receives SOS alert payload with location and dispatches notifications."""
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
        location_data = data.get('location', {})
        message = data.get('message', 'SOS button triggered.')

        lat = location_data.get('lat')
        lng = location_data.get('lng')
        accuracy = location_data.get('accuracy')
    except Exception:
        return JsonResponse({"detail": "Invalid JSON or payload structure."}, status=400)

    # 1. Save the final incident location immediately (Module 7)
    if lat and lng:
        loc = UserLocation.objects.create(
            user=request.user,
            latitude=lat,
            longitude=lng,
            accuracy=accuracy,
            # Use a high score/priority flag to mark this as an incident
            is_incident_location=True # This field should be added to UserLocation model later
        )
        print(f"SOS location saved: {loc.id}")
    else:
        print("SOS triggered without valid location data.")

    # 2. Call the Alerting Engine (Member D's Module 6)
    # Placeholder: In a real system, you would call a function like:
    # alert_dispatched = dispatch_alert(user=request.user, message=message, location=location_data)
    
    # Simulate a successful dispatch for testing
    alert_dispatched = True 

    if alert_dispatched:
        # TODO: Add logic to emit WebSocket notification to frontend and admin
        return JsonResponse({"status": "alert_dispatched", "detail": "Trusted contacts notified."}, status=202)
    else:
        return JsonResponse({"status": "error", "detail": "Failed to reach alerting service."}, status=500)