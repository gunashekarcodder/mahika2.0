from django.urls import path
from . import views
from . import api_auth
from . import api_contacts
from . import api_sos
from . import api_location
from . import api_privacy  # <--- Import new file

urlpatterns = [
    # Pages
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('chat/', views.chat_view, name='chat'),
    path('characters/', views.character_select_view, name='character_select'),
    path('contacts/', views.contacts_view, name='contacts'),
    path('settings/', views.settings_view, name='settings'), # <--- New Page

    # APIs
    path('auth/signup/', api_auth.signup_api, name='signup_api'),
    path('auth/login/', api_auth.login_api, name='login_api'),
    path('api/contacts/', api_contacts.contact_manager, name='contact_manager'),
    path('api/contacts/<int:contact_id>/delete/', api_contacts.contact_delete, name='contact_delete'),
    path('api/sos/trigger/', api_sos.trigger_sos, name='trigger_sos'),
    path('api/location/', api_location.save_location, name='save_location'),

    # Privacy APIs
    path('api/privacy/delete-chats/', api_privacy.delete_chat_history, name='delete_chats'),
    path('api/privacy/delete-account/', api_privacy.delete_account, name='delete_account'),

    # Add to urlpatterns:
path('admin-panel/', views.admin_dashboard_view, name='admin_dashboard'),
]