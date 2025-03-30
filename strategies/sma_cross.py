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
        close_data = self.price_data["close"]
        logger.debug(f"Close data for SMA: {close_data.values}")

        fast_sma = ta.trend.SMAIndicator(
            close_data, window=self.fast_period
        ).sma_indicator()
        slow_sma = ta.trend.SMAIndicator(
            close_data, window=self.slow_period
        ).sma_indicator()
        logger.debug(f"Fast SMA: {fast_sma.values}, Slow SMA: {slow_sma.values}")

        entries = fast_sma > slow_sma
        exits = fast_sma < slow_sma
        logger.debug(
            f"Entries (fast_sma > slow_sma): {entries.values}, Exits (fast_sma < slow_sma): {exits.values}"
        )

        signals = pd.DataFrame(index=self.price_data.index)
        signals["signal"] = 0
        signals.loc[entries, "signal"] = 1
        signals.loc[exits, "signal"] = -1
        logger.debug(f"Generated signals: {signals['signal'].values}")

        return signals
