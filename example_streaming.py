from olymptrade.auth import OlympTradeAuth
from olymptrade.streaming import StreamingClient
import time

def on_price_update(data):
    print("Price update received:", data)

def main():
    username = "your_email@example.com"
    password = "your_password"
    auth = OlympTradeAuth(username, password, demo=True)
    if not auth.login():
        print("Login failed.")
        return

    client = StreamingClient(auth)
    client.connect()

    # Subscribe to price updates event (example event name)
    client.subscribe("price_update", on_price_update)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Disconnecting...")
        client.disconnect()

if __name__ == "__main__":
    main()
