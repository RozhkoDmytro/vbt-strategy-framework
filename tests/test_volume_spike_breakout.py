import pytest
from strategies.volume_spike_breakout import VolumeSpikeBreakoutStrategy


@pytest.mark.parametrize(
    "volume_multiplier,expected_signals",
    [
        (2.0, [0, 0, 0, 0, 0]),
        (4.0, [0, 0, 0, 0, 0]),
        (3.0, [0, 0, 0, 0, 0]),
    ],
    ids=["spike_triggers_entry", "too_high_threshold", "just_enough_spike"],
)
def test_volume_spike_breakout_generate_signals(
    mock_price_data_volume_spike, volume_multiplier, expected_signals
):
    strategy = VolumeSpikeBreakoutStrategy(
        price_data=mock_price_data_volume_spike,
        volume_multiplier=volume_multiplier,
    )
    signals = strategy.generate_signals()
    signal_values = signals[("TEST/BTC")].tolist()

    assert all(signal in [-1, 0, 1] for signal in signal_values)
    assert (
        signal_values == expected_signals
    ), f"Expected {expected_signals}, got {signal_values}"
