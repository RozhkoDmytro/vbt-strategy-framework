import pytest
from strategies.sma_cross import SMACrossStrategy


@pytest.mark.parametrize(
    "price_data_fixture,fast_period,slow_period,expected_signals",
    [
        ("mock_price_data_no_signals", 2, 3, [0, 0, 0, 0, 0]),  # Без сигналів
        ("mock_price_data_entry_exit", 2, 3, [0, 0, 1, -1, -1]),  # Вхід і вихід
    ],
    ids=["sma2_3_no_signals", "sma2_3_entry_exit"],
)
def test_sma_cross_generate_signals(
    request, price_data_fixture, fast_period, slow_period, expected_signals
):
    """
    Test the generate_signals method of the SMACrossStrategy class.

    Verifies that the generated signals are correct and match the expected values.

    Parameters
    ----------
    price_data_fixture : str
        The name of the pytest fixture that contains the price data.
    fast_period : int
        The period for the fast moving average.
    slow_period : int
        The period for the slow moving average.
    expected_signals : list
        A list of expected signals (1 for buy, -1 for sell, 0 for hold).

    """
    price_data = request.getfixturevalue(price_data_fixture)
    strategy = SMACrossStrategy(
        price_data=price_data, fast_period=fast_period, slow_period=slow_period
    )
    signals = strategy.generate_signals()
    assert len(signals) == len(
        price_data
    ), f"Expected {len(price_data)} rows, got {len(signals)}"
    signal_values = signals[("TEST/BTC", "close")]
    assert all(
        signal in [-1, 0, 1] for signal in signal_values
    ), f"Found invalid signal values: {signal_values.tolist()}"
    assert (
        signal_values.tolist() == expected_signals
    ), f"Expected signals {expected_signals}, but got {signal_values.tolist()}"
