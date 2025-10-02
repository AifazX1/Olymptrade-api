import requests
from typing import List, Dict, Optional
from .auth import OlympTradeAuth

class MarketData:
    """
    Provides market data functions for Olymp Trade.
    """

    def __init__(self, auth: OlympTradeAuth):
        self.auth = auth
        self.base_url = "https://api-demo.olymptrade.com/api/v2" if self.auth.demo else "https://api.olymptrade.com/api/v2"

    def _get_headers(self) -> Dict[str, str]:
        token = self.auth.get_token()
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def get_instruments(self) -> List[Dict]:
        """
        Returns a list of all available instruments (forex, crypto, stocks, indices).
        """
        url = f"{self.base_url}/instruments"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()

    def get_realtime_price(self, instrument_id: int) -> Optional[float]:
        """
        Returns the real-time market price for the given instrument ID.
        """
        url = f"{self.base_url}/quotes/{instrument_id}"
        response = requests.get(url, headers=self._get_headers())
        if response.status_code == 200:
            data = response.json()
            return data.get("price")
        return None

    def get_historical_candles(self, instrument_id: int, timeframe: str, count: int = 100) -> List[Dict]:
        """
        Returns historical candle data for the given instrument ID and timeframe.
        Timeframe examples: '1m', '5m', '15m', '30m', '1h', '4h', '1d'
        """
        url = f"{self.base_url}/candles"
        params = {
            "instrument_id": instrument_id,
            "timeframe": timeframe,
            "count": count
        }
        response = requests.get(url, headers=self._get_headers(), params=params)
        response.raise_for_status()
        return response.json()

    def get_account_info(self) -> Dict:
        """
        Returns account information including balance, open trades, and trading history.
        """
        url = f"{self.base_url}/account"
        response = requests.get(url, headers=self._get_headers())
        response.raise_for_status()
        return response.json()
