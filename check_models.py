import google.generativeai as genai

# PASTE YOUR REAL KEY HERE
api_key = "AIzaSyDjmOhBLudYap3iu0bfpFlN3AlE9xWszoE"

genai.configure(api_key=api_key)

print("--- Searching for available Gemini models ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ AVAILABLE: {m.name}")
except Exception as e:
    print(f"❌ Error: {e}")