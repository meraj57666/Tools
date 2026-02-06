import time
import sys
import os

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def banner():
    clear()
    print(r"""
 __  __ _____  _____    _    ____  
|  \/  | ____|/ _ \ \  / \  |  _ \ 
| |\/| |  _| | | | \ \/ _ \ | |_) |
| |  | | |___| |_| |\  / ___ \|  __/ 
|_|  |_|_____|____/  \/_/   \_\_|    
    """)
    print("Location: MERAJ\n")

def select_option(prompt, options):
    print(prompt)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    while True:
        choice = input("Select option: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(options):
            return int(choice)
        else:
            print("Invalid choice, try again.")

def load_numbers(filename):
    if not os.path.isfile(filename):
        print(f"File '{filename}' not found.")
        sys.exit(1)
    with open(filename, "r") as f:
        numbers = [line.strip() for line in f if line.strip()]
    return numbers

def simulate_find_account(number, domain, device_type):
    # Simulate checking if account exists for the number on the domain/device
    time.sleep(0.5)
    # For demo, let's say every number ending with even digit exists
    return number[-1] in '02468'

def simulate_send_otp(number, speed):
    # Simulate sending OTP with delay based on speed
    delays = {'Slow': 3, 'Medium': 1.5, 'Fast': 0.5}
    time.sleep(delays.get(speed, 1))
    # Simulate success always
    return True

def main():
    banner()

    divacy_options = ['iPhone', 'Android', 'Windows', 'MacOS', 'Linux', 'Other']
    divacy_choice = select_option("Select Divacy (Device Type):", divacy_options)
    divacy = divacy_options[divacy_choice - 1]

    domain_options = [
        'm.facebook.com/login/identify/#',
        'www.facebook.com/login/identify/#',
        'mobile.facebook.com/login/identify/#',
        'All Facebook Domains'
    ]
    domain_choice = select_option("Select Facebook domain:", domain_options)
    domain = domain_options[domain_choice - 1]

    device_options = ['iPhone', 'Android', 'Windows', 'MacOS', 'Linux', 'Other']
    device_choice = select_option("Select device for sending OTP:", device_options)
    device = device_options[device_choice - 1]

    numbers_file = input("Enter filename containing numbers: ").strip()
    numbers = load_numbers(numbers_file)

    print(f"\nLoaded {len(numbers)} numbers from {numbers_file}.\n")

    speed_options = ['Slow', 'Medium', 'Fast']
    speed_choice = select_option("Select speed:", speed_options)
    speed = speed_options[speed_choice - 1]

    print("\nStarting process...\n")
    for idx, number in enumerate(numbers, 1):
        print(f"[{idx}/{len(numbers)}] Checking account for number: {number} ... ", end='')
        if simulate_find_account(number, domain, device):
            print("Account found. Sending OTP... ", end='')
            if simulate_send_otp(number, speed):
                print("OTP sent successfully.")
            else:
                print("Failed to send OTP.")
        else:
            print("Account not found.")
    print("\nProcess completed.")

if __name__ == "__main__":
    main()
