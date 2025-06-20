# arnoldcheck.py

import hashlib
import requests
import logging
import os
from rich.console import Console
from rich.text import Text

# Crazy cool ASCII Banner 
BANNER = r"""
            
                
      _                     _     _ 
     / \   _ __ _ __   ___ | | __| |        _         _
    / _ \ | '__| '_ \ / _ \| |/ _` |       | |_______| |
   / ___ \| |  | | | | (_) | | (_| |      ||  _______  ||
  /_/   \_\_|  |_| |_|\___/|_|\__,_|       |_|       |_|

    🛡️ ArnoldCheck - Password Inspector         
"""

# Setup Rich for colored terminal output
console = Console()

# Setup logging to log.txt
logging.basicConfig(
    filename='log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

# -------------------------------
# Password strength checker

def password_strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_symbol = any(not c.isalnum() for c in password)

    score = sum([has_upper, has_lower, has_digit, has_symbol])

    if length < 8 or score <= 1:
        return "Weak"
    elif length >= 12 and score >= 3:
        return "Strong"
    else:
        return "Medium"

# -------------------------------
# Get SHA-1 hash of password

def get_password_hash(password):
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    return sha1[:5], sha1[5:]  # Return prefix and suffix

# -------------------------------
# Query HIBP API with prefix

def check_pwned_api(prefix):
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f"API error: {res.status_code}")
    return res.text  # Return list of suffixes + counts

# -------------------------------
# Check if suffix is in the API response

def get_breach_count(hashes, suffix):
    hashes = (line.split(':') for line in hashes.splitlines())
    for hash_suffix, count in hashes:
        if hash_suffix == suffix:
            return int(count)
    return 0

# -------------------------------
# Main password check logic

def check_password(password):
    prefix, suffix = get_password_hash(password)
    response = check_pwned_api(prefix)
    count = get_breach_count(response, suffix)

    # Evaluate strength
    strength = password_strength(password)

    # Show strength
    console.print(f"[bold white]Password Strength:[/] [yellow]{strength}[/]")

    # Breach status
    if count:
        console.print(f"[bold red]⚠️  This password has been found {count} times in data breaches! You should think twice before using it.[/]")
        logging.info(f"Password found {count} times in breaches. Strength: {strength}")
    else:
        console.print(f"[bold green]✅ This password was NOT found in any known data breach.[/]")
        logging.info(f"Password is safe. Strength: {strength}")

# -------------------------------
# Main loop for user input

def run_checker():
    # Show banner only once at the start
    console.print(Text(BANNER, style="bold cyan"))

    while True:
        # Prompt for password input
        console.print("[bold blue]🔐 Enter password to check:[/]")
        password = input(">> ").strip()

        if not password:
            console.print("[bold red]Password cannot be empty![/]")
            logging.warning("Empty password submitted.")
            continue

        try:
            check_password(password)
        except Exception as e:
            console.print(f"[bold red]Error:[/] {e}")
            logging.error(f"Exception: {e}")

        # Ask to run again
        again = input("\n[?] Check another password? (y/n): ").strip().lower()
        if again != 'y':
            console.print("\n[bold green]Goodbye! Stay safe and pick 💪 passwords![/]")
            break

# -------------------------------
# Start the script

if __name__ == "__main__":
    run_checker()
