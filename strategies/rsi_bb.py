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
        """
        Initialize the RSI-BB strategy.

        Parameters
        ----------
        price_data : pd.DataFrame
            The price data for all symbols.
        rsi_period : int, optional
            The period for the RSI indicator. Defaults to 14.
        bb_period : int, optional
            The period for the Bollinger Bands indicator. Defaults to 20.
        """
        super().__init__(price_data)
        self.rsi_period = rsi_period
        self.bb_period = bb_period

    def generate_signals(self) -> pd.DataFrame:
        """
        Generate trading signals based on RSI and Bollinger Bands.

        This method calculates trading signals for each symbol in the price data using
        the Relative Strength Index (RSI) and Bollinger Bands indicators. A buy signal
        (1) is generated when the RSI is below 30 and the price is below the lower
        Bollinger Band, indicating a potential entry point. A sell signal (-1) is
        generated when the RSI is above 70 and the price is above the upper Bollinger
        Band, suggesting a potential exit point. No signal (0) is assigned otherwise.

        Returns
        -------
        pd.DataFrame
            A DataFrame with the same index and columns as the price data, containing
            the generated trading signals: 1 for buy, -1 for sell, and 0 for hold.
        """
        close_df = self.get_close_price()
        signals = pd.DataFrame(index=close_df.index, columns=close_df.columns, data=0)

        for symbol in close_df.columns:
            close = close_df[symbol]
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
        signals = self.normalize_signals(signals)
        return signals
