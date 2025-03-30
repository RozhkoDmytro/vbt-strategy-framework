import pandas as pd
import vectorbt as vbt
import ta
from strategies.base import StrategyBase
import logging

logger = logging.getLogger(__name__)


class VWAPReversionStrategy(StrategyBase):
    def __init__(self, price_data: pd.DataFrame, vwap_period: int = 20):
        super().__init__(price_data)
        self.vwap_period = vwap_period

    def generate_signals(self) -> pd.DataFrame:
        signals = pd.DataFrame(index=self.price_data.index)

        # Ensure MultiIndex structure
        if not isinstance(self.price_data.columns, pd.MultiIndex):
            raise ValueError("price_data must have MultiIndex columns")

        # Iterate over available pairs
        pairs = self.price_data.columns.get_level_values("pair").unique()
        for pair in pairs:
            try:
                high = self.price_data[(pair, "high")]
                low = self.price_data[(pair, "low")]
                close = self.price_data[(pair, "close")]
                volume = self.price_data[(pair, "volume")]

                # Calculate VWAP
                vwap = ta.volume.VolumeWeightedAveragePrice(
                    high=high,
                    low=low,
                    close=close,
                    volume=volume,
                    window=self.vwap_period,
                ).volume_weighted_average_price()

                # Generate entry and exit signals
                entries = close < vwap * 0.98
                exits = close > vwap

                # Store signals
                signals[(pair, "signal")] = 0
                signals.loc[entries, (pair, "signal")] = 1
                signals.loc[exits, (pair, "signal")] = -1
            except KeyError as e:
                logger.warning(f"Missing data for {pair}: {e}")
                continue

        # Assign MultiIndex to signal columns
        signals.columns = pd.MultiIndex.from_tuples(
            signals.columns, names=["pair", "signal_type"]
        )

        return signals
