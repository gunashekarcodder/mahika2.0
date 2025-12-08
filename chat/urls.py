# chat/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Main API endpoint for chat interaction
    path('chat/', views.ChatAPIView.as_view(), name='chat_api'),
]