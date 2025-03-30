import pandas as pd
import vectorbt as vbt
import logging
from strategies.base import StrategyBase

logger = logging.getLogger(__name__)


class RSIBBStrategy(StrategyBase):
    def __init__(
        self,
        price_data: pd.DataFrame,
        rsi_window: int = 14,
        bb_window: int = 20,
        bb_std: float = 2.0,
    ):
        super().__init__(price_data)
        self.rsi_window = rsi_window
        self.bb_window = bb_window
        self.bb_std = bb_std

    def generate_signals(self) -> pd.DataFrame:
        close = self.price_data.xs("close", level="ohlcv", axis=1).iloc[:, 0]
        rsi = vbt.RSI.run(close, window=self.rsi_window).rsi
        bb = vbt.BBANDS.run(
            close, window=self.bb_window, std=self.bb_std, input_names=["close"]
        )

        entries = (rsi < 30) & (close < bb.lower)
        exits = (rsi > 70) & (close > bb.upper)

        logger.debug(f"RSI head:\n{rsi.head()}")
        logger.debug(f"BB Lower head:\n{bb.lower.head()}")
        logger.debug(f"BB Upper head:\n{bb.upper.head()}")
        logger.debug(f"RSI Entries: {entries.sum()}, Exits: {exits.sum()}")

        debug_df = pd.DataFrame(
            {
                "close": close,
                "rsi": rsi,
                "bb_lower": bb.lower,
                "bb_upper": bb.upper,
                "entry": entries.astype(int),
                "exit": exits.astype(int),
            }
        )
        debug_df.to_csv("logs/rsi_bb_debug.csv")

        signals = pd.DataFrame(0, index=close.index, columns=["signal"])
        signals.loc[entries, "signal"] = 1
        signals.loc[exits, "signal"] = -1

        return signals
