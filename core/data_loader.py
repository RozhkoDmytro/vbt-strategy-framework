import os
import pandas as pd
import numpy as np
import pyarrow.parquet as pq
import logging
from core.exchange import ExchangeBase
from config import config

logger = logging.getLogger(__name__)


class DataLoader:
    def __init__(self, exchange: ExchangeBase):
        self.exchange = exchange
        self.data_path = os.path.join(config.data_dir, config.data_file)

    def _replace_infinite_values(self, df: pd.DataFrame) -> pd.DataFrame:
        n_inf_before = np.isinf(df.values).sum()
        df.replace([np.inf, -np.inf], np.nan, inplace=True)
        logger.debug(f"[VALIDATION] Replaced {n_inf_before} inf values with NaN")
        return df

    def _fill_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        n_nan_before = df.isna().sum().sum()
        logger.debug(f"[VALIDATION] NaNs before filling: {n_nan_before}")

        df.ffill(inplace=True)
        df.bfill(inplace=True)

        n_nan_after = df.isna().sum().sum()
        logger.debug(f"[VALIDATION] NaNs after filling: {n_nan_after}")
        return df

    def _filter_negative_close(self, df: pd.DataFrame) -> pd.DataFrame:
        before_filtering = df.shape[0]

        if isinstance(df.columns, pd.MultiIndex) and "ohlcv" in df.columns.names:
            close_cols = df.xs("close", level="ohlcv", axis=1)
            df = df[(close_cols >= 0).all(axis=1)]
        elif "close" in df.columns:
            df = df[df["close"] >= 0]

        after_filtering = df.shape[0]
        logger.debug(
            f"[VALIDATION] Rows removed by positive-value filter: {before_filtering - after_filtering}"
        )
        return df

    def _final_checks(self, df: pd.DataFrame):
        if df.empty:
            raise ValueError("Loaded data is empty after filtering")
        if not pd.api.types.is_datetime64_any_dtype(df.index):
            raise ValueError("Index must be datetime")
        if df.isnull().any().any():
            raise ValueError("Data contains remaining missing values")
        if not isinstance(df.columns, pd.MultiIndex):
            raise ValueError("Data must have MultiIndex columns")
        if df.columns.names != ["pair", "ohlcv"]:
            raise ValueError(f"Incorrect MultiIndex column names: {df.columns.names}")

        required_cols = {"open", "high", "low", "close", "volume"}
        cols = set(df.columns.get_level_values(1))
        if not required_cols.issubset(cols):
            missing_cols = required_cols - cols
            raise ValueError(f"Missing OHLCV columns: {', '.join(missing_cols)}")

    def _validate_data(self, df: pd.DataFrame) -> pd.DataFrame:
        logger.info(f"[VALIDATION] Initial shape: {df.shape}")

        df = self._replace_infinite_values(df)
        df = self._fill_missing_values(df)
        df = self._filter_negative_close(df)

        logger.info(f"[VALIDATION] Shape after filtering: {df.shape}")

        self._final_checks(df)
        logger.info(f"[VALIDATION] Final shape after validation: {df.shape}")

        return df

    def load_data(self) -> pd.DataFrame:
        if os.path.exists(self.data_path) and config.data_format == "parquet":
            logger.info(f"Loading cached data from {self.data_path}")
            df = pq.read_table(self.data_path).to_pandas()
            df = self._validate_data(df)
            return df

        logger.info(f"Fetching data from exchange to save at {self.data_path}")
        pairs = self.exchange.get_top_pairs(config.base_currency, config.num_pairs)
        logger.info(f"Fetching data for {len(pairs)} pairs: {pairs}")

        data = {}
        for pair in pairs:
            try:
                df = self.exchange.fetch_ohlcv(
                    pair, config.timeframe, config.start_date, config.end_date
                )
                df.columns = pd.MultiIndex.from_product(
                    [[pair], df.columns], names=["pair", "ohlcv"]
                )
                data[pair] = df
                logger.debug(f"Fetched {pair} with shape {df.shape}")
            except ValueError as e:
                logger.warning(f"Skipping {pair}: {e}")
                continue

        if not data:
            raise ValueError("No valid data fetched from exchange")

        combined_df = pd.concat(data.values(), axis=1)
        logger.info(f"Combined data shape before validation: {combined_df.shape}")
        combined_df = self._validate_data(combined_df)

        os.makedirs(config.data_dir, exist_ok=True)
        if config.data_format == "parquet":
            combined_df.to_parquet(self.data_path, compression="snappy")
            logger.info(f"Data saved to {self.data_path}")

        return combined_df
