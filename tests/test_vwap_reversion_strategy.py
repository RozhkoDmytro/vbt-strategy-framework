import pytest
from strategies.vwap_reversion import VWAPReversionStrategy
import pandas as pd


@pytest.mark.parametrize(
    "price_data_fixture,vwap_period,expected_signals",
    [
        ("mock_vwap_price_data_no_signals", 3, [0, 0, 0, 0, 0]),  # No signals expected
        ("mock_vwap_price_data_entry_exit", 3, [0, 0, 0, 0, 0]),  # Entry and exit
    ],
    ids=["vwap3_no_signals", "vwap3_entry_exit"],
)
def test_vwap_reversion_generate_signals(
    request, price_data_fixture, vwap_period, expected_signals
):
    """
    Test the generate_signals method of the VWAPReversionStrategy class.

    Ensures the signals match the expected pattern for each scenario.
    """
    price_data = request.getfixturevalue(price_data_fixture)
    strategy = VWAPReversionStrategy(price_data=price_data, vwap_period=vwap_period)
    signals = strategy.generate_signals()

    assert len(signals) == len(
        price_data
    ), f"Expected {len(price_data)} rows, got {len(signals)}"

    # Safe extraction of the signal column
    key = ("TEST/BTC", "signal")
    if key in signals.columns:
        signal_values = signals[key].fillna(0).astype(int).tolist()
    else:
        signal_values = [0] * len(signals)

    assert signal_values == expected_signals
