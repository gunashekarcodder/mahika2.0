from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from core.models import TrustedContact, UserLocation
from .models import Message, Character, Conversation
import json
import os
from groq import Groq

@csrf_exempt
def chat_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body)
        user_input = data.get('message', '')
        char_id = int(data.get('char_id', 1))
        
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Please login to chat'}, status=401)
            
        user = request.user
        
        # --- 1. AUTO-FIX DATABASE ---
        if not Character.objects.filter(id=1).exists():
            Character.objects.create(id=1, name="Mahika", prompt="You are Mahika, a strict safety bot.", is_safety_bot=True)
            Character.objects.create(id=2, name="Bestie", prompt="You are a supportive best friend.", is_safety_bot=False)
            Character.objects.create(id=3, name="Fun Bot", prompt="You are a funny bot.", is_safety_bot=False)

        # --- 2. GET CONVERSATION ---
        try:
            character = Character.objects.get(id=char_id)
        except Character.DoesNotExist:
            character = Character.objects.get(id=1)

        conversation, created = Conversation.objects.get_or_create(user=user, character=character)

        # --- 3. SAFETY CHECK ---
        risk_score = 0
        trigger_alert = False
        reply = ""
        user_input_lower = user_input.lower()

        if any(w in user_input_lower for w in ['kill', 'suicide', 'die', 'murder', 'blood', 'weapon']):
            risk_score = 10
            trigger_alert = True
            reply = "🚨 CRITICAL THREAT DETECTED. I am initiating emergency protocols."
        elif any(w in user_input_lower for w in ['danger', 'scared', 'hurt', 'follow']):
            risk_score = 8
            trigger_alert = True
            reply = f"{user.username}, I sense danger! Alerting contacts now."
        else:
            # --- 4. GROQ AI RESPONSE ---
            try:
                client = Groq(api_key=settings.GROQ_API_KEY)
                
                recent_msgs = Message.objects.filter(conversation=conversation).order_by('-timestamp')[:10]
                history_msgs = reversed(recent_msgs)
                
                messages_payload = [{"role": "system", "content": f"{character.prompt} User: {user.username}. Keep replies short."}]
                for m in history_msgs:
                    role = "assistant" if m.sender == 'bot' else "user"
                    messages_payload.append({"role": role, "content": m.text})
                messages_payload.append({"role": "user", "content": user_input})

                chat_completion = client.chat.completions.create(
                    messages=messages_payload,
                    model="llama-3.3-70b-versatile",
                )
                reply = chat_completion.choices[0].message.content

            except Exception as e:
                print(f"⚠️ Groq Error: {e}")
                reply = "I am monitoring your safety manually. (Offline Mode)"

        # --- 5. SAVE MESSAGES ---
        Message.objects.create(conversation=conversation, sender='user', text=user_input, risk_score=risk_score)
        Message.objects.create(conversation=conversation, sender='bot', text=reply, risk_score=0)

        # --- 6. SOS EMAIL WITH LOCATION ---
        if trigger_alert:
            contacts = TrustedContact.objects.filter(user=user)
            emails = [c.email for c in contacts if c.email]
            
            if emails:
                # ✅ CORRECTED FIELD NAME: 'captured_at' instead of 'timestamp'
                last_loc = UserLocation.objects.filter(user=user).order_by('-captured_at').first()
                
                if last_loc:
                    google_maps_link = f"https://www.google.com/maps?q={last_loc.latitude},{last_loc.longitude}"
                    location_info = f"📍 EXACT LOCATION: {google_maps_link}"
                else:
                    location_info = "📍 Location: GPS data not yet received (User must allow location on Dashboard)."

                email_subject = f"🚨 SOS ALERT: {user.username} is in DANGER!"
                email_body = (
                    f"URGENT: Mahika Safety System detected a high-risk message.\n\n"
                    f"👤 User: {user.username}\n"
                    f"💬 Message: '{user_input}'\n\n"
                    f"{location_info}\n\n"
                    f"Please check on them immediately."
                )

                print(f"📧 Sending SOS with Location to: {emails}")
                try:
                    send_mail(email_subject, email_body, settings.EMAIL_HOST_USER, emails, fail_silently=False)
                except Exception as e:
                    print(f"❌ Email Failed: {e}")

        return JsonResponse({
            "status": "ok",
            "bot_reply": { "text": reply, "sender": "bot" },
            "alert_triggered": trigger_alert
        })

    except Exception as e:
        print(f"❌ SERVER ERROR: {str(e)}")
        return JsonResponse({'error': str(e)}, status=400)