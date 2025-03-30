import logging
from utils.utils import (
    setup_logging,
    initialize_exchange,
    load_price_data,
    setup_directories,
)
from core.backtester import run_strategy
from config import config

logger = logging.getLogger(__name__)


def main():
    """Run the backtesting framework."""
    setup_logging()
    try:
        exchange = initialize_exchange()
        price_data = load_price_data(exchange)
        setup_directories()

        # Instantiate strategies with price data (full OHLCV for strategies)
        strategies = []
        for strategy_cls in config.strategies:
            if getattr(strategy_cls, "requires_ohlcv", False):
                strategies.append(strategy_cls(price_data))  # Full OHLCV
            else:
                close_data = price_data.xs("close", level="ohlcv", axis=1)
                strategies.append(strategy_cls(close_data))  # Only close

        for strategy in strategies:
            run_strategy(strategy)

    except Exception as e:
        logger.error(
            f"Backtesting framework terminated due to an error: {e}", exc_info=True
        )


if __name__ == "__main__":
    main()
