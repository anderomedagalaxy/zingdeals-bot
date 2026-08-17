import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID
from storage import is_deal_sent, save_sent_deal
from scraper import fetch_and_filter_deals

def run_bot():
    print("[*] Running Zingdeals Policy & Transparency Engine...")
    deals = fetch_and_filter_deals()
    
    if not deals:
        print("[!] No 100% transparent verified deals found right now. Skipping to avoid spam.")
        return

    for deal in deals:
        deal_id = deal["id"]
        
        if is_deal_sent(deal_id):
            continue  
            
        # 100% Transparent Template matching your exact USP
        deal_message = (
            "🔥 **ZINGDEALS VERIFIED LOOT** 🔥\n\n"
            f"📦 **{deal['title']}**\n\n"
            f"❌ **MRP:** ~{deal['mrp']}~\n"
            f"✅ **Loot Price:** {deal['price']}\n"
            f"💰 **Total Savings:** {deal['savings']}\n\n"
            f"🔗 **Grab Deal Here:** {deal['raw_link']}\n\n"
            "💎 *100% Transparent Deal - No Fake Claims, Only Real Loots!*"
        )
        
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHANNEL_ID,
            "text": deal_message,
            "parse_mode": "Markdown"
        }
        
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"[+] Successfully posted transparent deal to Telegram!")
            save_sent_deal(deal_id)
            break  
        else:
            print(f"[!] Failed to post: {response.text}")

if __name__ == "__main__":
    run_bot()