import pandas as pd
import ccxt
from core.exchange import ExchangeBase
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BinanceExchange(ExchangeBase):
    def __init__(self):
        self.exchange = ccxt.binance()

    def _validate_ohlcv_data(self, df: pd.DataFrame, symbol: str) -> None:
        """Validate OHLCV data without modifying it.

        Args:
            df: DataFrame with OHLCV data.
            symbol: Trading pair symbol (e.g., 'BTC/USDT').

        Raises:
            ValueError: If data is invalid.
        """
        if df.empty:
            raise ValueError(f"No data returned for {symbol}")
        if "timestamp" not in df.columns or not pd.api.types.is_datetime64_any_dtype(
            df["timestamp"]
        ):
            raise ValueError(f"Invalid or missing timestamp column for {symbol}")

        required_columns = ["open", "high", "low", "close", "volume"]
        if not set(required_columns).issubset(df.columns):
            raise ValueError(
                f"Missing required OHLCV columns for {symbol}: {set(required_columns) - set(df.columns)}"
            )
        if df[required_columns].isnull().any().any():
            raise ValueError(f"Missing values in OHLCV data for {symbol}")

    def fetch_ohlcv(
        self, symbol: str, timeframe: str, start_date: str, end_date: str
    ) -> pd.DataFrame:
        """Fetch OHLCV data from Binance with validation.

        Args:
            symbol: Trading pair symbol ( modernist 'BTC/USDT').
            timeframe: Timeframe (e.g., '1m').
            start_date: Start date in 'YYYY-MM-DD' format.
            end_date: End date in 'YYYY-MM-DD' format.

        Returns:
            DataFrame with OHLCV data indexed by timestamp.

        Raises:
            ValueError: If data is invalid or API request fails.
            ccxt.NetworkError: If there’s a network issue.
            ccxt.ExchangeError: If there’s an exchange-specific error.
        """
        since = self.exchange.parse8601(f"{start_date}T00:00:00Z")
        until = self.exchange.parse8601(f"{end_date}T23:59:59Z")

        try:
            logger.info(
                f"Fetching OHLCV data for {symbol} from {start_date} to {end_date}"
            )
            ohlcv = self.exchange.fetch_ohlcv(
                symbol, timeframe, since=since, limit=None, params={"until": until}
            )
        except ccxt.NetworkError as e:
            logger.error(f"Network error fetching data for {symbol}: {e}")
            raise ValueError(
                f"Failed to fetch data for {symbol} due to network issue: {e}"
            )
        except ccxt.ExchangeError as e:
            logger.error(f"Exchange error fetching data for {symbol}: {e}")
            raise ValueError(
                f"Failed to fetch data for {symbol} due to exchange error: {e}"
            )
        except Exception as e:
            logger.error(f"Unexpected error fetching data for {symbol}: {e}")
            raise ValueError(f"Unexpected error fetching data for {symbol}: {e}")

        df = pd.DataFrame(
            ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
        )
        df["timestamp"] = pd.to_datetime(
            df["timestamp"], unit="ms"
        )  # Convert timestamp before validation

        self._validate_ohlcv_data(df, symbol)  # Validate after conversion

        df.set_index("timestamp", inplace=True)
        logger.info(f"Successfully fetched OHLCV data for {symbol}")
        return df

    def get_top_pairs(self, base_currency: str, limit: int) -> list[str]:
        """Return top trading pairs by volume.

        Args:
            base_currency: Base currency (e.g., 'BTC').
            limit: Number of pairs to return.

        Returns:
            List of trading pair symbols.

        Raises:
            ValueError: If not enough pairs are available.
        """
        try:
            markets = self.exchange.load_markets()
            pairs = [pair for pair in markets if pair.endswith(f"/{base_currency}")]
            if len(pairs) < limit:
                raise ValueError(
                    f"Not enough pairs available for {base_currency}: {len(pairs)} found, {limit} required"
                )
            return pairs[:limit]
        except ccxt.NetworkError as e:
            logger.error(f"Network error loading markets: {e}")
            raise ValueError(f"Failed to load markets due to network issue: {e}")
        except ccxt.ExchangeError as e:
            logger.error(f"Exchange error loading markets: {e}")
            raise ValueError(f"Failed to load markets due to exchange error: {e}")
