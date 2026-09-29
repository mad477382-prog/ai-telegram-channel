import os
import sys
from datetime import datetime, timezone

import requests

from wings import WINGS

TELEGRAM_LIMIT = 4096


def choose_wing():
    forced = os.getenv("WING", "").strip()
    if forced:
        if forced not in WINGS:
            sys.exit(f"جناح غير معروف: {forced}. المتاح: {', '.join(WINGS)}")
        return WINGS[forced]

    now = datetime.now(timezone.utc)
    slot = 0 if now.hour < 10 else 1 if now.hour < 15 else 2
    names = list(WINGS)
    index = (now.timetuple().tm_yday * 3 + slot) % len(names)
    return WINGS[names[index]]


def _post(method, payload):
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    return requests.post(
        f"https://api.telegram.org/bot{token}/{method}",
        json=payload,
        timeout=30,
    )


def send_to_telegram(content) -> None:
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    if isinstance(content, dict) and content.get("type") == "poll":
        r = _post("sendPoll", {
            "chat_id": chat_id,
            "question": content["question"],
            "options": content["options"],
            "is_anonymous": content.get("is_anonymous", True),
        })
        if not r.ok:
            raise RuntimeError(f"Telegram error {r.status_code}: {r.text}")
        return

    if isinstance(content, dict):
        text, photo = content["text"], content.get("photo")
    else:
        text, photo = content, None

    if photo:
        r = _post("sendPhoto", {
            "chat_id": chat_id,
            "photo": photo,
            "caption": text[:1024],
            "parse_mode": "HTML",
        })
        if r.ok:
            return
        print(f"فشل إرسال الصورة ({r.status_code}): {r.text} — سأرسل نصاً فقط")

    r = _post("sendMessage", {
        "chat_id": chat_id,
        "text": text[:TELEGRAM_LIMIT],
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    })
    if not r.ok:
        raise RuntimeError(f"Telegram error {r.status_code}: {r.text}")


def main():
    wing = choose_wing()
    print(f"الجناح المختار: {wing.NAME}")
    content = wing.generate()
    print(content)
    send_to_telegram(content)
    print("تم النشر بنجاح ✅")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"::error title=فشل البوت::{type(e).__name__}: {e}")
        raise
