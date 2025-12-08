from django.db import models

# Create your models here.
# chat/models.py

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Character(models.Model):
    """Defines the AI personas (Mahika, Supportive Friend, etc.)."""
    name = models.CharField(max_length=100)
    prompt = models.TextField(help_text="The core personality prompt for the LLM.")
    is_safety_bot = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Conversation(models.Model):
    """Stores the history of a chat session."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    character = models.ForeignKey(Character, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Chat of {self.user.username} with {self.character.name}"

class Message(models.Model):
    """Stores individual messages in a conversation."""
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=[('user', 'User'), ('bot', 'Bot')])
    text = models.TextField()
    # The risk score returned by Bhagath/Manasa's modules
    risk_score = models.IntegerField(default=0) 
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"[{self.timestamp.strftime('%H:%M')}] {self.sender}: {self.text[:30]}..."