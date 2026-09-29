from .base import ask_ai, pick_topic, safe

NAME = "shocking_fact"


def generate() -> str:
    topic = pick_topic()
    prompt = f"""اكتب معلومة واحدة صادمة أو غريبة لكنها مؤكدة 100%،
من مجال «{topic}»، تخلي القارئ يتفاجأ.

الشروط:
- جملة أو جملتان فقط، بدون شرح إضافي.
- لا تبدأ بعبارات مثل "هل تعلم" أو "معلومة".
- لا تخترع رقماً أو حقيقة غير مؤكدة.
"""
    raw = ask_ai(prompt, temperature=0.75, max_tokens=150)
    return f"⚡ {safe(raw)}\n\n#معلومة_صادمة"
