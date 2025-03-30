import pandas as pd
import ccxt
from core.exchange import ExchangeBase
import logging

logger = logging.getLogger(__name__)


class BinanceExchange(ExchangeBase):
    def __init__(self):
        self.exchange = ccxt.binance()

    def _validate_ohlcv_data(self, df: pd.DataFrame, symbol: str) -> None:
        """
        Validate that the given OHLCV data is not empty and contains all required columns with no missing values.

        Args:
            df (pd.DataFrame): The OHLCV data to validate.
            symbol (str): The symbol of the data, used for error messages.

        Raises:
            ValueError: If the data is invalid or missing required columns or values.
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
        """
        Fetches OHLCV data for a given symbol and timeframe from Binance.

        Args:
            symbol (str): The symbol of the data to fetch (e.g., "BTC/USDT").
            timeframe (str): The timeframe of the data to fetch (e.g., "1m").
            start_date (str): The start date of the data to fetch in "YYYY-MM-DD" format.
            end_date (str): The end date of the data to fetch in "YYYY-MM-DD" format.

        Returns:
            pd.DataFrame: A DataFrame containing the OHLCV data with a DatetimeIndex.

        Raises:
            ValueError: If no data is returned for the given symbol or if the data is invalid.
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
            if not ohlcv:  # Перевірка на порожній список
                raise ValueError(f"No data returned for {symbol}")
            df = pd.DataFrame(
                ohlcv, columns=["timestamp", "open", "high", "low", "close", "volume"]
            )
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            self._validate_ohlcv_data(df, symbol)
            df.set_index("timestamp", inplace=True)
            logger.info(f"Successfully fetched OHLCV data for {symbol}")
            return df
        except (ccxt.NetworkError, ccxt.ExchangeError, ValueError) as e:
            logger.error(f"Error fetching data for {symbol}: {e}")
            raise ValueError(f"Failed to fetch data for {symbol}: {e}")

    def get_top_pairs(self, base_currency: str, limit: int) -> list[str]:
        """
        Return a list of top trading pairs by liquidity for a given base currency.

        Args:
            base_currency (str): The base currency of the pairs to fetch (e.g., "BTC").
            limit (int): The number of pairs to return.

        Returns:
            list[str]: A list of top trading pairs in the format "SYM/USDT".

        Raises:
            ValueError: If no active pairs are available for the given base currency.
            ValueError: If there is an issue loading markets from the exchange.
        """
        try:
            markets = self.exchange.load_markets()
            # Фільтруємо лише активні пари з базовою валютою
            pairs = [
                pair
                for pair in markets
                if pair.endswith(f"/{base_currency}") and markets[pair]["active"]
            ]
            if not pairs:
                raise ValueError(f"No active pairs available for {base_currency}")
            # Сортуємо за обсягом (якщо API підтримує), але тут просто беремо перші limit пар
            return pairs[:limit]
        except ccxt.NetworkError as e:
            logger.error(f"Network error loading markets: {e}")
            raise ValueError(f"Failed to load markets due to network issue: {e}")
        except ccxt.ExchangeError as e:
            logger.error(f"Exchange error loading markets: {e}")
            raise ValueError(f"Failed to load markets due to exchange error: {e}")
