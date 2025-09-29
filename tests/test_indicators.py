import pandas as pd
import numpy as np
from crypto_research.indicators import ema, rsi

def test_ema_constant():
    s = pd.Series([1.0] * 50)
    out = ema(s, span=10)
    assert np.allclose(out.dropna(), 1.0)

def test_rsi_neutral_on_flat():
    s = pd.Series([1.0] * 50)
    out = rsi(s, period=14)
    assert out.iloc[-1] == 50
