import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from .models import UserLocation
from django.db.models import ObjectDoesNotExist # Import to handle missing user

User = get_user_model()

# WARNING: @csrf_exempt is for quick testing, secure with JWT/Token later!
@csrf_exempt
def save_location(request):
    """API to receive and save user location coordinates."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
        lat = data.get('lat')
        lng = data.get('lng')
        accuracy = data.get('accuracy')
        
        if lat is None or lng is None:
             return JsonResponse({'error': 'Missing lat or lng fields'}, status=400)

        latitude = float(lat)
        longitude = float(lng)
    except Exception as e:
        return JsonResponse({'error': f'Invalid JSON data: {e}'}, status=400)

    # --- Authentication Placeholder ---
    try:
        # Since we skipped createsuperuser, we need a way to get a user.
        # We'll use the first existing user, or create a simple 'testuser' if none exists.
        user = User.objects.first()
        if user is None:
             user = User.objects.create_user(username='testuser', email='test@mahika.com', password='testpassword')
             print("Created dummy testuser for API testing.")
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'System setup required: No users available.'}, status=500)
    # --- End Authentication Placeholder ---

    loc = UserLocation.objects.create(
        user=user,
        latitude=latitude,
        longitude=longitude,
        accuracy=accuracy if accuracy is not None else None,
    )

    return JsonResponse({
        'status': 'ok',
        'location_id': loc.id,
        'lat': loc.latitude,
        'lng': loc.longitude
    }, status=201)