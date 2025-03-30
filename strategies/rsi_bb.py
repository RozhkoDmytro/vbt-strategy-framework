import pandas as pd
import vectorbt as vbt
from strategies.base import StrategyBase


class RSIBBStrategy(StrategyBase):
    def __init__(
        self, price_data: pd.DataFrame, rsi_period: int = 14, bb_period: int = 20
    ):
        super().__init__(price_data)
        self.rsi_period = rsi_period
        self.bb_period = bb_period

    def generate_signals(self) -> pd.DataFrame:
        """Generate signals based on RSI and Bollinger Bands."""

        close = self.price_data.xs("close", level="ohlcv", axis=1).iloc[:, 0]

        bb_indicator = vbt.BBANDS.run(close)
        rsi_indicator = vbt.RSI.run(close)

        entries = (rsi_indicator.rsi < 30) & (close < bb_indicator.lower)
        exits = (rsi_indicator.rsi > 70) | (close > bb_indicator.upper)

        signals = pd.DataFrame(0, index=close.index, columns=["signal"])
        signals.loc[entries, "signal"] = 1
        signals.loc[exits, "signal"] = -1

        return entries.astype(int) - exits.astype(int)
