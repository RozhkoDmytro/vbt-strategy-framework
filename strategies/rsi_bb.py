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
        close_data = self.price_data["close"]
        logger.debug(f"Close data for RSI/BB: {close_data.values}")

        rsi = ta.momentum.RSIIndicator(close_data, window=self.rsi_period).rsi()
        logger.debug(f"RSI: {rsi.values}")

        bb = ta.volatility.BollingerBands(close_data, window=self.bb_period)
        lower_band = bb.bollinger_lband()
        upper_band = bb.bollinger_hband()
        logger.debug(f"Lower BB: {lower_band.values}, Upper BB: {upper_band.values}")

        entries = (rsi < 30) & (close_data < lower_band)
        exits = (rsi > 70) & (close_data > upper_band)
        logger.debug(
            f"Entries (rsi < 30 & close < lower): {entries.values}, Exits (rsi > 70 & close > upper): {exits.values}"
        )

        signals = pd.DataFrame(index=self.price_data.index)
        signals["signal"] = 0
        signals.loc[entries, "signal"] = 1
        signals.loc[exits, "signal"] = -1
        logger.debug(f"Generated signals: {signals['signal'].values}")

        return signals
