import os
import requests
import random
from datetime import datetime
from openai import OpenAI

# ============ الإعدادات ============
TG_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OPENROUTER_KEY = os.getenv("OPENROUTER_API_KEY")

# التحقق من وجود المفتاح
if not OPENROUTER_KEY:
    print("❌ خطأ: مفتاح OPENROUTER_API_KEY غير موجود في GitHub Secrets!")
    exit(1)

print(f"✅ تم العثور على مفتاح OpenRouter: {OPENROUTER_KEY[:15]}...")

# إعداد عميل OpenRouter (متوافق مع OpenAI)
client = OpenAI(
    api_key=OPENROUTER_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# ============ دالة الذكاء الاصطناعي ============
def ask_ai(prompt):
    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3-8b-instruct:free",  # نموذج مجاني
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ خطأ: {str(e)}"

# ============ دالة تلغرام ============
def send_message(text):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    response = requests.post(url, json=payload)
    return response.status_code == 200

# ============ أنواع المحتوى ============
def generate_tip():
    return ask_ai("اكتب نصيحة برمجية أو تقنية مفيدة في 3 أسطر بالعربية مع إيموجي في البداية وهاشتاق واحد في النهاية.")

def generate_fact():
    return ask_ai("اكتب حقيقة علمية أو تقنية غريبة ومثيرة في 3 أسطر بالعربية مع إيموجي في البداية.")

def generate_quiz():
    return ask_ai("اكتب لغزاً تقنياً ممتعاً مع 4 خيارات (أ، ب، ج، د) بالعربية. لا تذكر الإجابة الآن.")

# ============ النشر ============
def auto_post():
    content_types = [
        ("💡 نصيحة تقنية", generate_tip),
        ("🔬 حقيقة علمية", generate_fact),
        ("🧩 لغز تقني", generate_quiz)
    ]
    
    name, generator = random.choice(content_types)
    print(f"📝 جاري توليد: {name}")
    
    content = generator()
    
    print("="*50)
    print("📄 المحتوى:")
    print(content)
    print("="*50)
    
    today = datetime.now().strftime("%Y-%m-%d")
    full_post = f"*{name}*\n📅 {today}\n\n{content}"
    
    print("📤 جاري النشر...")
    if send_message(full_post):
        print("✅ تم النشر بنجاح!")
    else:
        print("❌ فشل النشر")

if __name__ == "__main__":
    print(" بدء تشغيل البوت (OpenRouter)...")
    auto_post()
