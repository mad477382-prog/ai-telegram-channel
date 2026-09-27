import os
import requests
import random
from datetime import datetime

# ============ الإعدادات ============
TG_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GEMINI_KEY = os.getenv("AI_API_KEY")

# ============ دالة الذكاء الاصطناعي ============
def ask_gemini(prompt):
    """إرسال طلب لـ Google Gemini"""
    # ✅ النموذج الصحيح
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    params = {"key": GEMINI_KEY}
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        response = requests.post(url, params=params, json=data, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"️ خطأ من API: {response.status_code}\n{response.text}"
    except Exception as e:
        return f"❌ خطأ في الاتصال: {str(e)}"

# ============ دالة تلغرام ============
def send_message(text):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    response = requests.post(url, json=payload)
    return response.status_code == 200

# ============ أنواع المحتوى ============
def generate_tip():
    return ask_gemini("اكتب نصيحة برمجية أو تقنية مفيدة في 3 أسطر بالعربية مع إيموجي وهاشتاق واحد.")

def generate_fact():
    return ask_gemini("اكتب حقيقة علمية أو تقنية غريبة ومثيرة في 3 أسطر بالعربية مع إيموجي.")

def generate_quiz():
    return ask_gemini("اكتب لغزاً تقنياً ممتعاً مع 4 خيارات (أ، ب، ج، د) بالعربية. لا تذكر الإجابة.")

# ============ النشر ============
def auto_post():
    content_types = [
        ("💡 نصيحة تقنية", generate_tip),
        ("🔬 حقيقة علمية", generate_fact),
        ("🧩 لغز تقني", generate_quiz)
    ]
    
    name, generator = random.choice(content_types)
    print(f" جاري توليد: {name}")
    
    content = generator()
    today = datetime.now().strftime("%Y-%m-%d")
    full_post = f"*{name}*\n📅 {today}\n\n{content}"
    
    if send_message(full_post):
        print("✅ تم النشر بنجاح!")
    else:
        print("❌ فشل النشر")

if __name__ == "__main__":
    print("🚀 بدء تشغيل البوت...")
    auto_post()
