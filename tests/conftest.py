import pytest
import pandas as pd
import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def mock_price_data_no_signals():
    """
    A fixture that returns a DataFrame with sample price data for testing
    trading strategies. The data is constant and does not generate any
    trading signals.
    """
    data = {
        ("TEST/BTC", "open"): [100.0, 100.0, 100.0, 100.0, 100.0],
        ("TEST/BTC", "high"): [100.5, 100.5, 100.5, 100.5, 100.5],
        ("TEST/BTC", "low"): [99.5, 99.5, 99.5, 99.5, 99.5],
        ("TEST/BTC", "close"): [100.0, 100.0, 100.0, 100.0, 100.0],
        ("TEST/BTC", "volume"): [100, 150, 200, 120, 180],
    }
    index = pd.date_range("2025-01-01", periods=5, freq="1min")
    df = pd.DataFrame(data, index=index)
    df.columns.names = ["pair", "ohlcv"]
    return df


@pytest.fixture
def mock_price_data_entry_exit():
    """
    A fixture that returns a DataFrame with sample price data
    that simulates entering and exiting trading signals.

    The data includes open, high, low, close prices, and volume
    for the trading pair "TEST/BTC" over a period of 5 minutes.

    The DataFrame's index is a date range starting from "2025-01-01"
    with a frequency of 1 minute.
    """

    data = {
        ("TEST/BTC", "open"): [100.0, 101.0, 102.0, 99.0, 98.0],
        ("TEST/BTC", "high"): [100.5, 101.5, 102.5, 99.5, 98.5],
        ("TEST/BTC", "low"): [99.5, 100.5, 101.5, 98.5, 97.5],
        ("TEST/BTC", "close"): [100.0, 101.0, 102.0, 99.0, 98.0],
        ("TEST/BTC", "volume"): [100, 150, 200, 120, 180],
    }
    index = pd.date_range("2025-01-01", periods=5, freq="1min")
    df = pd.DataFrame(data, index=index)
    df.columns.names = ["pair", "ohlcv"]
    return df


@pytest.fixture
def mock_vwap_price_data_no_signals():
    """Mock price data without any VWAP entry/exit signals."""
    index = pd.date_range("2025-01-01", periods=5, freq="1min")
    columns = pd.MultiIndex.from_product(
        [["TEST/BTC"], ["open", "high", "low", "close", "volume"]],
        names=["pair", "ohlcv"],
    )
    data = [
        [100.0, 100.5, 99.5, 100.0, 100],
        [100.5, 101.0, 100.0, 100.5, 150],
        [101.0, 101.5, 100.5, 101.0, 200],
        [100.5, 101.0, 100.0, 100.5, 120],
        [100.0, 100.5, 99.5, 100.0, 180],
    ]
    return pd.DataFrame(data, columns=columns, index=index)


@pytest.fixture
def mock_vwap_price_data_entry_exit():
    data = {
        ("TEST/BTC", "open"): [100, 100, 96, 106, 100],
        ("TEST/BTC", "high"): [101, 101, 97, 107, 101],
        ("TEST/BTC", "low"): [99, 99, 95, 105, 99],
        ("TEST/BTC", "close"): [100, 100, 96, 106, 100],  # 96 < VWAP * 0.98, 106 > VWAP
        ("TEST/BTC", "volume"): [100, 100, 200, 200, 100],
    }
    index = pd.date_range("2025-01-01", periods=5, freq="1min")
    df = pd.DataFrame(data, index=index)
    df.columns.names = ["pair", "ohlcv"]
    return df


@pytest.fixture
def mock_price_data2():
    """
    A fixture that returns a DataFrame with sample price data for testing
    trading strategies. The data includes open, high, low, close prices,
    and volume for the trading pair "TEST/BTC" over a period of 5 minutes.

    This data simulates a scenario with varying price levels, including
    a significant drop at the third minute, which can be used to test
    different trading strategy behaviors.

    The DataFrame's index is a date range starting from "2025-01-01"
    with a frequency of 1 minute.
    """

    data = {
        ("TEST/BTC", "open"): [100.0, 99.0, 20.0, 92.0, 98.0],
        ("TEST/BTC", "high"): [100.5, 99.5, 20.5, 92.5, 98.5],
        ("TEST/BTC", "low"): [99.5, 98.5, 19.5, 91.5, 97.5],
        ("TEST/BTC", "close"): [100.0, 99.0, 20.0, 92.0, 98.0],
        ("TEST/BTC", "volume"): [100, 150, 200, 120, 180],
    }
    index = pd.date_range("2025-01-01", periods=5, freq="1min")
    df = pd.DataFrame(data, index=index)
    df.columns.names = ["pair", "ohlcv"]
    return df


@pytest.fixture
def mock_price_data1():
    """
    A fixture that returns a DataFrame with sample price data for testing
    trading strategies. The data includes open, high, low, close prices,
    and volume for the trading pair "TEST/BTC" over a period of 5 minutes.

    The prices are random and the volume is also random, but within a range
    of 100 to 1000.

    The DataFrame's index is a date range starting from "2025-01-01"
    with a frequency of 1 minute.
    """
    index = pd.date_range(start="2025-01-01", periods=5, freq="1min")
    columns = pd.MultiIndex.from_product(
        [["TEST/BTC"], ["open", "high", "low", "close", "volume"]],
        names=["pair", "ohlcv"],
    )
    base_price = np.random.random(5) * 100 + 50
    spread = np.random.random(5) * 5
    df = pd.DataFrame(index=index, columns=columns)
    df[("TEST/BTC", "open")] = base_price
    df[("TEST/BTC", "high")] = base_price + spread
    df[("TEST/BTC", "low")] = base_price - spread
    df[("TEST/BTC", "close")] = base_price + (spread * np.random.uniform(-1, 1, 5))
    df[("TEST/BTC", "volume")] = np.random.randint(100, 1000, size=5)
    return df


@pytest.fixture
def mock_price_data_volume_spike():
    """
    Test dataset designed to trigger a volume spike breakout signal
    on the final bar (index 4).
    """
    data = {
        ("TEST/BTC", "open"): [100, 101, 102, 103, 105],
        ("TEST/BTC", "high"): [101, 102, 103, 104, 115],
        ("TEST/BTC", "low"): [99, 100, 101, 102, 104],
        ("TEST/BTC", "close"): [100, 101, 102, 104, 114],  # breakout at end
        ("TEST/BTC", "volume"): [100, 90, 110, 90, 400],  # volume spike at end
    }
    index = pd.date_range("2025-01-01", periods=5, freq="1min")
    df = pd.DataFrame(data, index=index)
    df.columns.names = ["pair", "ohlcv"]
    return df
