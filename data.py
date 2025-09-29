"""
data.py
Utilities to load and save CSVs and to prepare tradeable price series.
"""
from typing import Tuple
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def prepare_price_series(df_ohlc: pd.DataFrame) -> pd.DataFrame:
    """
    Ensures the OHLC DataFrame has expected columns and returns a copy with 'close' and 'datetime' index.
    """
    required = {"open", "high", "low", "close"}
    if not required.issubset(df_ohlc.columns):
        raise ValueError(f"DataFrame missing required columns: {required - set(df_ohlc.columns)}")
    df = df_ohlc.copy()
    df = df.sort_index()
    logger.debug("Prepared price series with %d rows", len(df))
    return df
