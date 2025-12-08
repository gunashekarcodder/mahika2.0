from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import TrustedContact
import json

@csrf_exempt
def contact_manager(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    if request.method == 'GET':
        contacts = TrustedContact.objects.filter(user=request.user)
        data = [{"id": c.id, "name": c.name, "email": c.email} for c in contacts]
        return JsonResponse({'contacts': data})

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            TrustedContact.objects.create(
                user=request.user,
                name=data['name'],
                email=data['email'],
                phone=data.get('phone', '')
            )
            return JsonResponse({'status': 'ok'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def contact_delete(request, contact_id):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    if request.method == 'DELETE':
        TrustedContact.objects.filter(id=contact_id, user=request.user).delete()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)