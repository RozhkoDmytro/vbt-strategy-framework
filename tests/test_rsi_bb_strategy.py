import pytest
from strategies.rsi_bb import RSIBBStrategy


@pytest.mark.parametrize(
    "rsi_period,bb_period,expected_signals",
    [
        (2, 2, [0, 0, 0, 0, 0]),
        (2, 2, [0, 0, 0, 0, 0]),
    ],
    ids=["rsi2_bb2_no_signals", "rsi2_bb2_entry"],
)
def test_rsi_bb_generate_signals(
    mock_price_data2, rsi_period, bb_period, expected_signals
):
    strategy = RSIBBStrategy(
        price_data=mock_price_data2, rsi_period=rsi_period, bb_period=bb_period
    )
    signals = strategy.generate_signals()
    assert len(signals) == len(mock_price_data2)
    signal_values = signals[("TEST/BTC", "close")]
    assert all(signal in [-1, 0, 1] for signal in signal_values)
    assert (
        signal_values.tolist() == expected_signals
    ), f"Expected signals {expected_signals}, but got {signal_values.tolist()}"
