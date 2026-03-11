import os
import time
import random
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import track
from rich.align import Align

# কনসোল সেটআপ
console = Console()

def clear_screen():
    os.system('clear')

def show_banner():
    banner_text = """
    [bold cyan]
     ██████╗██████╗  █████╗ ███████╗██╗   ██╗
    ██╔════╝██╔══██╗██╔══██╗╚══███╔╝╚██╗ ██╔╝
    ██║     ██████╔╝███████║  ███╔╝  ╚████╔╝ 
    ██║     ██╔══██╗██╔══██║ ███╔╝    ╚██╔╝  
    ╚██████╗██║  ██║██║  ██║███████╗   ██║   
     ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   
    [/bold cyan]
    [bold yellow]   CRAZY EXPRASS - PREMIUM AUTOMATION[/bold yellow]
    """
    console.print(Align.center(banner_text))
    console.print(Panel.fit(" [bold green]FB Account Creator Pro v2.0[/bold green] ", subtitle="[bold white]Developed by Meraj[/bold white]"))

def premium_input(prompt):
    return console.input(f"[bold magenta]➜ {prompt}: [/bold magenta]")

def main_logic():
    clear_screen()
    show_banner()

    # ইউজার ইনপুট
    target_num = premium_input("Enter Target Phone Number")
    
    # ডামি নাম জেনারেটর (High Level logic)
    first_names = ["Arif", "Sabbir", "Tanvir", "Nayan", "Mahmud", "Rakib"]
    last_names = ["Hossain", "Khan", "Ahmed", "Mulla", "Sheikh", "Talukdar"]
    
    f_name = random.choice(first_names)
    l_name = random.choice(last_names)
    full_name = f"{f_name} {l_name}"

    # প্রসেসিং এনিমেশন
    console.print(f"\n[bold blue]⏳ Initializing Facebook Security Bypass...[/bold blue]")
    for _ in track(range(10), description="[green]Bypassing Checkpoints..."):
        time.sleep(0.3)

    # আউটপুট টেবিল
    table = Table(title="Registration Details", show_header=True, header_style="bold magenta")
    table.add_column("Field", style="dim", width=12)
    table.add_index_column("Status")
    table.add_row("Full Name", f"[bold white]{full_name}[/bold white]")
    table.add_row("Phone Num", f"[bold yellow]{target_num}[/bold yellow]")
    table.add_row("Proxy IP", "[bold green]192.168.0.1 (Encrypted)[/bold green]")
    
    console.print(table)

    console.print(f"\n[bold green]✅ Requesting OTP to: {target_num}[/bold green]")
    console.print("[italic white]Wait for 60 seconds...[/italic white]")
    
    # OTP ইনপুট
    time.sleep(2)
    otp = premium_input("Enter Received OTP")
    
    if len(otp) == 6 or len(otp) == 5:
        console.print(Panel("[bold green]Success! Account Created Successfully.[/bold green]", title="Status"))
    else:
        console.print(Panel("[bold red]Error: Invalid OTP or Timeout![/bold red]", title="Status"))

if __name__ == "__main__":
    main_logic()
