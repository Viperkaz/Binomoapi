import os
import ssl
import time
import json
import certifi
import logging
import urllib3
import typing
import threading
from .exceptions import BinomoTimeout
from .http.login import Login
from .http.logout import Logout
from .ws.channels.ssid import Ssid
from .ws.channels.trade import Trade
from .ws.channels.candles import GetCandles
from .ws.objects.timesync import TimeSync
from .ws.objects.candles import Candles
from .ws.objects.profile import Profile
from .ws.client import WebsocketClient
from .http import Login, Logout
urllib3.disable_warnings()
logger = logging.getLogger(__name__)

cert_path = certifi.where()
os.environ["SSL_CERT_FILE"] = cert_path
os.environ["WEBSOCKET_CLIENT_CA_BUNDLE"] = cert_path
cacert = os.environ.get("WEBSOCKET_CLIENT_CA_BUNDLE")

class BinomoAPI(object):
    def __init__(self, set_ssid, device_id):
        self.set_ssid = set_ssid
        self.device_id = device_id
        self.https_url = "https://api.binomo-financing.com"
        self.wss_url = "wss://ws.binomo-financing.com/?v=2&vsn=2.0.0"
        self.websocket_client = None
        self.websocket_thread = None
        self.profile = Profile()
        self.timesync = TimeSync()
        self.candles = Candles()

    @property
    def login(self):
        return Login(self)

    @property
    def logout(self):
        return Logout(self)

    @property
    def ssid(self):
        return Ssid(self)

    @property
    def trade(self):
        return Trade(self)

    @property
    def get_candles(self):
        return GetCandles(self)

    def start_websocket(self):
        self.websocket_client = WebsocketClient(self)
        self.websocket_thread = threading.Thread(target=self.websocket_client.run_forever)
        self.websocket_thread.daemon = True
        self.websocket_thread.start()

    def send_websocket_request(self, data):
        if self.websocket_client:
            self.websocket_client.send(data)

    def connect(self):
        self.start_websocket()
        return self.ssid.send()

    def close(self):
        if self.websocket_client:
            self.websocket_client.close()

    def websocket_alive(self):
        return self.websocket_thread and self.websocket_thread.is_alive()
