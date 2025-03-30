import pandas as pd
import vectorbt as vbt
from .base import StrategyBase


class VWAPReversionStrategy(StrategyBase):
    def __init__(self, price_data: pd.DataFrame):
        super().__init__(price_data)

    def generate_signals(self) -> pd.DataFrame:
        """Generate signals based on VWAP reversion."""
        vwap = vbt.VWAP.run(
            self.price_data, self.price_data
        )  # Volume assumed same as close for simplicity
        entries = self.price_data < vwap.vwap * 0.98  # 2% below VWAP
        exits = self.price_data > vwap.vwap
        return entries.astype(int) - exits.astype(int)
