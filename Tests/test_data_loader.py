from FuturePulse.data_loader import DataLoader
import pytest
import pandas as pd

def test_load_data():
    loader = DataLoader()
    data = loader.load_data("Examples/MES.csv", resample=0)
    assert isinstance(data, pd.DataFrame)
    assert set(data.columns).issuperset({'Open', 'High', 'Low', 'Close', 'Volume'})
    assert isinstance(data.index, pd.DatetimeIndex)
    assert data.index.tz is None  # Ensure naive timestamps
    assert len(data) > 0

def test_resample_same_frequency():
    loader = DataLoader()
    data_no_resample = loader.load_data("Examples/MES.csv", resample=0)
    data_resample = loader.load_data("Examples/MES.csv", resample=5)
    assert data_no_resample.columns.tolist() == data_resample.columns.tolist()
    assert len(data_no_resample) == len(data_resample)  # Expect same row count for 5-minute data
    assert data_no_resample.equals(data_resample)  # Data should be identical

def test_invalid_datetime_column():
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write("Datetime,Open,High,Low,Close,Volume\n")
        f.write("invalid,1,2,3,4,100\n")
        temp_file = f.name
    loader = DataLoader()
    with pytest.raises(ValueError, match="Failed to parse 'Datetime' column"):
        loader.load_data(temp_file, resample=0)
    import os
    os.unlink(temp_file)