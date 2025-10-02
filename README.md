# Olymp Trade Python Library

A modular Python package for accessing Olymp Trade market data and account information, designed for use in trading bots.

## Features

- Secure authentication for demo and live accounts
- Fetch real-time market prices for all instruments (forex, crypto, stocks, indices)
- Fetch historical candle data for all standard timeframes (1m, 5m, 15m, 30m, 1h, 4h, 1d, etc.)
- Retrieve account info including balance, open trades, and trading history
- Real-time streaming updates for market data
- Graceful error handling and reconnections
- Example scripts demonstrating usage

## Installation

```bash
pip install requests websocket-client
```

Clone this repository or copy the `olymptrade` package into your project.

## Usage

### Authentication

```python
from olymptrade.auth import OlympTradeAuth

auth = OlympTradeAuth("your_email@example.com", "your_password", demo=True)
auth.login()
token = auth.get_token()
print("Token:", token)
```

### Fetch Market Data

```python
from olymptrade.auth import OlympTradeAuth
from olymptrade.market_data import MarketData

auth = OlympTradeAuth("your_email@example.com", "your_password", demo=True)
auth.login()

market_data = MarketData(auth)
instruments = market_data.get_instruments()
print(instruments)

price = market_data.get_realtime_price(instruments[0]["id"])
print("Real-time price:", price)

candles = market_data.get_historical_candles(instruments[0]["id"], "1m", count=10)
print(candles)

account_info = market_data.get_account_info()
print(account_info)
```

### Real-time Streaming

```python
from olymptrade.auth import OlympTradeAuth
from olymptrade.streaming import StreamingClient

def on_price_update(data):
    print("Price update:", data)

auth = OlympTradeAuth("your_email@example.com", "your_password", demo=True)
auth.login()

client = StreamingClient(auth)
client.connect()
client.subscribe("price_update", on_price_update)

# Keep running to receive updates
import time
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    client.disconnect()
```

## Security

- Authentication tokens are handled securely within the library.
- Avoid hardcoding credentials in production; use environment variables or secure vaults.

## Future Enhancements

- Add functions for placing demo trades programmatically.
- Expand error handling and reconnection strategies.
- Support additional streaming events.

## License

MIT License
