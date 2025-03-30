import pandas as pd
import ta
import logging
from strategies.base import StrategyBase

logger = logging.getLogger(__name__)


class VWAPReversionStrategy(StrategyBase):
    def __init__(self, price_data: pd.DataFrame):
        super().__init__(price_data)

    def generate_signals(self) -> pd.DataFrame:
        close = self.price_data.xs("close", level="ohlcv", axis=1).iloc[:, 0]
        high = self.price_data.xs("high", level="ohlcv", axis=1).iloc[:, 0]
        low = self.price_data.xs("low", level="ohlcv", axis=1).iloc[:, 0]
        volume = self.price_data.xs("volume", level="ohlcv", axis=1).iloc[:, 0]

        vwap_indicator = ta.volume.VolumeWeightedAveragePrice(
            high=high, low=low, close=close, volume=volume
        )
        vwap = vwap_indicator.volume_weighted_average_price()

        entries = close < vwap * 0.98
        exits = close > vwap

        logger.debug(f"VWAP head:\n{vwap.head()}")
        logger.debug(f"Entries: {entries.sum()}, Exits: {exits.sum()}")

        debug_df = pd.DataFrame(
            {
                "close": close,
                "vwap": vwap,
                "entry": entries.astype(int),
                "exit": exits.astype(int),
            }
        )
        debug_df.to_csv("logs/vwap_debug.csv")

        signals = pd.DataFrame(0, index=close.index, columns=["signal"])
        signals.loc[entries, "signal"] = 1
        signals.loc[exits, "signal"] = -1

        return signals
