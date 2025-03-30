import pandas as pd
import vectorbt as vbt
from .base import StrategyBase


class RSIBBStrategy(StrategyBase):
    def __init__(
        self, price_data: pd.DataFrame, rsi_period: int = 14, bb_period: int = 20
    ):
        super().__init__(price_data)
        self.rsi_period = rsi_period
        self.bb_period = bb_period

    def generate_signals(self) -> pd.DataFrame:
        """Generate signals based on RSI and Bollinger Bands."""
        rsi = vbt.RSI.run(self.price_data, window=self.rsi_period)
        bb = vbt.BBANDS.run(self.price_data, window=self.bb_period)
        entries = (rsi.rsi < 30) & (self.price_data > bb.lower)
        exits = rsi.rsi > 70
        return entries.astype(int) - exits.astype(int)
