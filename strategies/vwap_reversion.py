import pandas as pd
import vectorbt as vbt
import ta
from strategies.base import StrategyBase


class VWAPReversionStrategy(StrategyBase):
    def __init__(self, price_data: pd.DataFrame, vwap_period: int = 20):
        super().__init__(price_data)
        self.vwap_period = vwap_period

    def generate_signals(self) -> pd.DataFrame:
        vwap = ta.volume.VolumeWeightedAveragePrice(
            high=self.price_data["high"],
            low=self.price_data["low"],
            close=self.price_data["close"],
            volume=self.price_data["volume"],
            window=self.vwap_period,
        ).volume_weighted_average_price()
        entries = self.price_data["close"] < vwap * 0.98
        exits = self.price_data["close"] > vwap
        signals = pd.DataFrame(index=self.price_data.index)
        signals["signal"] = 0
        signals.loc[entries, "signal"] = 1
        signals.loc[exits, "signal"] = -1
        return signals
