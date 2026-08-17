from config import AMAZON_TAG

def make_affiliate_link(raw_url):
    """
    Yeh function raw URL mein hamara Amazon Affiliate Tag attach kar deta hai.
    """
    try:
        # Agar link amazon ka hai aur usme pehle se tag nahi hai
        if "amazon.in" in raw_url or "amazon.com" in raw_url:
            if "?" in raw_url:
                # Agar URL mein pehle se parameters hain toh &tag= jodh do
                if "tag=" not in raw_url:
                    affiliate_url = f"{raw_url}&tag={AMAZON_TAG}"
                else:
                    affiliate_url = raw_url
            else:
                # Agar URL seedha hai toh ?tag= jodh do
                affiliate_url = f"{raw_url}?tag={AMAZON_TAG}"
            return affiliate_url
        
        # Agar kisi aur site ka hai (jaise Flipkart), toh abhi ke liye wahi raw link return kar do
        return raw_url
        
    except Exception as e:
        print(f"[-] Error in affiliate generation: {e}")
        return raw_url

if __name__ == "__main__":
    # Test karne ke liye
    test_link = "https://www.amazon.in/dp/B0BRMY7NG8"
    print("Generated Link:", make_affiliate_link(test_link))