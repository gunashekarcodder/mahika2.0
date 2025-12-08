from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import uuid

def get_token(user):
    # In a real app, use JWT. For MVP, a random string works.
    return str(uuid.uuid4())

@csrf_exempt
def signup_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    try:
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            return JsonResponse({'detail': 'Username already taken'}, status=400)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        
        return JsonResponse({
            'status': 'ok',
            'token': get_token(user),
            'username': user.username
        })
    except Exception as e:
        return JsonResponse({'detail': str(e)}, status=400)

@csrf_exempt
def login_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)
    
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        # Allow login by email, find username first
        try:
            u = User.objects.get(email=email)
            username = u.username
        except User.DoesNotExist:
            username = email 

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                'status': 'ok',
                'token': get_token(user),
                'username': user.username
            })
        else:
            return JsonResponse({'detail': 'Invalid credentials'}, status=401)
    except Exception as e:
        return JsonResponse({'detail': str(e)}, status=400)