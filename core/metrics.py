import numpy as np
import pandas as pd
import vectorbt as vbt


def calculate_metrics(portfolio: vbt.Portfolio) -> pd.DataFrame:
    # Get stats per column (per symbol)
    """
    Calculate performance metrics for a given portfolio.

    Parameters
    ----------
    portfolio : vbt.Portfolio
        A VectorBT Portfolio object containing backtesting results.

    Returns
    -------
    pd.DataFrame
        DataFrame containing calculated metrics including Total Return,
        Sharpe Ratio, Max Drawdown, Win Rate, Expectancy, and Exposure Time.
        Metrics that cannot be calculated are set to NaN.
    """

    stats = portfolio.stats(group_by=False).to_frame().T

    # Ensure all required metrics are safely extracted, fallback to NaN
    metrics = pd.DataFrame(
        {
            "Total Return": stats.get("Total Return [%]", np.nan),
            "Sharpe Ratio": stats.get("Sharpe Ratio", np.nan),
            "Max Drawdown": stats.get("Max Drawdown [%]", np.nan),
            "Win Rate": portfolio.trades.win_rate() * 100,
            "Expectancy": portfolio.trades.expectancy(),
            "Exposure Time": stats.get("Exposure Time [%]", np.nan),
        }
    )

    return metrics
