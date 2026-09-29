from .base import ask_ai, pick_topic, safe

NAME = "daily_quiz"


def generate() -> str:
    topic = pick_topic()
    prompt = f"""ضع سؤال ثقافة عامة واحداً بأربعة خيارات، متوسط الصعوبة،
من مجال «{topic}».

الشروط:
- سؤال واحد فقط، وإجابته صحيحة ومؤكدة 100%.
- ضع الإجابة الصحيحة في مكان عشوائي بين الخيارات.
- التنسيق حرفياً (بدون أي زيادة):
السؤال: ...
أ) ...
ب) ...
ج) ...
د) ...
الإجابة: (الحرف واسم الخيار) - (جملة قصيرة توضح لماذا)
"""
    raw = ask_ai(prompt, temperature=0.8, max_tokens=350)

    if "الإجابة:" in raw:
        question, answer = raw.split("الإجابة:", 1)
        question = question.replace("السؤال:", "").strip()
        return (
            "🧠 <b>سؤال اليوم</b>\n\n"
            f"{safe(question)}\n\n"
            "👇 اضغط لإظهار الإجابة:\n"
            f"<tg-spoiler>{safe(answer)}</tg-spoiler>\n\n"
            "#سؤال_اليوم"
        )
    return f"🧠 <b>سؤال اليوم</b>\n\n{safe(raw)}\n\n#سؤال_اليوم"
