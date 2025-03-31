import pandas as pd
import logging
from strategies.base import StrategyBase

logger = logging.getLogger(__name__)


class VolumeSpikeBreakoutStrategy(StrategyBase):
    requires_ohlcv = True

    def __init__(
        self, price_data: pd.DataFrame, window: int = 20, volume_multiplier: float = 2.0
    ):
        super().__init__(price_data)
        self.window = window
        self.volume_multiplier = volume_multiplier

    def generate_signals(self) -> pd.DataFrame:
        signals = pd.DataFrame(index=self.price_data.index)
        close_df = self.price_data.xs("close", level="ohlcv", axis=1)
        volume_df = self.price_data.xs("volume", level="ohlcv", axis=1)

        for pair in close_df.columns:
            try:
                close = close_df[pair]
                volume = volume_df[pair]

                avg_volume = volume.rolling(self.window).mean()
                recent_high = close.rolling(self.window).max()
                recent_low = close.rolling(self.window).min()

                entry = (volume > avg_volume * self.volume_multiplier) & (
                    close > recent_high.shift(1)
                )
                exit = close < recent_low.shift(1)

                signal = pd.Series(0, index=close.index)
                signal[entry] = 1
                signal[exit] = -1

                signals[pair] = signal
            except KeyError as e:
                logger.warning(f"Missing data for {pair}: {e}")
                continue

        signals = signals[close_df.columns]
        return self.normalize_signals(signals)
