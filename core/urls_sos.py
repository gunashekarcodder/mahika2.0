from django.urls import path
from . import views_sos # Import the SOS view

urlpatterns = [
    # SOS Alert Endpoint
    path('api/sos/trigger/', views_sos.trigger_sos_alert, name='trigger_sos'),
]