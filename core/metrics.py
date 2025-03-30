import vectorbt as vbt


def calculate_metrics(portfolio: vbt.Portfolio) -> dict:
    """Calculate key backtest metrics."""
    return {
        "total_return": portfolio.total_return().iloc[0],
        "sharpe_ratio": portfolio.sharpe_ratio().iloc[0],
        "max_drawdown": portfolio.max_drawdown().iloc[0],
        "win_rate": portfolio.win_rate().iloc[0],
        "expectancy": portfolio.expectancy().iloc[0],
        "exposure_time": portfolio.positions().coverage().iloc[0],
    }
