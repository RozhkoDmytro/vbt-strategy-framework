import vectorbt as vbt
import logging

logger = logging.getLogger(__name__)


def calculate_metrics(portfolio: vbt.Portfolio) -> dict:
    """Calculate performance metrics from a portfolio."""
    stats = portfolio.stats()
    logger.debug(f"Available stats keys: {list(stats.keys())}")  # Додаємо для дебагінгу
    return {
        "total_return": stats.get("Total Return [%]", 0.0),
        "sharpe_ratio": stats.get(
            "Sharpe Ratio", 0.0
        ),  # Використовуємо .get із значенням за замовчуванням
        "sortino_ratio": stats.get("Sortino Ratio", 0.0),
        "max_drawdown": stats.get("Max Drawdown [%]", 0.0),
        "calmar_ratio": stats.get("Calmar Ratio", 0.0),
        "win_rate": stats.get("Win Rate [%]", 0.0),
    }
