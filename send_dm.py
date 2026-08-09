import os
import csv
import json
import random
import requests
from datetime import datetime

def load_cookies():
    cookies_json = os.getenv("X_COOKIES_JSON")
    if not cookies_json:
        print("X_COOKIES_JSON topilmadi!")
        return None
    try:
        cookies_list = json.loads(cookies_json)
        # Cookie’larni dict formatiga o‘tkazamiz
        cookies = {}
        for c in cookies_list:
            if "name" in c and "value" in c:
                cookies[c["name"]] = c["value"]
        return cookies
    except Exception as e:
        print("Cookie o‘qishda xato:", e)
        return None

def load_messages():
    with open("messages.txt", "r", encoding="utf-8") as f:
        content = f.read().strip()
        messages = [m.strip() for m in content.split("\n\n") if m.strip()]
        return messages

def load_leads():
    leads = []
    with open("leads.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads.append(row)
    return leads

def already_sent(username):
    if not os.path.exists("sent_log.txt"):
        return False
    with open("sent_log.txt", "r", encoding="utf-8") as f:
        sent = [line.strip().lower() for line in f if line.strip()]
    return username.lower() in sent

def mark_as_sent(username):
    with open("sent_log.txt", "a", encoding="utf-8") as f:
        f.write(username + "\n")
    print(f"→ @{username} sent_log.txt ga qo‘shildi")

def personalize(message, name):
    return message.replace("{name}", name)

def send_dm(cookies, username, text):
    """
    Oddiy cookie asosida DM yuborish urinishi.
    Bu usul barqaror emas va xavfli.
    """
    try:
        # Asosiy headerlar
        headers = {
            "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
            "x-csrf-token": cookies.get("ct0", ""),
            "x-twitter-auth-type": "OAuth2Session",
            "x-twitter-active-user": "yes",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "content-type": "application/json",
        }

        # Avval user_id ni topishga harakat
        user_url = f"https://api.x.com/graphql/sLVLhh7bD0Ls7UueXDZJaA/UserByScreenName"
        # Bu qism murakkab, shuning uchun hozircha soddalashtirilgan variant

        print(f"DM yuborishga urinilmoqda → @{username}")
        print("Xabar:", text[:100] + "...")

        # Hozircha xavfsizlik uchun haqiqiy so‘rov yuborilmaydi
        # Keyinroq to‘liq endpoint qo‘shiladi
        print("⚠ Hozircha real yuborish o‘chirilgan (xavfsizlik uchun)")
        return False

    except Exception as e:
        print("Yuborishda xato:", e)
        return False

def main():
    print(f"[{datetime.now()}] Bot ishga tushdi")
    
    cookies = load_cookies()
    if not cookies:
        return
    
    print(f"Cookie yuklandi. Asosiy tokenlar: auth_token={'bor' if 'auth_token' in cookies else 'yo‘q'}, ct0={'bor' if 'ct0' in cookies else 'yo‘q'}")
    
    messages = load_messages()
    leads = load_leads()
    
    pending = [l for l in leads if not already_sent(l["username"])]
    
    if not pending:
        print("Barcha leadlar yozilgan.")
        return
    
    print(f"Qolgan yangi leadlar: {len(pending)} ta")
    
    lead = random.choice(pending)
    message_template = random.choice(messages)
    final_message = personalize(message_template, lead["name"])
    
    print(f"\nTanlandi: @{lead['username']}")
    print(f"Ism: {lead['name']}")
    print("-" * 50)
    
    # Haqiqiy yuborish
    success = send_dm(cookies, lead["username"], final_message)
    
    if success:
        mark_as_sent(lead["username"])
        print("DM muvaffaqiyatli yuborildi.")
    else:
        print("DM yuborilmadi (test yoki xato).")
        # Xavfsizlik uchun baribir belgilab qo‘yamizmi? Hozircha yo‘q
        # mark_as_sent(lead["username"])

if __name__ == "__main__":
    main()
