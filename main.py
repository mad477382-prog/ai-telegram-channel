import os
import random
from datetime import datetime
from openai import OpenAI

# ============ الإعدادات ============
TG_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
GROQ_KEY = os.getenv("GROQ_API_KEY")

# إعداد عميل Groq
client = OpenAI(
    api_key=GROQ_KEY,
    base_url="https://api.groq.com/openai/v1"
)

# ============ دالة الذكاء الاصطناعي ============
def ask_groq(prompt):
    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=300
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"️ خطأ: {str(e)}"

# ============ دالة تلغرام ============
def send_message(text):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    response = requests.post(url, json=payload)
    return response.status_code == 200

# ============ أنواع المحتوى ============
def generate_tip():
    return ask_groq("اكتب نصيحة برمجية أو تقنية مفيدة في 3 أسطر بالعربية مع إيموجي في البداية وهاشتاق واحد في النهاية.")

def generate_fact():
    return ask_groq("اكتب حقيقة علمية أو تقنية غريبة ومثيرة في 3 أسطر بالعربية مع إيموجي في البداية.")

def generate_quiz():
    return ask_groq("اكتب لغزاً تقنياً ممتعاً مع 4 خيارات (أ، ب، ج، د) بالعربية. لا تذكر الإجابة الآن.")

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
    
    # طباعة المحتوى للتأكد
    print("="*50)
    print("📄 المحتوى:")
    print(content)
    print("="*50)
    
    today = datetime.now().strftime("%Y-%m-%d")
    full_post = f"*{name}*\n📅 {today}\n\n{content}"
    
    print(" جاري النشر...")
    if send_message(full_post):
        print("✅ تم النشر بنجاح!")
    else:
        print("❌ فشل النشر")

if __name__ == "__main__":
    print("🚀 بدء تشغيل البوت (Groq)...")
    auto_post()
