import pandas as pd
import pytest
from strategies.sma_cross import SMACrossStrategy


def test_sma_cross_signals():
    """Test signal generation for SMA Crossover strategy."""
    data = pd.DataFrame(
        {"close": [10, 11, 12, 13, 12, 11, 10, 9, 10, 11]},
        index=pd.date_range("2025-02-01", periods=10, freq="1min"),
    )
    strategy = SMACrossStrategy(data, fast_period=2, slow_period=5)
    signals = strategy.generate_signals()
    assert signals.iloc[0] == 0  # No signal at start
