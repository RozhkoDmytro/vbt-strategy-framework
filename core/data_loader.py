import os
import pandas as pd
import pyarrow.parquet as pq
import logging
from core.exchange import ExchangeBase
from config import config
import numpy as np


# Configure logger
logger = logging.getLogger(__name__)


class DataLoader:
    def __init__(self, exchange: ExchangeBase):
        self.exchange = exchange
        self.data_path = os.path.join(config.data_dir, config.data_file)

    def _validate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate the integrity of the OHLCV data."""
        required_cols = {"open", "high", "low", "close", "volume"}

        # Remove infinite values and replace with NaN
        df.replace([np.inf, -np.inf], np.nan, inplace=True)

        # Drop rows with NaN values
        df.dropna(inplace=True)

        # Ensure all prices and volumes are greater than 0
        df = df[(df > 0).all(axis=1)]

        # Check if dataframe is empty
        if df.empty:
            raise ValueError("Loaded data is empty")

        # Check if index is datetime
        if not pd.api.types.is_datetime64_any_dtype(df.index):
            raise ValueError("Index must be datetime")

        # Check for any missing values
        if df.isnull().any().any():
            raise ValueError("Data contains missing values")

        # Handle validation for MultiIndex columns
        if isinstance(df.columns, pd.MultiIndex):
            # Get the unique column names from the second level (OHLCV)
            cols = set(df.columns.get_level_values(1))
        else:
            cols = set(df.columns)

        # Check if all required OHLCV columns are present
        if not required_cols.issubset(cols):
            missing_cols = required_cols - cols
            available_cols = ", ".join(map(str, df.columns.tolist()))
            raise ValueError(
                f"Data must contain all OHLCV columns: {', '.join(missing_cols)}"
                f"\nAvailable columns: {available_cols}"
            )
        return df

    def load_data(self) -> pd.DataFrame:
        """Load or fetch OHLCV data for specified pairs and period."""
        if os.path.exists(self.data_path) and config.data_format == "parquet":
            logger.info(f"Loading cached data from {self.data_path}")
            df = pq.read_table(self.data_path).to_pandas()
            self._validate_data(df)
            return df

        logger.info(f"Fetching data from exchange to save at {self.data_path}")
        pairs = self.exchange.get_top_pairs(config.base_currency, config.num_pairs)
        data = {}
        for pair in pairs:
            try:
                df = self.exchange.fetch_ohlcv(
                    pair, config.timeframe, config.start_date, config.end_date
                )
                data[pair] = df
            except ValueError as e:
                logger.warning(f"Skipping {pair}: {e}")
                continue

        if not data:
            raise ValueError("No valid data fetched from exchange")

        # Use only keys from data for pd.concat

        combined_df = pd.concat(
            data.values(), axis=1, keys=data.keys(), names=["pair", "ohlcv"]
        )

        combined_df = self._validate_data(combined_df)

        os.makedirs(config.data_dir, exist_ok=True)
        if config.data_format == "parquet":
            combined_df.to_parquet(self.data_path, compression="snappy")
            logger.info(f"Data saved to {self.data_path}")
        else:
            raise ValueError(f"Unsupported data format: {config.data_format}")

        return combined_df
