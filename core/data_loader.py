import os
import pandas as pd
import logging
import numpy as np
from config import config
from core.exchange import ExchangeBase

# Configure logger
logger = logging.getLogger(__name__)


class DataLoader:
    def __init__(self, exchange: ExchangeBase):
        self.exchange = exchange
        self.data_path = os.path.join(config.data_dir, config.data_file)

    def _validate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate the integrity of the OHLCV data."""
        required_cols = {"open", "high", "low", "close", "volume"}

        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        df.dropna(inplace=True)
        df = df[(df.select_dtypes(include=[np.number]) > 0).all(axis=1)]

        if df.empty:
            raise ValueError("Loaded data is empty")

        if not pd.api.types.is_datetime64_any_dtype(df.index):
            raise ValueError("Index must be datetime")

        if df.isnull().any().any():
            raise ValueError("Data contains missing values")

        if not isinstance(df.columns, pd.MultiIndex):
            raise ValueError(
                "Data must have MultiIndex columns with levels ['pair', 'ohlcv']"
            )

        if df.columns.names != ["pair", "ohlcv"]:
            raise ValueError(
                f"Incorrect MultiIndex column names: {df.columns.names}, expected ['pair', 'ohlcv']"
            )

        cols = set(df.columns.get_level_values(1))
        if not required_cols.issubset(cols):
            missing_cols = required_cols - cols
            raise ValueError(f"Missing OHLCV columns: {', '.join(missing_cols)}")

        logger.info("Data validation passed. Shape: %s", df.shape)
        return df

    def load_data(self) -> pd.DataFrame:
        """Load or fetch OHLCV data for specified pairs and period."""
        if os.path.exists(self.data_path) and config.data_format == "parquet":
            logger.info(f"Loading cached data from {self.data_path}")
            df = pd.read_parquet(self.data_path)

            if not isinstance(df.columns, pd.MultiIndex):
                df.columns = pd.MultiIndex.from_tuples(df.columns)
            if df.columns.names != ["pair", "ohlcv"]:
                df.columns.set_names(["pair", "ohlcv"], inplace=True)

            logger.debug("Loaded data columns: %s", df.columns)
            logger.debug("Loaded data index type: %s", df.index.dtype)

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
                logger.info(f"Fetched {pair} with shape {df.shape}")
            except ValueError as e:
                logger.warning(f"Skipping {pair}: {e}")
                continue

        if not data:
            raise ValueError("No valid data fetched from exchange")

        combined_df = pd.concat(data.values(), axis=1, keys=data.keys())
        combined_df.columns = pd.MultiIndex.from_tuples(
            combined_df.columns, names=["pair", "ohlcv"]
        )

        logger.debug("Combined DataFrame head:\n%s", combined_df.head())

        combined_df = self._validate_data(combined_df)

        os.makedirs(config.data_dir, exist_ok=True)
        if config.data_format == "parquet":
            combined_df.to_parquet(self.data_path, compression="snappy")
            logger.info(f"Data saved to {self.data_path}")

        csv_path = os.path.splitext(self.data_path)[0] + ".csv"
        flat_df = combined_df.copy()
        flat_df.columns = ["_".join(col) for col in flat_df.columns.to_flat_index()]
        flat_df.to_csv(csv_path)
        logger.info(f"Flattened data saved to {csv_path} for external analysis")

        return combined_df
