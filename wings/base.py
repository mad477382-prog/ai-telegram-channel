import os
import random
import time
from html import escape

import requests
from openai import OpenAI

BASE_URL = "https://openrouter.ai/api/v1"

SYSTEM_PROMPT = (
    "أنت محرر محتوى محترف لقناة تلغرام عربية عامة ومنوعات. "
    "تكتب بلغة عربية فصحى مبسطة وجذابة ومختصرة. "
    "لا تخترع معلومات: اختر فقط معلومات أو أسئلة تعرفها بيقين تام. "
    "التزم بالتنسيق المطلوب حرفياً ولا تضف مقدمات أو شروحات خارج المطلوب."
)

TOPICS = [
    "الجغرافيا والدول", "التاريخ", "العلوم والفضاء", "جسم الإنسان",
    "الحيوانات والطبيعة", "الاختراعات والتكنولوجيا", "الرياضة",
    "الطعام والثقافات", "اللغات", "الفن والموسيقى", "علم النفس",
    "المحيطات والبحار", "الآثار والحضارات القديمة",
]

PREFERRED = ["llama", "gemma", "qwen", "gpt-oss", "mistral", "deepseek", "nemotron"]
EXCLUDED = ["coder", "vision", "-vl", "audio", "guard", "embed", "image"]


def pick_topic() -> str:
    return random.choice(TOPICS)


def get_api_key() -> str:
    key = os.getenv("OPENROUTER_API_KEY", "").strip()
    if not key.startswith("sk-or"):
        raise RuntimeError(
            "OPENROUTER_API_KEY غير صالح أو فارغ، أعد لصقه في GitHub Secrets"
        )
    return key


def free_models(api_key: str, limit: int = 6) -> list:
    try:
        r = requests.get(
            f"{BASE_URL}/models",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=20,
        )
        r.raise_for_status()
        data = r.json().get("data", [])
    except Exception as e:
        print(f"[models] تعذر جلب القائمة: {e}")
        return []

    found = []
    for m in data:
        mid = m.get("id", "")
        pricing = m.get("pricing", {})
        try:
            is_free = float(pricing.get("prompt", 1)) == 0 and float(pricing.get("completion", 1)) == 0
        except (TypeError, ValueError):
            is_free = False
        if not is_free or not mid.endswith(":free"):
            continue
        if any(x in mid.lower() for x in EXCLUDED):
            continue
        rank = next((i for i, k in enumerate(PREFERRED) if k in mid.lower()), len(PREFERRED))
        found.append((rank, -(m.get("context_length") or 0), mid))
    found.sort()
    return [mid for _, _, mid in found[:limit]]


def ask_ai(user_prompt: str, temperature: float = 0.7,
           max_tokens: int = 500, retries: int = 2) -> str:
    api_key = get_api_key()
    client = OpenAI(base_url=BASE_URL, api_key=api_key)

    candidates = []
    if os.getenv("OPENROUTER_MODEL", "").strip():
        candidates.append(os.getenv("OPENROUTER_MODEL").strip())
    candidates += free_models(api_key)
    candidates.append("openrouter/free")
    candidates = list(dict.fromkeys(candidates))
    print(f"[models] المرشحة: {candidates}")

    last_error = None
    for model in candidates:
        for attempt in range(1, retries + 1):
            try:
                resp = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt},
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                text = (resp.choices[0].message.content or "").strip()
                if text:
                    print(f"[models] نجح النموذج: {model}")
                    return text
                last_error = "رد فارغ"
            except Exception as e:
                last_error = e
            print(f"[ask_ai] {model} المحاولة {attempt} فشلت: {last_error}")
            time.sleep(3)
    raise RuntimeError(f"فشلت كل النماذج. آخر خطأ: {last_error}")


def safe(text: str) -> str:
    return escape(text.strip())
