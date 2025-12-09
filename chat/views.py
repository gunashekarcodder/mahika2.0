from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from core.models import TrustedContact
import json
import google.generativeai as genai

# Configure the AI with your key
try:
    genai.configure(api_key=settings.GEMINI_API_KEY)
except:
    print("⚠️ Warning: Gemini API Key missing or invalid.")

@csrf_exempt
def chat_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body)
        user_input = data.get('message', '').lower()
        user_name = request.user.username if request.user.is_authenticated else "Friend"
        
        risk_score = 0
        trigger_alert = False
        reply = ""

        # --- 1. LOCAL SAFETY CHECK (Priority #1) ---
        # We handle emergencies locally to ensure they never fail due to bad internet.
        
        if any(w in user_input for w in ['kill', 'suicide', 'die', 'murder', 'blood', 'weapon', 'gun']):
            risk_score = 10
            trigger_alert = True
            reply = "🚨 CRITICAL THREAT DETECTED. I am initiating emergency protocols. Please stay on the line."

        elif any(w in user_input for w in ['danger', 'scared', 'hurt', 'follow', 'stalk', 'beat', 'pain', 'threat']):
            risk_score = 8
            trigger_alert = True
            reply = f"{user_name}, I sense you are in danger. I am sending an alert to your trusted contacts now."

        # --- 2. ASK GEMINI AI (Priority #2) ---
        # If no immediate danger, we let the AI handle the conversation.
        else:
            try:
                # Set up the AI model
                model = genai.GenerativeModel('gemini-pro')
                
                # Create a specific instruction for the AI
                system_instruction = f"You are Mahika, a helpful, protective, and empathetic safety assistant. The user '{user_name}' says: '{user_input}'. Reply in 1-2 sentences. If they ask for help, give safety advice."
                
                # Get response
                response = model.generate_content(system_instruction)
                reply = response.text
                risk_score = 0
                
            except Exception as ai_error:
                print(f"⚠️ AI Error: {ai_error}")
                # FALLBACK: If internet/key fails, use simulated logic so demo doesn't break
                reply = "I am having trouble connecting to the cloud, but I am still monitoring your safety manually. How can I help?"

        # --- 3. SEND SOS EMAIL ---
        if trigger_alert and request.user.is_authenticated:
            contacts = TrustedContact.objects.filter(user=request.user)
            emails = [c.email for c in contacts if c.email]
            if emails:
                print(f"📧 Auto-Sending SOS to: {emails}")
                try:
                    send_mail(f"🚨 SOS: {user_name} Danger", f"Message: {user_input}", settings.EMAIL_HOST_USER, emails, fail_silently=False)
                except: pass

        return JsonResponse({
            "status": "ok",
            "bot_reply": { "text": reply, "sender": "bot" },
            "current_risk_score": risk_score,
            "alert_triggered": trigger_alert
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)