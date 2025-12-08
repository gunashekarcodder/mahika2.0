# mahika_project/urls.py - FINAL CORRECTION

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # 🎯 FIX 1: Include UI routes (dashboard/, chat/) at the ROOT path ''.
    path('', include('core.urls')), 
    
    # 🎯 FIX 2 (Optional but recommended): Prefix APIs with 'api/' for clean separation.
    # We must assume core.urls_location/core.urls_sos do NOT start with 'api/' themselves.
    path('api/', include('chat.urls')),
    path('api/', include('core.urls_location')), 
    path('api/', include('core.urls_sos')),
]