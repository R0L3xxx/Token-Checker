import os
import json
import random
import string
from datetime import datetime
import pytz

try:
    import requests
    from colorama import Fore, Style, init
except ImportError:
    print("Installing required packages...")
    os.system("pip install colorama==0.4.4 requests==2.26.0 pytz==2021.3")
    print("Packages installed. Please restart the script.")
    exit()

init()

class TokenChecker:
    def __init__(self):
        self.session = requests.Session()
        self.tokens = []
        self.valid_tokens = []
        self.invalid_tokens = []

    def load_tokens(self, filename='tokens.txt'):
        try:
            with open(filename, 'r') as file:
                self.tokens = [line.strip() for line in file.readlines() if line.strip()]
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")

    def check_tokens(self):
        if not self.tokens:
            print("No tokens loaded. Please provide a valid tokens file.")
            return

        for token in self.tokens:
            result = self.validate_token(token)
            if "Valid token" in result:
                print(f"{Fore.YELLOW}[{Fore.LIGHTGREEN_EX}+{Fore.LIGHTYELLOW_EX}]{Fore.LIGHTBLUE_EX} {result} {Style.RESET_ALL}")
                self.valid_tokens.append(token)
            else:
                print(f"{Fore.LIGHTYELLOW_EX}[{Fore.LIGHTRED_EX}-{Fore.LIGHTYELLOW_EX}]{Fore.LIGHTRED_EX} {result} {Style.RESET_ALL}")
                self.invalid_tokens.append(token)

        print(f"{Fore.LIGHTYELLOW_EX}\nTokens validation results:")
        print(f"{Fore.LIGHTCYAN_EX}Total tokens: {len(self.tokens)}{Style.RESET_ALL}")
        print(f"{Fore.LIGHTGREEN_EX}Valid tokens: {len(self.valid_tokens)}{Style.RESET_ALL}")
        print(f"{Fore.LIGHTRED_EX}Invalid tokens: {len(self.invalid_tokens)}{Style.RESET_ALL}")
        self.save_tokens()

    def validate_token(self, token):
        headers = {'Authorization': token}
        try:
            response = self.session.get("https://discord.com/api/v9/users/@me", headers=headers)
            if response.status_code == 200:
                return self.process_valid_token(token)
            elif response.status_code == 401 or "Unauthorized" in response.text:
                return "Invalid token"
            else:
                return f"Error with token: {token}, Status code: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return "Error validating token"

    def process_valid_token(self, token):
        return f"Valid token: {token[:10]}******"

    def save_tokens(self):
        if self.valid_tokens:
            with open("valid_tokens.txt", "w") as file:
                for token in self.valid_tokens:
                    file.write(f"{token}\n")
        
        if self.invalid_tokens:
            with open("invalid_tokens.txt", "w") as file:
                for token in self.invalid_tokens:
                    file.write(f"{token}\n")

    def get_nitro_expire_date(self, token):
        try:
            response = self.session.get("https://discord.com/api/v9/users/@me/billing/subscriptions", headers={'Authorization': token})
            if response.status_code == 200:
                subscriptions = response.json()
                for subscription in subscriptions:
                    if 'trial_ends_at' in subscription:
                        expire_date = subscription['trial_ends_at']
                        return datetime.fromisoformat(expire_date).replace(tzinfo=pytz.utc).strftime('%Y-%m-%d %H:%M:%S')
            return "Not Found"
        except requests.exceptions.RequestException as e:
            print(f"Error getting Nitro expire for token {token}: {str(e)}")
            return "Not Found"

def main():
    checker = TokenChecker()
    checker.load_tokens()

    if checker.tokens:
        checker.check_tokens()
    else:
        print("No tokens loaded. Please provide a valid tokens file.")

if __name__ == "__main__":
    main()
