import vectorbt as vbt
import pandas as pd
from config import config
from ..strategies.base import StrategyBase


class Backtester:
    def __init__(self, strategy: StrategyBase, price_data: pd.DataFrame):
        self.strategy = strategy
        self.price_data = price_data

    def run(self) -> vbt.Portfolio:
        """Run backtest for the given strategy."""
        signals = self.strategy.generate_signals()
        entries = signals == 1
        exits = signals == -1
        portfolio = vbt.Portfolio.from_signals(
            close=self.price_data,
            entries=entries,
            exits=exits,
            fees=config.commission,
            slippage=config.slippage,
            freq=config.timeframe,
        )
        return portfolio

    def save_results(self, portfolio: vbt.Portfolio, strategy_name: str):
        """Save backtest results."""
        metrics = self.strategy.get_metrics(portfolio)
        metrics_df = pd.DataFrame([metrics])
        metrics_df.to_csv(
            f"{config.results_dir}/{strategy_name}_metrics.csv", index=False
        )

        equity = portfolio.value()
        equity.plot(title=f"{strategy_name} Equity Curve").write_image(
            f"{config.results_dir}/screenshots/{strategy_name}_equity.png"
        )
