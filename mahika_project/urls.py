# mahika_project/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 1. UI Pages (Dashboard, Login, Chat UI) - MUST BE AT ROOT
    path('', include('core.urls')), 
    
    # 2. Chat API (The Brain)
    path('api/', include('chat.urls')), 

    # 3. Other APIs (Location, SOS)
    path('api/', include('core.urls_location')), 
    path('api/', include('core.urls_sos')),
]