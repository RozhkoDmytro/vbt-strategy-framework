import pandas as pd
import vectorbt as vbt
import ta
from strategies.base import StrategyBase


class SMACrossStrategy(StrategyBase):
    def __init__(
        self, price_data: pd.DataFrame, fast_period: int = 10, slow_period: int = 30
    ):
        super().__init__(price_data)
        self.fast_period = fast_period
        self.slow_period = slow_period

    def generate_signals(self) -> pd.DataFrame:
        close_data = self.price_data["close"]
        fast_sma = ta.trend.SMAIndicator(
            close_data, window=self.fast_period
        ).sma_indicator()
        slow_sma = ta.trend.SMAIndicator(
            close_data, window=self.slow_period
        ).sma_indicator()
        entries = fast_sma > slow_sma
        exits = fast_sma < slow_sma
        signals = pd.DataFrame(index=self.price_data.index)
        signals["signal"] = 0
        signals.loc[entries, "signal"] = 1
        signals.loc[exits, "signal"] = -1
        return signals
