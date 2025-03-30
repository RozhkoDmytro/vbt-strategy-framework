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
        """
        Initialize the SMACrossStrategy.

        Parameters
        ----------
        price_data : pd.DataFrame
            The price data for all symbols.
        fast_period : int, optional
            The period for the fast moving average. Defaults to 10.
        slow_period : int, optional
            The period for the slow moving average. Defaults to 30.
        """
        super().__init__(price_data)
        self.fast_period = fast_period
        self.slow_period = slow_period

    def generate_signals(self) -> pd.DataFrame:
        """
        Generate trading signals based on a moving average crossover.

        This method calculates trading signals for each symbol in the price data
        using the Simple Moving Average (SMA) indicator. A buy signal (1) is
        generated when the fast SMA crosses above the slow SMA, and a sell signal
        (-1) is generated when the fast SMA crosses below the slow SMA. No signal
        (0) is assigned otherwise.

        Returns
        -------
        pd.DataFrame
            A DataFrame with the same index and columns as the price data,
            containing the generated trading signals: 1 for buy, -1 for sell, and
            0 for hold.
        """
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
