import pandas as pd
import pytest
from core.backtester import Backtester
from strategies.sma_cross import SMACrossStrategy


def test_backtester_run():
    """Test backtester execution."""
    data = pd.DataFrame(
        {"close": [10, 11, 12, 13, 12, 11]},
        index=pd.date_range("2025-02-01", periods=6, freq="1min"),
    )
    strategy = SMACrossStrategy(data)
    backtester = Backtester(strategy, data)
    portfolio = backtester.run()
    assert portfolio.total_return().iloc[0] is not None
