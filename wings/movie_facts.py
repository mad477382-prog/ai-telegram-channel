from .base import ask_ai, pick_era, pick_genre, safe

NAME = "movie_facts"


def generate() -> str:
    genre, era = pick_genre(), pick_era()
    prompt = f"""اكتب منشوراً قصيراً لقناة تلغرام سينمائية عن حقيقة أو معلومة كواليس ممتعة
عن فيلم أو مسلسل شهير من نوع «{genre}» ومن فترة «{era}».

الشروط:
- اختر عملاً مشهوراً تعرف عنه معلومة مؤكدة، ولا تخترع شيئاً.
- بدون حرق لأحداث النهاية.
- الطول: من 60 إلى 90 كلمة.
- التنسيق حرفياً:
العنوان: (سطر واحد جذاب فيه اسم العمل)
المعلومة: (الفقرة)
"""
    raw = ask_ai(prompt, temperature=0.8, max_tokens=500)

    title, body = "حقيقة سينمائية", raw
    if "المعلومة:" in raw:
        head, body = raw.split("المعلومة:", 1)
        title = head.replace("العنوان:", "").strip() or title

    return f"🎬 <b>{safe(title)}</b>\n\n{safe(body)}\n\n#حقائق_سينمائية"
