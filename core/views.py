from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

def login_view(request):
    """Renders the login page."""
    return render(request, 'login.html') 

  # Ideally, users should be logged in to see the dashboard/chat
def dashboard_view(request):
    """Renders the main dashboard."""
    return render(request, 'dashboard.html')

def chat_view(request):
    """Renders the chat interface."""
    return render(request, 'chat.html')


def character_select_view(request):
    """Renders the character selection screen."""
    return render(request, 'character_select.html')

def register_view(request):
    """Renders the registration page."""
    # This was the missing part causing the error!
    return render(request, 'register.html')

# ... existing imports ...

# Add this function at the bottom
def contacts_view(request):
    """Renders the trusted contacts management page."""
    return render(request, 'contacts.html')

# Add to bottom of core/views.py
def settings_view(request):
    return render(request, 'settings.html')



from .models import UserLocation, TrustedContact
from chat.models import Conversation, Message
from django.contrib.auth.models import User
from django.db.models import Count, Q

# ... existing views ...

def admin_dashboard_view(request):
    """
    Module 9: Custom Admin Dashboard for Judges/Admins.
    Visualizes system stats and risk levels.
    """
    # 1. Basic Counts
    total_users = User.objects.count()
    total_sos = UserLocation.objects.count() # Every SOS saves a location
    total_messages = Message.objects.count()
    
    # 2. Risk Stats (High Risk Messages)
    high_risk_alerts = Message.objects.filter(risk_score__gte=8).count()
    
    # 3. Recent Alerts (Last 5 SOS triggers)
    recent_alerts = UserLocation.objects.order_by('-captured_at')[:5]
    
    context = {
        'total_users': total_users,
        'total_sos': total_sos,
        'total_messages': total_messages,
        'high_risk_alerts': high_risk_alerts,
        'recent_alerts': recent_alerts
    }
    return render(request, 'admin_dashboard.html', context)