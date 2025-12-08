from django.shortcuts import render

# Create your views here.
# chat/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.contrib.auth import get_user_model
from core.models import UserLocation # To save user's location snapshot

from .models import Character, Conversation, Message
from .serializers import ChatInputSerializer, MessageSerializer

# Placeholder for detection/scoring logic (Bhagath/Manasa's module)
def detect_and_score(text):
    """Simulates calling the NLP/Detection Module."""
    # TODO: Replace with an actual call to the detection microservice or function
    
    text_lower = text.lower()
    
    if 'danger' in text_lower or 'kill me' in text_lower or 'help' in text_lower:
        score = 9
        response_text = "I detect HIGH RISK. Please confirm your safety or press the SOS button!"
    elif 'sad' in text_lower or 'bad day' in text_lower:
        score = 4
        response_text = "I hear you. I'm here to listen. Remember, I'm monitoring for safety."
    else:
        score = 1
        response_text = "That's interesting! How does that relate to your safety concerns?"
        
    return score, response_text

class ChatAPIView(APIView):
    """Endpoint for sending messages and receiving responses/risk scores."""
    permission_classes = [IsAuthenticated] # Requires Auth Module to be working

    def post(self, request, *args, **kwargs):
        # 1. Validate input data
        serializer = ChatInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        
        user = request.user
        message_text = data['message']
        char_id = data['char_id']
        lat = data.get('lat')
        lng = data.get('lng')

        try:
            character = Character.objects.get(id=char_id)
        except Character.DoesNotExist:
            return Response({"detail": "Character not found."}, status=404)

        # 2. Find or create conversation
        conversation, created = Conversation.objects.get_or_create(
            user=user, character=character, defaults={'character': character}
        )

        with transaction.atomic():
            # 3. Save User's incoming message
            Message.objects.create(
                conversation=conversation, sender='user', text=message_text, risk_score=0
            )

            # 4. Save User Location snapshot (Module 7)
            if lat and lng:
                 UserLocation.objects.create(user=user, latitude=lat, longitude=lng)
            
            # 5. Get Risk Score and Bot Response (Module 4 & 5)
            risk_score, bot_response_text = detect_and_score(message_text)
            
            # 6. Check for high risk and trigger alert (Module 6)
            if risk_score >= 8:
                # TODO: Trigger Alerting Engine (calls Member D's module)
                print(f"HIGH RISK DETECTED for user {user.username}. Score: {risk_score}")
                # Placeholder: alert_triggered = True 

            # 7. Save Bot's response
            bot_message = Message.objects.create(
                conversation=conversation, sender='bot', text=bot_response_text, risk_score=risk_score
            )
            
        # 8. Return the bot's response and risk score
        response_serializer = MessageSerializer(bot_message)
        
        return Response({
            "status": "ok",
            "bot_reply": response_serializer.data,
            "current_risk_score": risk_score,
            "alert_triggered": risk_score >= 8 # Placeholder flag
        }, status=201)