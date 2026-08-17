import requests
from bs4 import BeautifulSoup
import re

def fetch_and_filter_deals():
    """
    Fetches live deals directly from DesiDime Telegram Web Page (No 404 / Blocked RSS)
    and strictly enforces Zingdeals Transparency Policy.
    """
    url = "https://t.me/s/desidime"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"[!] DesiDime fetch failed with status: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        message_divs = soup.find_all('div', class_='tgme_widget_message_text')
        
        verified_deals = []
        
        for div in message_divs:
            try:
                text = div.get_text(separator="\n").strip()
                
                # DesiDime format pattern matching:
                # Example: "55% off on - HAVELLS Hair Dryer - Rs. 585"
                match = re.search(r'(\d+)%\s*off\s*on\s*-\s*(.*?)\s*-\s*(?:Rs\.?|₹)\s*([\d,]+)', text, re.IGNORECASE)
                
                if not match:
                    continue
                    
                discount_pct = int(match.group(1))
                title = match.group(2).strip()
                deal_price = float(match.group(3).replace(',', ''))
                
                if discount_pct <= 0 or discount_pct >= 99 or deal_price <= 0:
                    continue
                    
                # Zingdeals Policy: Exact MRP & Savings Calculation
                mrp = deal_price / (1 - (discount_pct / 100))
                savings = mrp - deal_price
                
                # Extracting Buy Now link
                link_match = re.search(r'(https?://ddime\.in/\S+)', text)
                deal_link = link_match.group(1) if link_match else "https://www.desidime.com"
                
                deal_id = deal_link.split("/")[-1] if "ddime.in" in deal_link else str(hash(title))
                
                verified_deals.append({
                    "id": deal_id,
                    "title": title,
                    "mrp": f"₹{mrp:,.0f}",
                    "price": f"₹{deal_price:,.0f}",
                    "savings": f"₹{savings:,.0f} ({discount_pct}% OFF)",
                    "raw_link": deal_link
                })
            except Exception:
                continue
                
        return verified_deals

    except Exception as e:
        print(f"[!] Error in DesiDime web scraper: {e}")
        return []