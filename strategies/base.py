from abc import ABC, abstractmethod
import pandas as pd
import vectorbt as vbt
from core.metrics import calculate_metrics


class StrategyBase(ABC):
    requires_ohlcv: bool = False

    def __init__(self, price_data: pd.DataFrame):
        self.price_data = price_data

    @abstractmethod
    def generate_signals(self) -> pd.DataFrame:
        """Generate trading signals: 1 for entry, -1 for exit, 0 for hold."""
        pass

    def run_backtest(self) -> vbt.Portfolio:
        """Run backtest using VectorBT."""
        from ..core.backtester import Backtester

        backtester = Backtester(self, self.price_data)
        return backtester.run()

    def get_metrics(self, portfolio: vbt.Portfolio) -> dict:
        """Return backtest metrics."""
        return calculate_metrics(portfolio)

    def normalize_signals(self, signals: pd.DataFrame) -> pd.DataFrame:
        """
        Normalize signal structure to match the 'close' price frame exactly.
        """
        close = self.price_data.xs("close", level="ohlcv", axis=1)

        # Step 1: Ensure signals is a DataFrame with correct shape
        if isinstance(signals, pd.Series):
            signals = signals.to_frame()
        signals = signals.copy()

        # Step 2: Force reindex to close.index (DatetimeIndex) and columns (MultiIndex)
        signals = signals.reindex(
            index=close.index, columns=close.columns, fill_value=0
        )

        # Step 3: Ensure dtypes are numeric (int8 is optimal for signals)
        signals = signals.astype("int8")

        return signals

    def get_close_price(self) -> pd.DataFrame:
        """
        Extract close prices from self.price_data safely.
        """
        if not isinstance(self.price_data.columns, pd.MultiIndex):
            raise TypeError("price_data must have MultiIndex columns")

        return self.price_data.xs("close", level="ohlcv", axis=1)
