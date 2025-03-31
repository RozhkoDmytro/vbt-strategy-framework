from abc import ABC, abstractmethod
import pandas as pd


class ExchangeBase(ABC):
    @abstractmethod
    def fetch_ohlcv(
        self, symbol: str, timeframe: str, start_date: str, end_date: str
    ) -> pd.DataFrame:
        """Fetch OHLCV data for a given symbol and timeframe."""
        pass

    @abstractmethod
    def fetch_full_ohlcv(
        self, symbol: str, timeframe: str, start_date: str, end_date: str
    ) -> pd.DataFrame:
        """Fetch complete OHLCV data using time-based pagination."""
        pass

    @abstractmethod
    def get_top_pairs(self, base_currency: str, limit: int) -> list[str]:
        """Return a list of top trading pairs by liquidity."""
        pass
