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
        return json.loads(cookies_json)
    except:
        print("Cookie JSON formatda emas!")
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
    """Oldin yozilgan odamlarni tekshiradi"""
    if not os.path.exists("sent_log.txt"):
        return False
    with open("sent_log.txt", "r", encoding="utf-8") as f:
        sent_users = [line.strip().lower() for line in f if line.strip()]
    return username.lower() in sent_users

def mark_as_sent(username):
    """Yuborilgan odamni logga yozadi"""
    with open("sent_log.txt", "a", encoding="utf-8") as f:
        f.write(username + "\n")
    print(f"→ @{username} sent_log.txt ga qo‘shildi")

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
    
    # Faqat oldin yozilmaganlarni olish
    pending = [l for l in leads if not already_sent(l["username"])]
    
    if not pending:
        print("Barcha leadlar allaqachon yozilgan. Yangi lead qo‘shing.")
        return
    
    print(f"Qolgan yangi leadlar: {len(pending)} ta")
    
    # Bitta random lead tanlash
    lead = random.choice(pending)
    message_template = random.choice(messages)
    final_message = personalize(message_template, lead["name"])
    
    print(f"\nTanlandi: @{lead['username']}")
    print(f"Ism: {lead['name']}")
    print(f"Xabar:\n{final_message}")
    print("-" * 50)
    
    # Hozircha test rejimi (haqiqiy yuborish keyin qo‘shiladi)
    print("TEST REJIMI: Haqiqiy DM yuborilmadi.")
    
    # Yuborilgan deb belgilash
    mark_as_sent(lead["username"])
    print("Muvaffaqiyatli yakunlandi.")

if __name__ == "__main__":
    main()
