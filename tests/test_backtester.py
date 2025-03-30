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

    strategy = strategy_class(mock_price_data1)

    backtester = Backtester(strategy, mock_price_data1[("TEST/BTC", "close")])

    portfolio = backtester.run()

    assert portfolio is not None
    assert portfolio.stats() is not None
    assert portfolio.value() is not None
