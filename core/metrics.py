import numpy as np
import pandas as pd
import vectorbt as vbt


def calculate_metrics(portfolio: vbt.Portfolio) -> pd.DataFrame:
    # Get stats per column (per symbol)
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
