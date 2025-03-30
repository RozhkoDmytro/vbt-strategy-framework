import os
from core.data_loader import DataLoader
from core.backtester import Backtester
from core.exchange import BinanceExchange
from strategies.sma_cross import SMACrossStrategy
from strategies.rsi_bb import RSIBBStrategy
from strategies.vwap_reversion import VWAPReversionStrategy
from config import config


def get_exchange(exchange_name: str) -> BinanceExchange:
    """Initialize exchange based on config."""
    if exchange_name.lower() == "binance":
        return BinanceExchange()
    else:
        raise ValueError(f"Unsupported exchange: {exchange_name}")


def main():
    # Initialize exchange from config.exchange_name
    exchange = get_exchange(config.exchange_name)
    data_loader = DataLoader(exchange)

    # Load data with validation
    try:
        price_data = data_loader.load_data()
    except ValueError as e:
        print(f"Failed to load data: {e}")
        return

    # Define strategies
    strategies = [
        SMACrossStrategy(price_data),
        RSIBBStrategy(price_data),
        VWAPReversionStrategy(price_data),
    ]

    # Run backtests
    os.makedirs(config.results_dir, exist_ok=True)
    os.makedirs(f"{config.results_dir}/screenshots", exist_ok=True)

    for strategy in strategies:
        backtester = Backtester(strategy, price_data)
        portfolio = backtester.run()
        strategy_name = strategy.__class__.__name__.lower()
        backtester.save_results(portfolio, strategy_name)
        print(f"Results for {strategy_name} saved.")


if __name__ == "__main__":
    main()
