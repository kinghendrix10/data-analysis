# tests/test_data_analysis.py

import pytest
import pandas as pd
from backend.services.data_analysis import perform_analysis

def test_perform_analysis():
    data = {"Date": ["2021-01-01", "2021-02-01"], "Value": [10, 20]}
    df = pd.DataFrame(data)
    result = perform_analysis(df)
    assert result is not None
