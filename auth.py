import requests
import threading
import time

class OlympTradeAuth:
    """
    Handles authentication for Olymp Trade accounts (demo and live).
    """

    def __init__(self, username: str, password: str, demo: bool = True):
        self.username = username
        self.password = password
        self.demo = demo
        self.token = None
        self.token_expiry = None
        self.lock = threading.Lock()

    def login(self):
        """
        Logs in to Olymp Trade and retrieves an authentication token.
        """
        url = "https://api-demo.olymptrade.com/api/v2/login" if self.demo else "https://api.olymptrade.com/api/v2/login"
        payload = {
            "email": self.username,
            "password": self.password
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            self.token = data.get("token")
            self.token_expiry = time.time() + 3600  # Assuming token valid for 1 hour
            return True
        except requests.RequestException as e:
            print(f"Login failed: {e}")
            return False

    def get_token(self):
        """
        Returns a valid token, refreshing if necessary.
        """
        with self.lock:
            if self.token is None or time.time() >= self.token_expiry:
                success = self.login()
                if not success:
                    raise Exception("Authentication failed")
            return self.token
