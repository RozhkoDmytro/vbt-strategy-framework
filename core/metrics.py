import vectorbt as vbt


def calculate_metrics(portfolio: vbt.Portfolio) -> dict:
    stats = portfolio.stats(agg_func=None)

    return {
        "total_return": stats["Total Return [%]"].mean(),
        "sharpe_ratio": stats["Sharpe Ratio"].mean(),
        "max_drawdown": stats["Max Drawdown [%]"].mean(),
        "win_rate": portfolio.trades.win_rate().mean(),
        "expectancy": portfolio.trades.expectancy().mean(),
        "exposure_time": stats["Max Gross Exposure [%]"].mean(),  # correct column name
    }
