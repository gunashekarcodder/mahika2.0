from django.urls import path
from . import views_location # Import the view we just created

urlpatterns = [
    # Location API endpoint
    path('api/location/', views_location.save_location, name='save_location'),
]