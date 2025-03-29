# VBTTrader

## Overview
VBTTrader is a modular backtesting framework for trading strategies built with Python and VectorBT. It analyzes 1-minute OHLCV data for 100 BTC trading pairs from Binance for February 2025. The project emphasizes scalability, clean code, and comprehensive documentation, making it easy to extend with new strategies, exchanges, or timeframes.

## Features
- **Data Handling**: Fetches and caches 1-minute OHLCV data from Binance in `.parquet` format.
- **Trading Strategies**: Includes SMA Crossover, RSI with Bollinger Bands, and VWAP Reversion strategies.
- **Backtesting**: Powered by VectorBT with commission and slippage considerations.
- **Results**: Generates equity curves, performance metrics, and heatmaps.

## Installation
1. **Clone the repository**:
```bash
git clone https://github.com/RozhkoDmytro/vbt-strategy-framework
cd VBTTrader
```

2. **Set up a virtual environment**:
```bash
python3 -m venv vbt_env
source vbt_env/bin/activate  # On macOS/Linux
# vbt_env\Scripts\activate  # On Windows
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

## Usage
1. **Run the backtest**:
```bash
python main.py
```

2. **Check results**:
- Metrics are saved in `results/metrics.csv`.
- Equity curve plots are saved in `results/screenshots/<strategy_name>_equity.png`.

## Configuration
Settings are managed in `config.py`:
- `DATA_SOURCE`: Supports "binance" or "csv".
- `START_DATE`, `END_DATE`: Backtest period.
- `SYMBOLS`: List of trading pairs.
- `DATA_PATH`: Path to cache data.

## Strategies
- **SMACrossStrategy**: Triggers trades based on the crossover of fast (10-period) and slow (50-period) moving averages.
- **RSIBBStrategy**: (Placeholder) RSI < 30 with confirmation from a bounce off the lower Bollinger Band.
- **VWAPReversionStrategy**: (Placeholder) Opens when price deviates 2% below VWAP and exits on reversion.

## Project Structure
```
VBTTrader/
├── core/               # Core modules
│   ├── data_loader.py
│   ├── backtester.py
│   ├── exchange.py (interface)
│   └── metrics.py
├── strategies/         # Trading strategies
│   ├── base.py
│   ├── sma_cross.py
│   ├── rsi_bb.py
│   └── vwap_reversion.py
├── tests/              # Unit tests
├── data/               # Cached data
├── results/            # Backtest outputs
│   └── screenshots/    # Equity curve plots
├── config.py
├── main.py
├── requirements.txt
└── README.md
```

## Requirements
- Python ≥ 3.10
- Dependencies: `vectorbt`, `pandas`, `numpy`, `plotly`, `pyarrow`, `ccxt`, `pytest`

## Notes
- If Binance data is unavailable, switch to CSV mode via `config.py`.
- Easily extend the framework by adding new strategies or data sources.

## License
This project is unlicensed for now. Feel free to use and modify it as needed.

## Contact
For questions or contributions, open an issue on GitHub.
