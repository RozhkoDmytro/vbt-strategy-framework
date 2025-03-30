import pandas as pd
import vectorbt as vbt
import logging
from strategies.base import StrategyBase

logger = logging.getLogger(__name__)


class SMACrossStrategy(StrategyBase):
    def __init__(
        self, price_data: pd.DataFrame, fast_window: int = 10, slow_window: int = 30
    ):
        super().__init__(price_data)
        self.fast_window = fast_window
        self.slow_window = slow_window

    def generate_signals(self) -> pd.DataFrame:
        close = self.price_data.xs("close", level="ohlcv", axis=1).iloc[:, 0]

        fast_sma = vbt.MA.run(close, window=self.fast_window).ma
        slow_sma = vbt.MA.run(close, window=self.slow_window).ma

        entries = fast_sma > slow_sma
        exits = fast_sma < slow_sma

        logger.debug(f"SMA Cross | Close head:\n{close.head()}")
        logger.debug(f"Fast SMA head:\n{fast_sma.head()}")
        logger.debug(f"Slow SMA head:\n{slow_sma.head()}")
        logger.debug(f"Entries sum: {entries.sum()}, Exits sum: {exits.sum()}")

        debug_df = pd.DataFrame(
            {
                "close": close,
                "fast_sma": fast_sma,
                "slow_sma": slow_sma,
                "entry": entries.astype(int),
                "exit": exits.astype(int),
            }
        )
        debug_df.to_csv("logs/sma_debug.csv")

        signals = pd.DataFrame(0, index=close.index, columns=["signal"])
        signals.loc[entries, "signal"] = 1
        signals.loc[exits, "signal"] = -1

        return signals
