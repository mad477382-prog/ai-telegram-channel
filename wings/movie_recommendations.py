import os
import random

import requests

from .base import ask_ai, safe

NAME = "movie_recommendations"

API = "https://api.themoviedb.org/3"
IMG = "https://image.tmdb.org/t/p/w780"
CAPTION_LIMIT = 1024

GENRES = {
    28: "أكشن", 12: "مغامرات", 16: "رسوم متحركة", 35: "كوميدي",
    80: "جريمة", 18: "دراما", 14: "فانتازيا", 27: "رعب",
    9648: "غموض", 10749: "رومانسي", 878: "خيال علمي",
    53: "إثارة وتشويق", 10752: "حرب", 36: "تاريخي",
}


def _get(path, **params):
    key = os.getenv("TMDB_API_KEY", "").strip()
    if not key:
        raise RuntimeError("TMDB_API_KEY غير موجود، أضفه في GitHub Secrets")
    headers = {}
    if key.startswith("eyJ"):
        headers["Authorization"] = f"Bearer {key}"
    else:
        params["api_key"] = key
    r = requests.get(f"{API}{path}", params=params, headers=headers, timeout=20)
    r.raise_for_status()
    return r.json()


def _pick_movie():
    gid = random.choice(list(GENRES))
    for page in (random.randint(1, 8), 1):
        params = {
            "with_genres": gid,
            "sort_by": "vote_count.desc",
            "vote_count.gte": 2000,
            "vote_average.gte": 6.5,
            "language": "ar",
            "page": page,
        }
        results = [m for m in _get("/discover/movie", **params)["results"]
                   if m.get("poster_path")]
        if results:
            return random.choice(results)
    raise RuntimeError("لم يتم العثور على أفلام")


def _arabic_overview(movie_id, overview):
    if overview:
        return overview
    en = (_get(f"/movie/{movie_id}", language="en-US").get("overview") or "").strip()
    if not en:
        return ""
    prompt = (
        "لخّص النص الآتي عن قصة فيلم بالعربية في جملتين، بدون حرق للأحداث "
        "ودون إضافة أي معلومة من عندك:\n\n" + en
    )
    return ask_ai(prompt, temperature=0.3, max_tokens=250)


def generate():
    pick = _pick_movie()
    d = _get(f"/movie/{pick['id']}", language="ar", append_to_response="credits")

    title = d.get("title") or d.get("original_title") or ""
    original = d.get("original_title") or ""
    year = (d.get("release_date") or "")[:4]
    rating = round(d.get("vote_average") or 0, 1)
    runtime = d.get("runtime") or 0
    genres = "، ".join(g["name"] for g in d.get("genres", [])[:3])

    credits = d.get("credits", {})
    directors = [c["name"] for c in credits.get("crew", []) if c.get("job") == "Director"]
    cast = [c["name"] for c in credits.get("cast", [])[:4]]

    title_line = f"🎬 <b>{safe(title)}</b>"
    if original and original != title:
        title_line += f" | {safe(original)}"
    if year:
        title_line += f" ({year})"

    details = [""]
    if cast:
        details.append(f"🎭 <b>الممثلون:</b> {safe('، '.join(cast))}")
    if directors:
        details.append(f"🎥 <b>المخرج:</b> {safe(directors[0])}")
    details.append(f"⭐ <b>التقييم:</b> {rating}/10")
    if runtime:
        details.append(f"⏱ <b>المدة:</b> {runtime} دقيقة")
    if genres:
        details.append(f"🎞 <b>النوع:</b> {safe(genres)}")
    details_text = "\n".join(details) + "\n\n#ترشيحات_أفلام"

    overview = _arabic_overview(pick["id"], (d.get("overview") or "").strip())
    sep = "\n➖➖➖➖➖➖➖➖\n"
    fixed = len(title_line) + len(details_text) + 2 * len(sep) + 30
    room = max(CAPTION_LIMIT - fixed, 0)
    if len(overview) > room:
        overview = overview[: max(room - 1, 0)].rstrip() + "…"

    caption = title_line + sep
    if overview:
        caption += f"📖 <b>القصة:</b> {safe(overview)}" + sep
    caption += details_text.lstrip("\n") if not overview else details_text

    return {"text": caption, "photo": IMG + pick["poster_path"]}
