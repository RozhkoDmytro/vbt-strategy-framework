import pandas as pd
import vectorbt as vbt
import ta
from strategies.base import StrategyBase


class RSIBBStrategy(StrategyBase):
    def __init__(
        self, price_data: pd.DataFrame, rsi_period: int = 14, bb_period: int = 20
    ):
        super().__init__(price_data)
        self.rsi_period = rsi_period
        self.bb_period = bb_period

    def generate_signals(self) -> pd.DataFrame:
        close_data = self.price_data["close"]
        rsi = ta.momentum.RSIIndicator(close_data, window=self.rsi_period).rsi()
        bb = ta.volatility.BollingerBands(close_data, window=self.bb_period)
        entries = (rsi < 30) & (close_data < bb.bollinger_lband())
        exits = (rsi > 70) & (close_data > bb.bollinger_hband())
        signals = pd.DataFrame(index=self.price_data.index)
        signals["signal"] = 0
        signals.loc[entries, "signal"] = 1
        signals.loc[exits, "signal"] = -1
        return signals
