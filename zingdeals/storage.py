import json
import os

DB_FILE = "sent_deals.json"

def load_sent_deals():
    """Load sent deals from the JSON file. If file doesn't exist, return an empty set."""
    if not os.path.exists(DB_FILE):
        return set()
    try:
        with open(DB_FILE, "r") as f:
            # Yahan pehle 'loadf' tha jisse error aa raha tha, ab yeh 'load' hai
            data = json.load(f) if os.path.getsize(DB_FILE) > 0 else []
            return set(data)
    except Exception as e:
        print(f"[!] Storage Load Error: {e}")
        return set()

def save_sent_deal(deal_id):
    """Save a new deal ID to the JSON file so it doesn't get repeated."""
    sent_deals = load_sent_deals()
    sent_deals.add(deal_id)
    with open(DB_FILE, "w") as f:
        json.dump(list(sent_deals), f)

def is_deal_sent(deal_id):
    """Check if the deal has already been sent before."""
    sent_deals = load_sent_deals()
    return deal_id in sent_deals