import pytest
import pandas as pd
from core.backtester import Backtester
from strategies.sma_cross import SMACrossStrategy
from strategies.rsi_bb import RSIBBStrategy
from strategies.vwap_reversion import VWAPReversionStrategy
import os


@pytest.mark.parametrize(
    "strategy_class", [SMACrossStrategy, RSIBBStrategy, VWAPReversionStrategy]
)
def test_backtester_run(mock_price_data1, strategy_class):
    """
    Test the Backtester run method for multiple strategy classes.

    This test verifies that the `Backtester` class can successfully
    execute the `run` method using different trading strategy classes,
    specifically `SMACrossStrategy`, `RSIBBStrategy`, and
    `VWAPReversionStrategy`. It checks that the resulting portfolio
    is not None and contains valid statistics and value data.

    Parameters
    ----------
    mock_price_data1 : pd.DataFrame
        Mock price data provided as test input.
    strategy_class : class
        The trading strategy class to be tested.

    Asserts
    -------
    - The resulting portfolio is not None.
    - The portfolio contains valid statistics.
    - The portfolio has a non-null value.
    """

    strategy = strategy_class(mock_price_data1)

    backtester = Backtester(strategy, mock_price_data1)

    portfolio = backtester.run()

    assert portfolio is not None
    assert portfolio.stats() is not None
    assert portfolio.value() is not None
