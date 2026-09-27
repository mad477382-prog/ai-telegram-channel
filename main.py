import os
import requests

# 1. جلب البيانات
TG_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

print("="*40)
print("🔍 بدء عملية التشخيص...")
print(f"🔑 التوكن موجود: {'نعم' if TG_TOKEN else '❌ لا (تأكد من الاسم في Secrets)'}")
print(f"🆔 معرف القناة (Chat ID): {CHAT_ID}")
print("="*40)

# 2. محاولة إرسال رسالة اختبار بسيطة جداً (بدون ذكاء اصطناعي للتأكد من اتصال تلغرام)
test_message = "🧪 *رسالة تشخيص*\n\nإذا وصلت هذه الرسالة، يعني الاتصال ناجح 100%!"

url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"

payload = {
    "chat_id": CHAT_ID,
    "text": test_message,
    "parse_mode": "Markdown"
}

print("📤 جاري إرسال الطلب إلى تلغرام...")
response = requests.post(url, json=payload)

print(f"📡 حالة الاستجابة (Status Code): {response.status_code}")
print(f"📝 رد تلغرام الكامل: {response.text}")
print("="*40)

if response.status_code == 200:
    print("✅ نجاح باهر! الرسالة وصلت للقناة.")
else:
    print("❌ فشل الإرسال. انسخ 'رد تلغرام الكامل' وأرسله لي لأخبرك بالسبب الدقيق.")
