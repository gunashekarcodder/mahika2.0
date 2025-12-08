from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from .models import TrustedContact, UserLocation
import json

@csrf_exempt
def trigger_sos(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized: Please login first'}, status=401)

    try:
        data = json.loads(request.body)
        lat = data.get('lat')
        lng = data.get('lng')
        
        # ✅ FIX: Use the standard Google Maps URL format
        if lat and lng:
            maps_link = f"https://www.google.com/maps?q={lat},{lng}"
        else:
            maps_link = "Location unavailable (GPS error)"

        # Save Location History
        if lat and lng:
            UserLocation.objects.create(
                user=request.user,
                latitude=lat,
                longitude=lng
            )

        # Get Contacts
        contacts = TrustedContact.objects.filter(user=request.user)
        if not contacts.exists():
            return JsonResponse({'status': 'warning', 'message': 'SOS sent, but no contacts found!'})

        # Prepare Email
        recipient_list = [c.email for c in contacts if c.email]
        contact_names = [c.name for c in contacts]

        subject = f"🚨 SOS: {request.user.username} needs help!"
        message_body = f"""
        URGENT SOS ALERT!
        
        User '{request.user.username}' has triggered an emergency alert.
        
        📍 CLICK TO TRACK LOCATION: 
        {maps_link}
        
        Please contact them or emergency services immediately.
        
        - Sent via MAHIKA Safety System
        """

        # Send Email
        if recipient_list:
            print(f"📧 Sending to: {recipient_list}") 
            send_mail(
                subject,
                message_body,
                settings.EMAIL_HOST_USER,
                recipient_list,
                fail_silently=False,
            )

        return JsonResponse({
            'status': 'ok', 
            'message': f'Alert sent to {len(recipient_list)} people.',
            'contacts_notified': contact_names
        })

    except Exception as e:
        print("❌ SOS Error:", str(e))
        return JsonResponse({'error': str(e)}, status=400)