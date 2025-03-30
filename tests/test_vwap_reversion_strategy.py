import pytest
from strategies.vwap_reversion import VWAPReversionStrategy


@pytest.mark.parametrize(
    "price_data_fixture,vwap_period,expected_signals",
    [
        ("mock_vwap_price_data_no_signals", 3, [0, 0, 0, 0, 0]),  # Без сигналів
        ("mock_vwap_price_data_entry_exit", 3, [0, 0, 1, -1, 0]),  # Вхід і вихід
    ],
    ids=["vwap3_no_signals", "vwap3_entry_exit"],
)
def test_vwap_reversion_generate_signals(
    request, price_data_fixture, vwap_period, expected_signals
):
    price_data = request.getfixturevalue(price_data_fixture)
    strategy = VWAPReversionStrategy(price_data=price_data, vwap_period=vwap_period)
    signals = strategy.generate_signals()
    assert len(signals) == len(
        price_data
    ), f"Expected {len(price_data)} rows, got {len(signals)}"
    signal_values = signals[("TEST/BTC", "signal")]
    assert all(
        signal in [-1, 0, 1] for signal in signal_values
    ), f"Found invalid signal values: {signal_values.tolist()}"
    assert (
        signal_values.tolist() == expected_signals
    ), f"Expected signals {expected_signals}, but got {signal_values.tolist()}"
