from dataclasses import dataclass


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

    # Backtest parameters
    commission: float = 0.001  # 0.1%
    slippage: float = 0.0005  # 0.05%

    # Paths and formats
    data_dir: str = "data/"
    results_dir: str = "results/"
    data_file: str = "btc_1m_feb25.parquet"
    data_format: str = "parquet"


config = Config()
