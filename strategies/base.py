from abc import ABC, abstractmethod
import pandas as pd
import vectorbt as vbt
from ..core.metrics import calculate_metrics


class StrategyBase(ABC):
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
