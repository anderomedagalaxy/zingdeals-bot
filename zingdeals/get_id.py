import requests
from config import TELEGRAM_BOT_TOKEN

def get_group_id():
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    response = requests.get(url).json()
    
    print("\n--- Telegram Updates ---")
    if not response.get("result"):
        print("[!] Koi message nahi mila. Pehle apne ZingDeals group mein jaakar koi bhi message bhejo (jaise 'Hello' ya 'Hi'), fir yeh script dobara chalana.")
        return

    for update in response["result"]:
        if "message" in update:
            chat = update["message"]["chat"]
            print(f"Group Name: {chat.get('title')}")
            print(f"Group ID: {chat.get('id')}")
            print("-" * 30)

if __name__ == "__main__":
    get_group_id()