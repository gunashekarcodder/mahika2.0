# core/api_location.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserLocation
import json

@csrf_exempt
def save_location(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    # Allow anonymous for MVP testing, but prefer authenticated
    user = request.user if request.user.is_authenticated else None

    try:
        data = json.loads(request.body)
        lat = data.get('lat')
        lng = data.get('lng')
        accuracy = data.get('accuracy')

        if lat is None or lng is None:
            return JsonResponse({'error': 'Missing coordinates'}, status=400)

        # Only save if we have a logged-in user (prevents crash)
        if user:
            UserLocation.objects.create(user=user, latitude=lat, longitude=lng, accuracy=accuracy)
            return JsonResponse({'status': 'ok', 'message': 'Location Saved'})
        else:
            return JsonResponse({'status': 'ignored', 'message': 'User not logged in'})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)