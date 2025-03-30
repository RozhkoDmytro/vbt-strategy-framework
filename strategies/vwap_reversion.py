import pandas as pd
import ta
from strategies.base import StrategyBase


class VWAPReversionStrategy(StrategyBase):
    def __init__(self, price_data: pd.DataFrame):
        super().__init__(price_data)

    def generate_signals(self) -> pd.DataFrame:
        """Generate signals based on VWAP reversion."""
        close = self.price_data.xs("close", level="ohlcv", axis=1).iloc[:, 0]
        high = self.price_data.xs("high", level="ohlcv", axis=1).iloc[:, 0]
        low = self.price_data.xs("low", level="ohlcv", axis=1).iloc[:, 0]
        volume = self.price_data.xs("volume", level="ohlcv", axis=1).iloc[:, 0]

        vwap_indicator = ta.volume.VolumeWeightedAveragePrice(
            high=high, low=low, close=close, volume=volume
        )
        vwap = vwap_indicator.volume_weighted_average_price()

        entries = close < vwap * 0.98  # Entry if 2% below VWAP
        exits = close > vwap  # Exit if price returns above VWAP

        signals = pd.DataFrame(0, index=close.index, columns=["signal"])
        signals.loc[entries, "signal"] = 1
        signals.loc[exits, "signal"] = -1

        return signals
