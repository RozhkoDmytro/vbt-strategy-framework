import pandas as pd
import ta
import logging
from strategies.base import StrategyBase

logger = logging.getLogger(__name__)


class VWAPReversionStrategy(StrategyBase):
    requires_ohlcv = True

    def __init__(self, price_data: pd.DataFrame, vwap_period: int = 20):
        super().__init__(price_data)
        self.vwap_period = vwap_period

    def generate_signals(self) -> pd.DataFrame:
        if not isinstance(self.price_data.columns, pd.MultiIndex):
            raise ValueError("price_data must have MultiIndex columns")

        signals = pd.DataFrame(index=self.price_data.index)

        close_columns = self.price_data.xs("close", level="ohlcv", axis=1)

        for pair in close_columns.columns:
            try:
                high = self.price_data[(pair, "high")]
                low = self.price_data[(pair, "low")]
                close = self.price_data[(pair, "close")]
                volume = self.price_data[(pair, "volume")]

                vwap = ta.volume.VolumeWeightedAveragePrice(
                    high=high,
                    low=low,
                    close=close,
                    volume=volume,
                    window=self.vwap_period,
                ).volume_weighted_average_price()

                signal = pd.Series(0, index=close.index)
                signal[close < vwap * 0.98] = 1
                signal[close > vwap] = -1

                signals[pair] = signal

            except KeyError as e:
                logger.warning(f"Missing data for {pair}: {e}")
                continue

        # Ensure the same shape/order as close prices
        signals = signals[close_columns.columns]  # exact order
        return self.normalize_signals(signals)
