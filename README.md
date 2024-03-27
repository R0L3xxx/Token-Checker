# Token Checker

Token Checker is a Python program that validates Discord tokens by checking their validity with the Discord API. It categorizes tokens into valid and invalid tokens and saves them into separate files.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/your-username/token-checker.git
Install the required dependencies: ```


``pip install -r requirements.txt``

Run the program:


``python token_checker.py``

Usage
The program will load the tokens from the tokens.txt file.
It will then validate each token by sending a request to the Discord API.
Valid tokens will be printed in green, and invalid tokens will be printed in red.
The program will also create valid_tokens.txt and invalid_tokens.txt files containing the valid and invalid tokens, respectively.
The total number of tokens, valid tokens, and invalid tokens will be displayed in light cyan, light green, and light red, respectively.
Notes
Make sure to keep your tokens secure and private. Do not share them with anyone.
This program is for educational purposes only. Use it responsibly and in accordance with Discord's Terms of Service.
