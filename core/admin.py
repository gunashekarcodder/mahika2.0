from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import TrustedContact, UserLocation

@admin.register(TrustedContact)
class TrustedContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'phone', 'priority', 'created_at')
    search_fields = ('name', 'phone', 'user__username')
    list_filter = ('priority',)

@admin.register(UserLocation)
class UserLocationAdmin(admin.ModelAdmin):
    list_display = ('user', 'latitude', 'longitude', 'accuracy', 'captured_at')
    search_fields = ('user__username',)
    list_filter = ('captured_at',)