import os
import pandas as pd
import pyarrow.parquet as pq
from .exchange import ExchangeBase
from config import config


class DataLoader:
    def __init__(self, exchange: ExchangeBase):
        self.exchange = exchange
        self.data_path = os.path.join(config.data_dir, config.data_file)

    def _validate_data(self, df: pd.DataFrame) -> None:
        """Validate the integrity of the OHLCV data."""
        if df.empty:
            raise ValueError("Loaded data is empty")
        if not pd.api.types.is_datetime64_any_dtype(df.index):
            raise ValueError("Index must be datetime")
        if df.isnull().any().any():
            raise ValueError("Data contains missing values")
        if not all(
            col in df.columns for col in ["open", "high", "low", "close", "volume"]
        ):
            raise ValueError("Data must contain OHLCV columns")

    def load_data(self) -> pd.DataFrame:
        """Load or fetch OHLCV data for specified pairs and period."""
        if os.path.exists(self.data_path) and config.data_format == "parquet":
            print("Loading cached data...")
            df = pq.read_table(self.data_path).to_pandas()
            self._validate_data(df)
            return df

        print("Fetching data from exchange...")
        pairs = self.exchange.get_top_pairs(config.base_currency, config.num_pairs)
        data = {}
        for pair in pairs:
            try:
                df = self.exchange.fetch_ohlcv(
                    pair, config.timeframe, config.start_date, config.end_date
                )
                data[pair] = df["close"]  # Use only close price for simplicity
            except ValueError as e:
                print(f"Skipping {pair}: {e}")
                continue

        if not data:
            raise ValueError("No valid data fetched from exchange")

        combined_df = pd.concat(data, axis=1, keys=pairs)
        self._validate_data(combined_df)

        os.makedirs(config.data_dir, exist_ok=True)
        if config.data_format == "parquet":
            combined_df.to_parquet(self.data_path, compression="snappy")
        else:
            raise ValueError(f"Unsupported data format: {config.data_format}")

        return combined_df
