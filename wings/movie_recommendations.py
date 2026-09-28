from .base import ask_ai, pick_genre, safe

NAME = "movie_recommendations"


def generate() -> str:
    genre = pick_genre()
    prompt = f"""رشّح 3 أفلام أو مسلسلات حقيقية ومعروفة من نوع «{genre}» تستحق المشاهدة.

الشروط:
- أعمال حقيقية فقط، مع سنة الإصدار الصحيحة التي تتأكد منها.
- لكل عمل جملة أو جملتان تشرحان لماذا يستحق المشاهدة، بدون حرق.
- التنسيق حرفياً:
1. الاسم (السنة): الشرح
2. الاسم (السنة): الشرح
3. الاسم (السنة): الشرح
"""
    raw = ask_ai(prompt, temperature=0.8, max_tokens=600)
    return (
        f"🍿 <b>ترشيحات اليوم: {safe(genre)}</b>\n\n"
        f"{safe(raw)}\n\n#ترشيحات_أفلام"
    )
