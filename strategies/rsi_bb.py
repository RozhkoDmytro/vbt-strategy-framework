import pandas as pd
import vectorbt as vbt
import ta
import logging
from strategies.base import StrategyBase

logger = logging.getLogger(__name__)


class RSIBBStrategy(StrategyBase):
    def __init__(
        self, price_data: pd.DataFrame, rsi_period: int = 14, bb_period: int = 20
    ):
        super().__init__(price_data)
        self.rsi_period = rsi_period
        self.bb_period = bb_period

    def generate_signals(self) -> pd.DataFrame:
        signals = pd.DataFrame(
            index=self.price_data.index, columns=self.price_data.columns, data=0
        )

        for symbol in self.price_data.columns:
            close = self.price_data[symbol]
            logger.debug(f"Processing {symbol}")

            rsi = ta.momentum.RSIIndicator(close, window=self.rsi_period).rsi()
            bb = ta.volatility.BollingerBands(close, window=self.bb_period)
            lower_band = bb.bollinger_lband()
            upper_band = bb.bollinger_hband()

            entries = (rsi < 30) & (close < lower_band)
            exits = (rsi > 70) & (close > upper_band)

            signals.loc[entries, symbol] = 1
            signals.loc[exits, symbol] = -1

        logger.debug(f"Generated signals:\n{signals}")
        return signals
