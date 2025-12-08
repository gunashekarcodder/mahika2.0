from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from chat.models import Conversation, Message
from .models import UserLocation, TrustedContact

def is_authenticated(request):
    return request.user.is_authenticated

@csrf_exempt
def delete_chat_history(request):
    """
    Privacy Feature: Allows user to wipe all chat logs.
    This ensures 'Minimal Data Storage' principle.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    if not is_authenticated(request):
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        # Find all conversations for this user and delete them
        # Cascading delete will remove all associated Messages
        deleted_count, _ = Conversation.objects.filter(user=request.user).delete()
        
        print(f"🔒 PRIVACY ALERT: User {request.user.username} wiped {deleted_count} conversations.")
        
        return JsonResponse({
            'status': 'ok', 
            'message': 'Chat history securely erased.'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def delete_account(request):
    """
    GDPR Feature: Right to be forgotten.
    Deletes User, Locations, Contacts, and Chats.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    if not is_authenticated(request):
        return JsonResponse({'error': 'Unauthorized'}, status=401)

    try:
        user = request.user
        username = user.username
        
        # Delete the user object (Cascades to all other data)
        user.delete()
        
        print(f"🔒 ACCOUNT DELETED: {username} has left the system.")
        
        return JsonResponse({
            'status': 'ok', 
            'message': 'Account and all data permanently deleted.'
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)