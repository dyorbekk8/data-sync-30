import os
import csv
import json
import random
from datetime import datetime

def load_cookies():
    cookies_json = os.getenv("X_COOKIES_JSON")
    if not cookies_json:
        print("X_COOKIES_JSON topilmadi!")
        return None
    
    try:
        cookies = json.loads(cookies_json)
        return cookies
    except:
        print("Cookie JSON formatda emas!")
        return None

def load_messages():
    with open("messages.txt", "r", encoding="utf-8") as f:
        content = f.read().strip()
        # 3 ta xabarni ajratib olamiz
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
    with open("sent_log.txt", "r") as f:
        return username.lower() in f.read().lower()

def mark_as_sent(username):
    with open("sent_log.txt", "a") as f:
        f.write(username + "\n")

def personalize(message, name):
    return message.replace("{name}", name)

def main():
    print(f"[{datetime.now()}] Bot ishga tushdi")
    
    cookies = load_cookies()
    if not cookies:
        return
    
    print(f"Cookie yuklandi: {len(cookies)} ta")
    
    messages = load_messages()
    leads = load_leads()
    
    # Yuborilmagan leadlarni olish
    pending = [l for l in leads if not already_sent(l["username"])]
    
    if not pending:
        print("Barcha leadlar yuborilgan.")
        return
    
    # Bitta random lead tanlash
    lead = random.choice(pending)
    message_template = random.choice(messages)
    final_message = personalize(message_template, lead["name"])
    
    print(f"Tanlandi: @{lead['username']}")
    print(f"Xabar:\n{final_message}")
    print("-" * 40)
    print("Hozircha faqat test rejimi. Haqiqiy yuborish keyin qo‘shiladi.")
    
    # Test uchun yuborilgan deb belgilaymiz
    mark_as_sent(lead["username"])
    print(f"@{lead['username']} yuborilganlar ro‘yxatiga qo‘shildi.")

if __name__ == "__main__":
    main()
