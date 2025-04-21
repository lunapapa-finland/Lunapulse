from FuturePulse.data_loader import DataLoader
import pytest
import pandas as pd

def test_load_data():
    loader = DataLoader()
    data = loader.load_data("Examples/MES_1min_data_2024-12-24_H25.CME.csv", resample=True)
    assert isinstance(data, pd.DataFrame)
    assert set(data.columns).issuperset({'Open', 'High', 'Low', 'Close', 'Volume'})
    assert data.index.inferred_type == 'datetime64'
    assert len(data) < 201