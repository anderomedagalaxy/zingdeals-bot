import os
import threading
import time
import requests
from flask import Flask
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHANNEL_ID
from storage import is_deal_sent, save_sent_deal
from scraper import fetch_and_filter_deals

# --- KEEP-ALIVE WEB SERVER (For Render Free Tier) ---
app = Flask('')

@app.route('/')
def home():
    return "ZingDeals Bot is active and running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()

# --- SELF-PING SCRIPT (Prevents Sleep Mode) ---
def self_ping():
    # Render khud ka external URL deta hai (Render environment variable)
    app_url = os.environ.get("RENDER_EXTERNAL_URL")
    if not app_url:
        print("[*] RENDER_EXTERNAL_URL not found, self-ping skipped.")
        return
    
    while True:
        try:
            response = requests.get(app_url)
            print(f"[ping] Self-ping status: {response.status_code}")
        except Exception as e:
            print(f"[ping] Error during self-ping: {e}")
        # Har 5 minute (300 seconds) mein khud ko ping karega
        time.sleep(300)

def start_ping_thread():
    t = threading.Thread(target=self_ping)
    t.daemon = True
    t.start()

# --- MAIN BOT LOGIC ---
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
    # 1. Start the Flask server in background for Render
    keep_alive()
    
    # 2. Start self-pinging thread so Render never sleeps
    start_ping_thread()
    
    print("[*] ZingDeals Engine started with Keep-Alive Web Server!")
    
    # Yahan agar tera bot loop mein chalna chahiye (jaise har kuch der baad deals check karna), 
    # toh tu apna main loop yahan run kar sakta hai. Abhi ke liye yeh ek baar run hoga.
    run_bot()
