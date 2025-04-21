from abc import ABC, abstractmethod
import pandas as pd
import numpy as np

class BaseStrategy(ABC):
    @abstractmethod
    def generate_signals(self, data: pd.DataFrame) -> list:
        """Generate trade signals."""
        pass

class WedgeBreakoutStrategy(BaseStrategy):
    def __init__(self, lookback: int = 20, threshold: float = 0.5):
        self.lookback = lookback  # Number of bars to analyze for wedge
        self.threshold = threshold  # Breakout threshold (% of range)

    def generate_signals(self, data: pd.DataFrame) -> list:
        """Detect wedge breakouts and generate buy/sell signals."""
        signals = []
        highs = data['High']
        lows = data['Low']
        closes = data['Close']

        for i in range(self.lookback, len(data)):
            # Get lookback window
            window_highs = highs.iloc[i - self.lookback:i]
            window_lows = lows.iloc[i - self.lookback:i]
            
            # Calculate slopes of highs and lows using linear regression
            x = np.arange(self.lookback)
            high_slope, _ = np.polyfit(x, window_highs, 1)
            low_slope, _ = np.polyfit(x, window_lows, 1)

            # Check for converging pattern (negative high slope, positive low slope)
            if high_slope < 0 and low_slope > 0:
                # Calculate resistance (max high) and support (min low)
                resistance = window_highs.max()
                support = window_lows.min()
                current_close = closes.iloc[i]
                prev_close = closes.iloc[i - 1]

                # Breakout conditions
                if prev_close <= resistance and current_close > resistance:
                    signals.append({
                        'timestamp': data.index[i],
                        'type': 'buy',
                        'price': current_close
                    })
                elif prev_close >= support and current_close < support:
                    signals.append({
                        'timestamp': data.index[i],
                        'type': 'sell',
                        'price': current_close
                    })

        return signals