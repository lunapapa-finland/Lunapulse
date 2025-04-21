import pandas as pd

class DataLoader:
    def load_data(self, file_path: str, resample: int = 0) -> pd.DataFrame:
        """
        Load OHLC data from a CSV file and optionally resample to specified minute intervals.
        Timezones are removed from Datetime for consistency.

        Args:
            file_path (str): Path to the CSV file.
            resample (int): Resampling interval in minutes (0 to skip, or 5, 10, 15, 30, 60).

        Returns:
            pd.DataFrame: DataFrame with OHLCV columns and naive DatetimeIndex.

        Raises:
            ValueError: If resample value is invalid, Datetime column is missing, or parsing fails.
        """
        if resample not in [0, 5, 10, 15, 30, 60]:
            raise ValueError("Resample must be 0 (no resampling) or one of [5, 10, 15, 30, 60] minutes")

        # Load CSV
        data = pd.read_csv(file_path)
        if 'Datetime' not in data.columns:
            raise ValueError(f"CSV file must contain a 'Datetime' column. Found columns: {data.columns.tolist()}")

        # Convert Datetime to UTC and remove timezone
        try:
            data['Datetime'] = pd.to_datetime(data['Datetime'], utc=True, errors='raise').dt.tz_convert(None)
        except Exception as e:
            raise ValueError(f"Failed to parse 'Datetime' column: {str(e)}. Sample values: {data['Datetime'].head().tolist()}")

        # Set Datetime as index
        data.set_index('Datetime', inplace=True)
        if not isinstance(data.index, pd.DatetimeIndex):
            raise ValueError(f"Index is not a DatetimeIndex. Index type: {type(data.index)}")

        # Select OHLCV columns
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        if not all(col in data.columns for col in required_columns):
            raise ValueError(f"CSV must contain columns: {required_columns}. Found: {data.columns.tolist()}")
        data = data[required_columns]

        # Remove duplicates, keeping first occurrence
        data = data[~data.index.duplicated(keep='first')]

        if resample > 0:
            # Round timestamps to nearest 5-minute interval to handle minor offsets
            data.index = data.index.round(f'{resample}min')
            # Detect input frequency (in minutes)
            freq = pd.infer_freq(data.index)
            if freq and pd.Timedelta(freq).total_seconds() / 60 == resample:
                return data  # Skip resampling if frequency matches
            # Resample to specified interval
            data = data.resample(f'{resample}min').agg({
                'Open': 'first',
                'High': 'max',
                'Low': 'min',
                'Close': 'last',
                'Volume': 'sum'
            }).dropna()

        return data