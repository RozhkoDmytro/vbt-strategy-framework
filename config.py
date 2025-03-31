from dataclasses import dataclass
from strategies.sma_cross import SMACrossStrategy
from strategies.rsi_bb import RSIBBStrategy
from strategies.vwap_reversion import VWAPReversionStrategy
from strategies.volume_spike_breakout import VolumeSpikeBreakoutStrategy
from exchanges.binance import BinanceExchange


@dataclass
class Config:
    # Exchange settings
    exchange_name: str = "binance"
    base_currency: str = "BTC"
    num_pairs: int = 100
    timeframe: str = "1m"

    # Data period
    start_date: str = "2025-02-01"
    end_date: str = "2025-02-28"
    fetch_delay_seconds: int = 0.5  # delay between paginated API requests

    # Backtest parameters
    commission: float = 0.001  # 0.1%
    slippage: float = 0.0005  # 0.05%

    # Paths and formats
    data_dir: str = "data/"
    results_dir: str = "results/"
    data_format: str = "parquet"
    data_file_template: str = (
        "{base_currency}_{timeframe}_{start_date}_{end_date}_{num_pairs}.{data_format}"
    )

    # Strategies
    strategies: list = None  # Will be initialized in __post_init__

    # Supported exchanges
    supported_exchanges: dict = None  # Will be initialized in __post_init__

    def __post_init__(self):
        """Initialize strategies and supported exchanges with default values."""
        if self.strategies is None:
            self.strategies = [
                SMACrossStrategy,
                RSIBBStrategy,
                VWAPReversionStrategy,
                VolumeSpikeBreakoutStrategy,
            ]
        if self.supported_exchanges is None:
            self.supported_exchanges = {"binance": BinanceExchange}

    @property
    def data_file(self) -> str:
        """Generate the data file name based on the template and current parameters.

        Returns:
            Formatted data file name (e.g., 'btc_1m_20250201_20250228_100.parquet').
        """
        # Replace dashes in dates to make the filename cleaner
        start_date_clean = self.start_date.replace("-", "")
        end_date_clean = self.end_date.replace("-", "")
        return self.data_file_template.format(
            base_currency=self.base_currency.lower(),
            timeframe=self.timeframe,
            start_date=start_date_clean,
            end_date=end_date_clean,
            num_pairs=self.num_pairs,
            data_format=self.data_format,
        )


config = Config()
