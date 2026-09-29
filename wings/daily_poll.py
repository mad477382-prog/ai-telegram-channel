from .base import ask_ai, pick_topic

NAME = "daily_poll"


def generate() -> dict:
    topic = pick_topic()
    prompt = f"""ضع سؤال استفتاء (رأي أو تفضيل، وليس له إجابة صحيحة وخاطئة)
مرتبط بمجال «{topic}» أو موضوع عام يثير النقاش، مع 4 خيارات قصيرة.

التنسيق حرفياً:
السؤال: ...
1) ...
2) ...
3) ...
4) ...
"""
    raw = ask_ai(prompt, temperature=0.9, max_tokens=200)

    question, options = "استفتاء اليوم", []
    if "السؤال:" in raw:
        head, rest = raw.split("السؤال:", 1)
    else:
        rest = raw
    lines = [l.strip() for l in rest.splitlines() if l.strip()]
    if lines:
        question = lines[0]
        for l in lines[1:]:
            for prefix in ("1)", "2)", "3)", "4)", "-", "•"):
                if l.startswith(prefix):
                    l = l[len(prefix):].strip()
                    break
            if l:
                options.append(l[:100])

    options = options[:10] or ["نعم", "لا"]
    return {
        "type": "poll",
        "question": question[:255],
        "options": options,
        "is_anonymous": True,
    }
