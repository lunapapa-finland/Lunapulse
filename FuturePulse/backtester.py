from FuturePulse.strategy import BaseStrategy
import pandas as pd

class Backtester:
    def run(self, data: pd.DataFrame, strategy: BaseStrategy) -> dict:
        """Run backtest and return trades/metrics."""
        signals = strategy.generate_signals(data)
        return {"trades": signals, "win_rate": 0.0}