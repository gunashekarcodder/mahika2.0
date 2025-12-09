from django.urls import path
from . import views

urlpatterns = [
    # Point to the new function 'chat_api'
    path('chat/', views.chat_api, name='chat_api'),
]