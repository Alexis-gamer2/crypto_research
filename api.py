"""
api.py
Helpers to fetch historical OHLC data from CoinGecko.
CoinGecko returns prices as [timestamp_ms, price].
We build a simple OHLC-like series by resampling the minute-level data.
"""
from typing import Tuple
import requests
import pandas as pd
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def fetch_market_chart(coin: str = "bitcoin", vs_currency: str = "usd", days: int = 30) -> pd.DataFrame:
    """
    Fetch market chart 'prices' from CoinGecko for given days.
    Returns a DataFrame indexed by datetime with column 'price'.
    """
    url = f"https://api.coingecko.com/api/v3/coins/{coin}/market_chart"
    params = {"vs_currency": vs_currency, "days": days}
    logger.info("Fetching CoinGecko market_chart: %s %s days", coin, days)
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    data = r.json()
    prices = data.get("prices", [])
    df = pd.DataFrame(prices, columns=["ts", "price"])
    df["datetime"] = pd.to_datetime(df["ts"], unit="ms")
    df = df.set_index("datetime").drop(columns=["ts"])
    # The data is irregular; resample to 1h OHLC by aggregating
    price = df["price"].resample("1H").ohlc().ffill().dropna()
    price.columns = ["open", "high", "low", "close"]
    return price
