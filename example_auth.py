from olymptrade.auth import OlympTradeAuth

def main():
    username = "your_email@example.com"
    password = "your_password"
    auth = OlympTradeAuth(username, password, demo=True)
    if auth.login():
        print("Login successful!")
        print("Token:", auth.get_token())
    else:
        print("Login failed.")

if __name__ == "__main__":
    main()
