from abc import ABC, abstractmethod
import pandas as pd
import ccxt


class ExchangeBase(ABC):
    @abstractmethod
    def fetch_ohlcv(
        self, symbol: str, timeframe: str, start_date: str, end_date: str
    ) -> pd.DataFrame:
        """Fetch OHLCV data for a given symbol and timeframe."""
        pass

    @abstractmethod
    def get_top_pairs(self, base_currency: str, limit: int) -> list[str]:
        """Return a list of top trading pairs by liquidity."""
        pass


class BinanceExchange(ExchangeBase):
    def __init__(self):
        self.exchange = ccxt.binance()

    def fetch_ohlcv(
        self, symbol: str, timeframe: str, start_date: str, end_date: str
    ) -> pd.DataFrame:
        """Fetch OHLCV data from Binance with validation."""
        since = self.exchange.parse8601(f"{start_date}T00:00:00Z")
        until = self.exchange.parse8601(f"{end_date}T23:59:59Z")
        ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, since=since, limit=None)
        df = pd.DataFrame(
            ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
        )

        # Validation
        if df.empty:
            raise ValueError(f"No data returned for {symbol}")
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        if not pd.api.types.is_datetime64_any_dtype(df["timestamp"]):
            raise ValueError(f"Invalid timestamp format for {symbol}")
        if df[["open", "high", "low", "close", "volume"]].isnull().any().any():
            raise ValueError(f"Missing values in OHLCV data for {symbol}")

        df.set_index("timestamp", inplace=True)
        return df

    def get_top_pairs(self, base_currency: str, limit: int) -> list[str]:
        """Return top trading pairs by volume."""
        markets = self.exchange.load_markets()
        pairs = [pair for pair in markets if pair.endswith(f"/{base_currency}")]
        if len(pairs) < limit:
            raise ValueError(f"Not enough pairs available for {base_currency}")
        return pairs[:limit]
