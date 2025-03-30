import os
import logging
from core.exchange_factory import ExchangeFactory
from core.data_loader import DataLoader
from core.backtester import Backtester
from config import config


def setup_logging():
    """Ensure logs directory exists and configure logging."""
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.FileHandler("logs/debug.log"), logging.StreamHandler()],
    )


logger = logging.getLogger(__name__)


def initialize_exchange():
    """Initialize exchange instance."""
    try:
        exchange = ExchangeFactory.get_exchange(config.exchange_name)
        logger.info(f"Initialized exchange: {config.exchange_name}")
        return exchange
    except ValueError as e:
        logger.error(f"Failed to initialize exchange: {e}")
        raise


def load_price_data(exchange):
    """Load price data from exchange."""
    data_loader = DataLoader(exchange)
    try:
        price_data = data_loader.load_data()
        first_pair = price_data.columns.get_level_values(0)[0]  # Наприклад, 'IOTA/BTC'
        price_data = price_data[first_pair]  # Отримуємо OHLCV для першої пари
        logger.info(f"Data loaded successfully for pair: {first_pair}")
        return price_data
    except ValueError as e:
        logger.error(f"Failed to load data: {e}")
        raise


def setup_directories():
    """Create required directories."""
    os.makedirs(config.results_dir, exist_ok=True)
    os.makedirs(f"{config.results_dir}/screenshots", exist_ok=True)
    logger.info("Result directories created successfully")


def run_strategy(strategy):
    """Run backtest for a single strategy and save results."""
    strategy_name = strategy.__class__.__name__
    try:
        logger.info(f"Starting backtest for {strategy_name}")
        # Передаємо лише 'close' у Backtester
        backtester = Backtester(strategy, strategy.price_data["close"])
        portfolio = backtester.run()

        logger.info(f"Backtest completed for {strategy_name}, saving results")
        backtester.save_results(portfolio, strategy_name.lower())

        logger.info(f"Results saved successfully for {strategy_name}")

    except Exception as e:
        logger.error(
            f"Error running backtest for {strategy_name}: {e}",
            exc_info=True,
        )


def main():
    """Run the backtesting framework."""
    setup_logging()
    try:
        exchange = initialize_exchange()
        price_data = load_price_data(exchange)
        setup_directories()

        # Instantiate strategies with price data (повні OHLCV для стратегій)
        strategies = [strategy(price_data) for strategy in config.strategies]

        for strategy in strategies:
            run_strategy(strategy)

    except Exception as e:
        logger.error(
            f"Backtesting framework terminated due to an error: {e}", exc_info=True
        )


if __name__ == "__main__":
    main()
