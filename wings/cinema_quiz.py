from .base import ask_ai, pick_era, pick_genre, safe

NAME = "cinema_quiz"


def generate() -> str:
    genre, era = pick_genre(), pick_era()
    prompt = f"""ضع سؤال مسابقة سينمائي واحداً بأربعة خيارات، متوسط الصعوبة،
عن أفلام أو مسلسلات من نوع «{genre}» ومن فترة «{era}».

الشروط:
- سؤال واحد فقط، وإجابته صحيحة ومؤكدة.
- ضع الإجابة الصحيحة في مكان عشوائي بين الخيارات.
- التنسيق حرفياً (بدون أي زيادة):
السؤال: ...
أ) ...
ب) ...
ج) ...
د) ...
الإجابة: (الحرف واسم الخيار)
"""
    raw = ask_ai(prompt, temperature=0.9, max_tokens=400)

    if "الإجابة:" in raw:
        question, answer = raw.split("الإجابة:", 1)
        question = question.replace("السؤال:", "").strip()
        return (
            "🧠 <b>تحدي اليوم السينمائي</b>\n\n"
            f"{safe(question)}\n\n"
            "👇 اضغط لإظهار الإجابة:\n"
            f"<tg-spoiler>{safe(answer)}</tg-spoiler>\n\n"
            "#تحدي_سينمائي"
        )
    return f"🧠 <b>تحدي اليوم السينمائي</b>\n\n{safe(raw)}\n\n#تحدي_سينمائي"
