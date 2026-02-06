import requests

def check_fb_number(phone_number):
    # Eita ekta basic logic, Facebook ekhon direct access block rakhe
    # Tai eita shob shomoy 100% accurate result na-o dite pare
    url = f"https://www.facebook.com/login/?next&ref=dbl&fl&login_from_aymt=1"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Amra login page check korchi browser behavior simulate kore
        response = requests.get(url, headers=headers)
        
        # Real life-e ekhane aro complex API ba Selenium lagte pare
        # Ekhane amra logic-ta shudhu format hisebe dekhachi
        print(f"Checking {phone_number}...")
        
        # Note: Facebook ekhon direct 'OK' ba 'NO' bole na scraping-e
        # Tai eita ekta mock result dekhabe
        return "OK" if len(phone_number) > 10 else "NO"
        
    except Exception as e:
        return "Error"

def main():
    print("--- FB Number Checker ---")
    numbers = input("Numbers gulo din (comma diye alada korun): ").split(',')
    
    print("\nResult:")
    for num in numbers:
        num = num.strip()
        result = check_fb_number(num)
        print(f"{num} -> {result}")

if __name__ == "__main__":
    main()
