import pandas as pd
import vectorbt as vbt
import ta
import logging
from strategies.base import StrategyBase

logger = logging.getLogger(__name__)


class SMACrossStrategy(StrategyBase):
    def __init__(
        self, price_data: pd.DataFrame, fast_period: int = 10, slow_period: int = 30
    ):
        super().__init__(price_data)
        self.fast_period = fast_period
        self.slow_period = slow_period

    def generate_signals(self) -> pd.DataFrame:
        signals = pd.DataFrame(
            index=self.price_data.index, columns=self.price_data.columns, data=0
        )

        for symbol in self.price_data.columns:
            close = self.price_data[symbol]
            logger.debug(f"Processing {symbol}")

            fast_sma = ta.trend.SMAIndicator(
                close, window=self.fast_period
            ).sma_indicator()
            slow_sma = ta.trend.SMAIndicator(
                close, window=self.slow_period
            ).sma_indicator()

            entries = fast_sma > slow_sma
            exits = fast_sma < slow_sma

            signals.loc[entries, symbol] = 1
            signals.loc[exits, symbol] = -1

        logger.debug(f"Generated SMA signals:\n{signals}")
        return signals
