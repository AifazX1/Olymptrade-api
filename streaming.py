import threading
import websocket
import json
import time
from typing import Callable, Optional
from .auth import OlympTradeAuth

class StreamingClient:
    """
    Provides real-time streaming updates for Olymp Trade market data.
    """

    def __init__(self, auth: OlympTradeAuth):
        self.auth = auth
        self.ws = None
        self.thread = None
        self.running = False
        self.callbacks = {}
        self.url = "wss://stream-demo.olymptrade.com" if self.auth.demo else "wss://stream.olymptrade.com"

    def _on_message(self, ws, message):
        data = json.loads(message)
        event = data.get("event")
        if event and event in self.callbacks:
            self.callbacks[event](data)

    def _on_error(self, ws, error):
        print(f"WebSocket error: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        print("WebSocket connection closed")
        self.running = False

    def _on_open(self, ws):
        print("WebSocket connection opened")
        self.running = True

    def connect(self):
        headers = {
            "Authorization": f"Bearer {self.auth.get_token()}"
        }
        self.ws = websocket.WebSocketApp(
            self.url,
            header=headers,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close,
            on_open=self._on_open
        )
        self.thread = threading.Thread(target=self.ws.run_forever)
        self.thread.daemon = True
        self.thread.start()

    def subscribe(self, event: str, callback: Callable):
        """
        Subscribe to a specific event with a callback function.
        """
        self.callbacks[event] = callback
        # Send subscription message to server
        if self.ws and self.running:
            msg = json.dumps({"action": "subscribe", "event": event})
            self.ws.send(msg)

    def unsubscribe(self, event: str):
        """
        Unsubscribe from a specific event.
        """
        if event in self.callbacks:
            del self.callbacks[event]
            if self.ws and self.running:
                msg = json.dumps({"action": "unsubscribe", "event": event})
                self.ws.send(msg)

    def disconnect(self):
        """
        Disconnect the websocket connection.
        """
        if self.ws:
            self.ws.close()
        self.running = False
