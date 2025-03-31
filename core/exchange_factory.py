from .exchange import ExchangeBase
from config import config


class ExchangeFactory:
    """Factory for creating exchange strategies."""

    @staticmethod
    def get_exchange(exchange_name: str) -> ExchangeBase:
        """Create an exchange strategy based on name.

        Args:
            exchange_name: Name of the exchange (e.g., 'binance').

        Returns:
            An instance of ExchangeBase subclass.

        Raises:
            ValueError: If the exchange is not supported.
        """
        exchange_class = config.supported_exchanges.get(exchange_name.lower())
        if exchange_class is None:
            raise ValueError(
                f"Unsupported exchange: {exchange_name}. Supported exchanges: {list(config.supported_exchanges.keys())}"
            )
        return exchange_class()
