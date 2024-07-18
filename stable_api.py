from .api import BinomoAPI
from .api import BinomoAPI
from .constants import ASSET_INDEX, EXPIRATION_TIMES
class Binomo:
    def __init__(self, set_ssid, device_id):
        self.api = BinomoAPI(set_ssid, device_id)

    def connect(self):
        return self.api.connect()

    def get_candles(self, asset, interval, count):
        return self.api.get_candles(asset, interval, count)

    def buy(self, asset, amount, direction, expiration):
        return self.api.trade.buy(asset, amount, direction, expiration)

    def get_balance(self):
        return self.api.profile.balance

    def close(self):
        self.api.close()
    def get_assets(self):
        return ASSET_INDEX

    def get_expiration_times(self):
        return EXPIRATION_TIMES

    def subscribe_to_asset(self, asset):
        return self.api.subscribe_to_asset(asset)

    def unsubscribe_from_asset(self, asset):
        return self.api.unsubscribe_from_asset(asset)

    def get_profile(self):
        return self.api.get_profile()