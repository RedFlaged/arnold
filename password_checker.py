import re 
import getpass
import hashlib
import requests # type: ignore
import secrets
import string

def check_password_strength(password):
    score = 0
    feedback = []

    if len(password) >= 12:
        score += 1
    else:
        feedback.append("Pasword should be at least 12 characters long.")

    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Password should contain at least one uppercase letter.")

    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Password should contain at least one lowercase letter.")


    if score == 5:
        return "Strong", feedback
    elif score == 4:
        return "Moderate", feedback
    else:
        return "Weak", feedback
    

def check_breach_status(password):
    try:
        sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix = sha1.hash[:5]
        suffix = sha1.hash[5:]

        url = f"https://api.pwnedpasswords.com/range/{prefix}"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            raise RuntimeError("Error fetching data from HIB API.")
        hashes =(line.split(':') for line in response.text.splitlines())
        for hash_suffix,count in hashes:

            if hash_suffix == suffix:
                return True, int(count)

        return False, 0

def strong_password_generator(length=16):
    if length < 12:
        length = 12
    characters = string .ascii_letters + string.digits + "!@#$%^&*()_+-={}|\[]:',./<>?"
    return ''.join(secrets.choice(characters) for _ in range (length))

def main():
    print("Password Strenth and Breach Checher")
    password = getpass.getpass("Enter the passwort you'd want to test (input hidden):")

    strength, tips = check_password_strength(password)
    print(f"\n Password Strength: {strength}")

    print("Checking if password has been exposed in a breach...")
    try:
        breached, count = check_breach_status(password)
        if breached:
            print("This password was leaked in a list of breached passwords, {count} times.")
        else:
            print("This password has not appeared in any breaches and is safe to use.")

    except Exception as e:
        print("Error checking the breach status of your password: {e}")
        return
    
    if strength != "Strong" or breached:
        print(f"\n Suggested Strong Password:")
        print(strong_password_generator())

    
if __name__ == "__main__":
    main()
