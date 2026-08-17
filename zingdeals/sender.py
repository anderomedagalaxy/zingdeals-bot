import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID

def format_deal_message(deal, affiliate_link):
    """
    Yeh function boring data ko ek 'Sundar Loot Card' mein badalta hai.
    """
    message = (
        f"🔥 **ZINGDEALS EXCLUSIVE LOOT** 🔥\n\n"
        f"📦 **{deal['title']}**\n\n"
        f"💥 Discount: `{deal['discount']}`\n"
        f"💰 Deal Price: **{deal['deal_price']}** *(MRP: {deal['mrp']})*\n\n"
        f"👉 **Grab Now:** {affiliate_link}\n\n"
        f"⚡ *Limited Time Deal - Grab Fast before price goes up!*"
    )
    return message

def send_to_telegram(message):
    """
    Yeh function Telegram Bot API ka use karke channel par message post karta hai.
    """
    # Agar abhi bot token set nahi kiya hai, toh warning dega
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("[!] Warning: Telegram Bot Token set nahi hai config.py mein!")
        print("--- Message jo Telegram par jana chahiye tha ---")
        print(message)
        print("-----------------------------------------------")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHANNEL_ID,
        "text": message,
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("[+] Deal successfully posted to Telegram channel!")
            return True
        else:
            print(f"[-] Failed to send message: {response.text}")
            return False
    except Exception as e:
        print(f"[-] Error connecting to Telegram API: {e}")
        return False

if __name__ == "__main__":
    # Test karne ke liye ek dummy deal
    from scraper import fetch_latest_deals
    from affiliate import make_affiliate_link
    
    d = fetch_latest_deals()
    link = make_affiliate_link(d['raw_link'])
    msg = format_deal_message(d, link)
    send_to_telegram(msg)