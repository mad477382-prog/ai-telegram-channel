import os
import random
import time
from html import escape

from openai import OpenAI

MODEL = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3-8b-instruct:free")

SYSTEM_PROMPT = (
    "أنت محرر محتوى محترف ومتخصص حصراً في السينما والأفلام والمسلسلات، "
    "تكتب لقناة تلغرام عربية اسمها «تحديات سينمائية». "
    "اكتب دائماً بلغة عربية فصحى مبسطة وجذابة. "
    "لا تخترع معلومات: إن لم تكن متأكداً من معلومة فاختر فيلماً أو حقيقة تعرفها جيداً. "
    "التزم بالتنسيق المطلوب حرفياً ولا تضف مقدمات أو شروحات خارج المطلوب."
)

GENRES = [
    "الخيال العلمي", "الإثارة والتشويق", "الجريمة", "الرعب", "الدراما",
    "الكوميديا", "الحركة", "الرسوم المتحركة", "الحرب", "السيرة الذاتية",
    "الغموض", "الأفلام الوثائقية", "الويسترن", "الرومانسية", "الفانتازيا",
]

ERAS = [
    "الأربعينيات والخمسينيات", "الستينيات", "السبعينيات", "الثمانينيات",
    "التسعينيات", "الألفية (2000-2009)", "العقد الماضي (2010-2019)",
    "السنوات الأخيرة",
]


def pick_genre() -> str:
    return random.choice(GENRES)


def pick_era() -> str:
    return random.choice(ERAS)


def ask_ai(user_prompt: str, temperature: float = 0.9,
           max_tokens: int = 700, retries: int = 3) -> str:
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ["OPENROUTER_API_KEY"],
    )
    last_error = None
    for attempt in range(1, retries + 1):
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
            )
            text = (resp.choices[0].message.content or "").strip()
            if text:
                return text
            last_error = "رد فارغ"
        except Exception as e:
            last_error = e
        print(f"[ask_ai] المحاولة {attempt} فشلت: {last_error}")
        time.sleep(5 * attempt)
    raise RuntimeError(f"فشل الاتصال بالذكاء الاصطناعي: {last_error}")


def safe(text: str) -> str:
    return escape(text.strip())
