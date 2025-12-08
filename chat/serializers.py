# chat/serializers.py

from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender', 'text', 'risk_score', 'timestamp']

class ChatInputSerializer(serializers.Serializer):
    """Serializer for incoming messages from the frontend."""
    message = serializers.CharField(max_length=5000)
    char_id = serializers.IntegerField(required=True)
    # The frontend is responsible for passing the latest location data
    lat = serializers.FloatField(required=False)
    lng = serializers.FloatField(required=False)