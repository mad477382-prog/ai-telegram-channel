import os
import requests

GEMINI_KEY = os.getenv("AI_API_KEY")
print(f"🔑 المفتاح المستخدم: {GEMINI_KEY[:10]}... (أول 10 أحرف)")

# جربنا نموذجين، الأول هو الأحدث والأكثر استقراراً
url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"

params = {"key": GEMINI_KEY}
data = {
    "contents": [{"parts": [{"text": "اكتب كلمة مرحب فقط"}]}]
}

print("📤 جاري الاتصال بـ Google Gemini...")
response = requests.post(url, params=params, json=data)

print(f"📡 حالة الاستجابة: {response.status_code}")
print(f"📝 رد جوجل الكامل: {response.text}")
