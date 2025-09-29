"""
indicators.py
Simple implementations of EMA and RSI.
"""
from typing import Tuple
import pandas as pd
import numpy as np


def ema(series: pd.Series, span: int) -> pd.Series:
    """
    Exponential moving average using pandas EWMA.
    """
    return series.ewm(span=span, adjust=False).mean()


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """
    Relative Strength Index (RSI).
    """
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -1 * delta.clip(upper=0)
    ma_up = up.rolling(window=period, min_periods=period).mean()
    ma_down = down.rolling(window=period, min_periods=period).mean()
    rs = ma_up / ma_down
    rsi = 100 - (100 / (1 + rs))
    rsi = rsi.fillna(50)  # fill early values neutrally
    return rsi
