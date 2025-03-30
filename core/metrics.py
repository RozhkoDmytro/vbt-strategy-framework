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

    # Normalize percentage fields if missing
    if "Total Return [%]" not in stats and "Total Return" in stats:
        stats["Total Return [%]"] = stats["Total Return"] * 100

    if "Max Drawdown [%]" not in stats and "Max Drawdown" in stats:
        stats["Max Drawdown [%]"] = stats["Max Drawdown"] * 100

    if "Exposure Time [%]" not in stats and "Exposure Time" in stats:
        stats["Exposure Time [%]"] = stats["Exposure Time"] * 100

    metrics = pd.DataFrame(
        {
            "Total Return [%]": stats.get("Total Return [%]", np.nan),
            "Sharpe Ratio": stats.get("Sharpe Ratio", np.nan),
            "Max Drawdown [%]": stats.get("Max Drawdown [%]", np.nan),
            "Win Rate [%]": portfolio.trades.win_rate() * 100,
            "Expectancy": portfolio.trades.expectancy(),
            "Exposure Time [%]": stats.get("Exposure Time [%]", np.nan),
        }
    )

    return metrics
