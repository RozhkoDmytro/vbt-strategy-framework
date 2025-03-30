import pandas as pd
import vectorbt as vbt
from .base import StrategyBase


class SMACrossStrategy(StrategyBase):
    def __init__(
        self, price_data: pd.DataFrame, fast_period: int = 10, slow_period: int = 50
    ):
        super().__init__(price_data)
        self.fast_period = fast_period
        self.slow_period = slow_period

    def generate_signals(self) -> pd.DataFrame:
        """Generate signals based on SMA crossover."""
        fast_sma = vbt.MA.run(self.price_data, window=self.fast_period)
        slow_sma = vbt.MA.run(self.price_data, window=self.slow_period)
        entries = fast_sma.ma_crossed_above(slow_sma)
        exits = fast_sma.ma_crossed_below(slow_sma)
        return entries.astype(int) - exits.astype(int)
