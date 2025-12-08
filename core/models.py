from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model

# Retrieves the active User model
User = get_user_model()

# (Part of Module 1: User Authentication)
class TrustedContact(models.Model):
    """Stores the user's list of trusted contacts for SOS alerts."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trusted_contacts')
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=30, blank=True, null=True)
    priority = models.PositiveSmallIntegerField(default=1)  # 1 means contact first
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} for {self.user.username}"

# (Part of Location Module)
class UserLocation(models.Model):
    """Stores a user's geographical location history."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='locations')
    latitude = models.FloatField()
    longitude = models.FloatField()
    accuracy = models.FloatField(null=True, blank=True)
    captured_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} @ ({self.latitude}, {self.longitude})"
    
    class Meta:
        # Order by newest location first
        ordering = ['-captured_at']