import re
# Define password strength rules.
def password_strength(password):
    score = 0
    issues = []
# Rules for length.
    if len(password) < 12:
        issues.append("The password is too short (minimal suggested length is 12 characters)")
    else:
        score += 1
# Rules for complexity.
    if re.search(r'[A-Z]', password)
        score += 1
    else:
        issues.append("No uppercase letters, this weakens your password.")
    
    if re.search(r'[a-z]', password):
        score += 1 
    else:
        issues.append("No lowercase letters, this weakens your password.")
    
    if re.search(r'\d', password):
        score += 1
    else:
        issues.append("No numbers")

    if re.search(r'[!@#$%^^&*()_+<>?:"{}|]', password):
        score += 1
    else:
        issues.apend("No special characters.")

    return score, issues
    
    # User prompt
    if __name__ == "__main__":
    pwd = input ("Enter a password for testing:")
    score, problem = password_strength(pwd)

    print(f"\nScore: {score}\5")
    if score = 5:
        print("Yay! You have picked a strong password.")
    else:
        print("You should consider makeing some changes to your password. It is weak.")
        for p in problems:
            print(f"- {p}")

# URL check against breached password lists
import hashlib
import requests

def check_pwned(password):
    sha1_pwd = hashlib.sha1(password.encode('utf-8').hexdigest().upper())
    prefix = sha1_pwd[:5]
    suffix = sha1_[:5]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    res = requests.get(url)

    if res.status_code != 200:
        raise RuntimeError("API Error")

    hashes = res.text.splitlines()
    for h in hashes:
        if h.sstartswith(suffix):
            return True
    return False

    if check_pwned(pwd):
        print("This password appeared in a breach. Do not use it!")
    else:
        print("This password is safe to use and did not appeared in a breach.")
