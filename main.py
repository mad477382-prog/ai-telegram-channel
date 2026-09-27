import os
import requests
import random
from datetime import datetime

# ============ الإعدادات ============
TG_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GEMINI_KEY = os.getenv("AI_API_KEY")

# ============ دوال الذكاء الاصطناعي ============
def ask_gemini(prompt):
    """إرسال طلب لـ Google Gemini والحصول على الرد"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    
    data = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"️ خطأ من API: {response.status_code}\n{response.text}"

# ============ دوال تلغرام ============
def send_message(text):
    """إرسال رسالة إلى القناة"""
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    }
    
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        return True
    else:
        print(f"❌ خطأ تلغرام: {response.text}")
        return False

# ============ أنواع المحتوى ============
def generate_tip():
    """توليد نصيحة تقنية"""
    prompt = "اكتب نصيحة برمجية أو تقنية مفيدة في 3-4 أسطر باللغة العربية مع إيموجي مناسب في البداية وهاشتاق واحد في النهاية"
    return ask_gemini(prompt)

def generate_fact():
    """توليد حقيقة علمية"""
    prompt = "اكتب حقيقة علمية أو تقنية غريبة ومثيرة للاهتمام في 3 أسطر باللغة العربية مع إيموجي في البداية"
    return ask_gemini(prompt)

def generate_quote():
    """توليد اقتباس تحفيزي"""
    prompt = "اكتب اقتباساً تحفيزياً عن النجاح أو التعلم أو البرمجة مع ذكر قائله إن أمكن، باللغة العربية، في سطرين"
    return ask_gemini(prompt)

def generate_quiz():
    """توليد لغز أو سؤال تقني"""
    prompt = "اكتب سؤالاً أو لغزاً تقنياً ممتعاً مع 4 خيارات (أ، ب، ج، د) باللغة العربية. لا تذكر الإجابة الآن"
    return ask_gemini(prompt)

# ============ النشر التلقائي ============
def auto_post():
    """اختيار نوع محتوى عشوائي ونشره"""
    content_types = [
        ("💡 نصيحة تقنية", generate_tip),
        ("🔬 حقيقة علمية", generate_fact),
        ("✨ اقتباس تحفيزي", generate_quote),
        (" لغز تقني", generate_quiz)
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

# ============ التشغيل ============
if __name__ == "__main__":
    print("🚀 بدء تشغيل البوت...")
    auto_post()
