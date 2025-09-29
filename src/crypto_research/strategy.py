"""
strategy.py
Example strategy: EMA crossover (fast/slow) -> generate signals.
Signals: 1 for long, 0 for flat. No shorts.
"""
from typing import Dict
import pandas as pd
from .indicators import ema, rsi


def ema_crossover_signals(df: pd.DataFrame, fast: int = 12, slow: int = 26, rsi_period: int = 14, rsi_filter: bool = True) -> pd.DataFrame:
    """
    Adds columns to df: ema_fast, ema_slow, rsi, signal
    signal: 1 = long, 0 = flat
    Optionally require rsi < 70 to enter to avoid overbought.
    """
    df = df.copy()
    df["ema_fast"] = ema(df["close"], span=fast)
    df["ema_slow"] = ema(df["close"], span=slow)
    df["rsi"] = rsi(df["close"], period=rsi_period)

    # generate naive crossover signals
    df["signal_raw"] = (df["ema_fast"] > df["ema_slow"]).astype(int)
    # only take signal changes (enter when 0->1)
    df["signal"] = df["signal_raw"].shift(1).fillna(0)  # shift: act at next bar open
    if rsi_filter:
        # don't enter if rsi is above 70
        enter_mask = (df["signal_raw"] == 1) & (df["rsi"] < 70)
        df["signal"] = enter_mask.astype(int)
    # keep forward-filled position
    df["position"] = df["signal"].replace(0, method="ffill").fillna(0)
    return df
