import pandas as pd
import ta
import logging
from strategies.base import StrategyBase

logger = logging.getLogger(__name__)


class VWAPReversionStrategy(StrategyBase):
    requires_ohlcv = True

    def __init__(self, price_data: pd.DataFrame, vwap_period: int = 20):
        super().__init__(price_data)
        self.vwap_period = vwap_period

    def generate_signals(self) -> pd.DataFrame:
        """
        Generate trading signals based on VWAP reversion.

        This method computes trading signals for each pair in the price data using
        the Volume Weighted Average Price (VWAP) indicator. An entry signal (1)
        is generated when the close price is less than 98% of the VWAP, indicating
        a potential buy opportunity. An exit signal (-1) is generated when the close
        price exceeds the VWAP, suggesting a potential sell opportunity. No signal (0)
        is assigned otherwise.

        Returns
        -------
        pd.DataFrame
            A DataFrame with the same index as the price data and a MultiIndex
            column structure, with the first level as the trading pair and the
            second level as "signal", containing the generated trading signals:
            1 for entry, -1 for exit, and 0 for hold.

        Raises
        ------
        ValueError
            If the price_data does not have MultiIndex columns.
        """

        if not isinstance(self.price_data.columns, pd.MultiIndex):
            raise ValueError("price_data must have MultiIndex columns")

        signals = pd.DataFrame(index=self.price_data.index)

        for pair in self.price_data.columns.get_level_values("pair").unique():
            try:
                high = self.price_data[(pair, "high")]
                low = self.price_data[(pair, "low")]
                close = self.price_data[(pair, "close")]
                volume = self.price_data[(pair, "volume")]

                vwap = ta.volume.VolumeWeightedAveragePrice(
                    high=high,
                    low=low,
                    close=close,
                    volume=volume,
                    window=self.vwap_period,
                ).volume_weighted_average_price()

                signal = pd.Series(0, index=close.index)
                signal[close < vwap * 0.98] = 1
                signal[close > vwap] = -1

                signals[(pair, "signal")] = signal

            except KeyError as e:
                logger.warning(f"Missing data for {pair}: {e}")
                continue

        # Ensure MultiIndex and order match price_data close
        signals.columns = pd.MultiIndex.from_tuples(
            signals.columns, names=["pair", "signal_type"]
        )
        signals = signals.sort_index(axis=1)

        return signals
