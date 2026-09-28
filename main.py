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


def send_to_telegram(text: str) -> None:
    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]
    if len(text) > TELEGRAM_LIMIT:
        text = text[: TELEGRAM_LIMIT - 1] + "…"
    r = requests.post(
        f"https://api.telegram.org/bot{token}/sendMessage",
        json={
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        },
        timeout=30,
    )
    if not r.ok:
        raise RuntimeError(f"Telegram error {r.status_code}: {r.text}")


def main():
    wing = choose_wing()
    print(f"الجناح المختار: {wing.NAME}")
    text = wing.generate()
    print(text)
    send_to_telegram(text)
    print("تم النشر بنجاح ✅")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"::error title=فشل البوت::{type(e).__name__}: {e}")
        raise
