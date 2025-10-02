from olymptrade.auth import OlympTradeAuth
from olymptrade.market_data import MarketData

def main():
    username = "your_email@example.com"
    password = "your_password"
    auth = OlympTradeAuth(username, password, demo=True)
    if not auth.login():
        print("Login failed.")
        return

    market_data = MarketData(auth)

    instruments = market_data.get_instruments()
    print("Available instruments:", instruments)

    if instruments:
        instrument_id = instruments[0]["id"]
        price = market_data.get_realtime_price(instrument_id)
        print(f"Real-time price for instrument {instrument_id}: {price}")

        candles = market_data.get_historical_candles(instrument_id, "1m", count=10)
        print(f"Historical candles for instrument {instrument_id}:")
        for candle in candles:
            print(candle)

    account_info = market_data.get_account_info()
    print("Account info:", account_info)

if __name__ == "__main__":
    main()
