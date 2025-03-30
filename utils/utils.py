import os
import logging
from config import config


def setup_logging():
    """Ensure logs directory exists and configure logging."""
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.FileHandler("logs/debug.log"), logging.StreamHandler()],
    )


def initialize_exchange():
    """Initialize exchange instance."""
    from core.exchange_factory import ExchangeFactory

    try:
        exchange = ExchangeFactory.get_exchange(config.exchange_name)
        logging.info(f"Initialized exchange: {config.exchange_name}")
        return exchange
    except ValueError as e:
        logging.error(f"Failed to initialize exchange: {e}")
        raise


def load_price_data(exchange):
    """Load price data from exchange."""
    from core.data_loader import DataLoader

    data_loader = DataLoader(exchange)
    try:
        price_data = data_loader.load_data()
        logging.info(f"Data loaded successfully: {price_data.shape[1]} symbols")
        return price_data
    except ValueError as e:
        logging.error(f"Failed to load data: {e}")
        raise


def setup_directories():
    """Create required directories."""
    os.makedirs(config.results_dir, exist_ok=True)
    os.makedirs(f"{config.results_dir}/screenshots", exist_ok=True)
    logging.info("Result directories created successfully")
