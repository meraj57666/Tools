import requests
import time

def load_numbers(filename):
    with open(filename, 'r') as f:
        numbers = [line.strip() for line in f if line.strip()]
    return numbers

def select_device():
    devices = {
        '1': 'iPhone',
        '2': 'Android',
        '3': 'Windows Phone',
        '4': 'BlackBerry',
        '5': 'Desktop',
        '6': 'Other'
    }
    print("Select device type:")
    for k, v in devices.items():
        print(f"{k}. {v}")
    choice = ''
    while choice not in devices:
        choice = input("Enter choice (1-6): ").strip()
    return devices[choice]

def select_domain():
    domains = {
        '1': 'https://m.facebook.com/login/identify/',
        '2': 'https://mbasic.facebook.com/login/identify/',
        '3': 'https://www.facebook.com/login/identify/',
        '4': 'https://touch.facebook.com/login/identify/',
        '5': 'https://free.facebook.com/login/identify/',
        '6': 'https://web.facebook.com/login/identify/'
    }
    print("Select Facebook domain:")
    for k, v in domains.items():
        print(f"{k}. {v}")
    choice = ''
    while choice not in domains:
        choice = input("Enter choice (1-6): ").strip()
    return domains[choice]

def send_otp(session, domain, number, device):
    headers = {
        'User-Agent': f'{device} Facebook App',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    # Prepare payload for Facebook's forgot password form
    payload = {
        'email': number,
        'did_submit': 'Search'
    }
    try:
        # Get initial page to get cookies and form data
        r = session.get(domain)
        if r.status_code != 200:
            print(f"Failed to access {domain} for {number}")
            return False

        # Facebook uses hidden inputs, but for simplicity, we send only email param
        # In real scenario, scraping hidden inputs and fb_dtsg tokens is needed

        r2 = session.post(domain, data=payload, headers=headers)
        if r2.status_code == 200 and ('We sent a code' in r2.text or 'Enter your code' in r2.text or 'Check your email' in r2.text):
            print(f"OTP sent successfully to {number}")
            return True
        else:
            print(f"Failed to send OTP to {number}")
            return False
    except Exception as e:
        print(f"Error sending OTP to {number}: {e}")
        return False

def main():
    print("Facebook OTP Sender Tool")
    numbers_file = input("Enter filename containing numbers: ").strip()
    numbers = load_numbers(numbers_file)
    if not numbers:
        print("No numbers loaded. Exiting.")
        return

    device = select_device()
    domain = select_domain()

    session = requests.Session()

    for number in numbers:
        send_otp(session, domain, number, device)
        time.sleep(5)  # slow down requests to avoid rate limiting

if __name__ == "__main__":
    main()
