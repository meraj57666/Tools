import random
import string
import requests
from faker import Faker
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()
fake = Faker()

def generate_random_name():
    return fake.first_name(), fake.last_name()

def generate_random_birthdate():
    year = random.randint(1980, 2003)
    month = random.randint(1, 12)
    day = random.randint(1, 28)  # Simplify day selection
    return f"{month:02d}/{day:02d}/{year}"

def generate_random_email(first_name, last_name):
    domains = ["gmail.com", "yahoo.com", "outlook.com"]
    domain = random.choice(domains)
    number = random.randint(10, 9999)
    return f"{first_name.lower()}.{last_name.lower()}{number}@{domain}"

def banner():
    banner_text = """
███████╗ ██████╗ ██████╗  █████╗  ██████╗██╗  ██╗
██╔════╝██╔═══██╗██╔══██╗██╔══██╗██╔════╝██║ ██╔╝
█████╗  ██║   ██║██████╔╝███████║██║     █████╔╝ 
██╔══╝  ██║   ██║██╔══██╗██╔══██║██║     ██╔═██╗ 
███████╗╚██████╔╝██║  ██║██║  ██║╚██████╗██║  ██╗
╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
    """
    console.print(Panel(banner_text, title="Facebook Account Creator", subtitle="Termux Script", style="bold blue"))

def create_facebook_account(phone_number):
    first_name, last_name = generate_random_name()
    birthdate = generate_random_birthdate()
    email = generate_random_email(first_name, last_name)
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    console.print(f"[bold green]Generated Details:[/bold green]")
    console.print(f"Name: {first_name} {last_name}")
    console.print(f"Birthdate: {birthdate}")
    console.print(f"Email: {email}")
    console.print(f"Phone: {phone_number}")
    console.print(f"Password: {password}")

    # Simulated payload for Facebook signup (Note: This is a placeholder)
    payload = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone_number,
        "password": password,
        "birthdate": birthdate,
        "gender": random.choice(["male", "female", "custom"]),
    }

    console.print("\n[bold yellow]Triggering OTP request to the phone number...[/bold yellow]")

    # NOTE: Facebook signup API is private and protected by anti-bot measures.
    # This is a placeholder to simulate OTP trigger.
    # Replace the URL and payload with actual API if available and legal.
    try:
        response = requests.post("https://mbasic.facebook.com/reg/", data=payload, timeout=10)
        if response.status_code == 200:
            console.print("[bold green]OTP request triggered successfully! Check your phone.[/bold green]")
        else:
            console.print(f"[bold red]Failed to trigger OTP. Status code: {response.status_code}[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error triggering OTP: {e}[/bold red]")

def main():
    banner()
    phone_number = Prompt.ask("[bold cyan]Enter the phone number (with country code)[/bold cyan]")
    create_facebook_account(phone_number)

if __name__ == "__main__":
    main()
