import pandas as pd

class DataLoader:
    def load_data(self, file_path: str, resample: bool = True) -> pd.DataFrame:
        """Load OHLC data from a CSV file and optionally resample to 5-minute intervals."""
        data = pd.read_csv(file_path, parse_dates=['Datetime'])
        data.set_index('Datetime', inplace=True)
        data = data[['Open', 'High', 'Low', 'Close', 'Volume']]  # Drop Adj Close
        
        if resample:
            # Resample to 5-minute intervals
            data = data.resample('5min').agg({
                'Open': 'first',
                'High': 'max',
                'Low': 'min',
                'Close': 'last',
                'Volume': 'sum'
            }).dropna()
        
        return data