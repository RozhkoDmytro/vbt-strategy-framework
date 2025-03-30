import vectorbt as vbt
import pandas as pd
from config import config
from strategies.base import StrategyBase
import matplotlib.pyplot as plt
import os
import logging

logger = logging.getLogger(__name__)


class Backtester:
    def __init__(self, strategy: StrategyBase, price_data: pd.DataFrame):
        self.strategy = strategy
        self.price_data = price_data

    def run(self) -> vbt.Portfolio:
        """Run backtest for the given strategy."""
        signals = self.strategy.generate_signals()
        entries = signals == 1
        exits = signals == -1
        close_prices = self.price_data.xs("close", level="ohlcv", axis=1)
        portfolio = vbt.Portfolio.from_signals(
            close=close_prices,
            entries=entries,
            exits=exits,
            fees=config.commission,
            slippage=config.slippage,
            freq=config.timeframe,
        )
        return portfolio

    def save_results(self, portfolio: vbt.Portfolio, strategy_name: str):
        """Save backtest results and metrics."""
        logger.info("Attempting to save results...")

        # Ensure directories exist
        os.makedirs(f"{config.results_dir}/screenshots", exist_ok=True)

        # Save metrics CSV
        metrics = self.strategy.get_metrics(portfolio)
        metrics_df = pd.DataFrame([metrics])
        metrics_df.to_csv(
            f"{config.results_dir}/{strategy_name}_metrics.csv", index=False
        )
        logger.info("Metrics CSV saved successfully.")

        # Save equity curve using matplotlib
        equity = portfolio.value()
        plt.figure(figsize=(10, 5))
        plt.plot(equity.index, equity, label="Equity Curve")
        plt.title(f"{strategy_name} Equity Curve")
        plt.xlabel("Date")
        plt.ylabel("Portfolio Value")
        plt.grid(True)
        plt.legend()

        plt.savefig(f"{config.results_dir}/screenshots/{strategy_name}_equity.png")
        plt.close()

        logger.info("PNG saved successfully using matplotlib.")
