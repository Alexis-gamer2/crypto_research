"""
backtester.py
A simple vectorized backtester for long-only strategies.
Assumptions:
- We buy at next bar open price after a signal with slippage and fee.
- Fixed fraction position sizing (percent of equity).
"""
from typing import Dict
import pandas as pd
import numpy as np
import logging

logger = logging.getLogger(__name__)


def run_backtest(df: pd.DataFrame, initial_capital: float = 10_000.0, position_size: float = 0.95,
                 slippage: float = 0.0005, fee: float = 0.00075) -> pd.DataFrame:
    """
    df must include 'position' (0/1) and OHLC columns. Returns a results DataFrame with portfolio equity.
    """
    df = df.copy()
    df["next_open"] = df["open"].shift(-1)  # we trade at open of next bar
    df = df.dropna(subset=["next_open"])
    # compute returns when in position from next_open to close of that bar
    df["bar_return"] = (df["close"] / df["next_open"]) - 1.0
    # gross return after slippage and fee when entering position on that bar
    # when entering we apply (1 - fee - slippage) on entry and (1 - fee - slippage) on exit simplified
    # For vectorization, model effective return per bar when we are in position
    df["effective_return"] = df["bar_return"] - (fee * 2) - slippage

    # Start equity series
    equity = []
    equity_val = initial_capital
    in_position = 0
    for idx, row in df.iterrows():
        target_pos = int(row["position"])
        if target_pos and not in_position:
            # entering: allocate portion of equity
            allocation = equity_val * position_size
            units = allocation / row["next_open"]
            # Apply entry costs (approx)
            allocation_after_costs = allocation * (1 - fee - slippage)
            in_position = units
            cash = equity_val - allocation
        elif not target_pos and in_position:
            # exiting: sell at close
            proceeds = in_position * row["close"]
            proceeds_after_costs = proceeds * (1 - fee - slippage)
            equity_val = cash + proceeds_after_costs
            in_position = 0
            cash = equity_val
        elif target_pos and in_position:
            # hold: mark-to-market using close
            equity_val = cash + in_position * row["close"]
        else:
            # flat
            equity_val = equity_val  # no change
        equity.append({"datetime": idx, "equity": equity_val, "position": int(target_pos)})
    results = pd.DataFrame(equity).set_index("datetime")
    return results


def performance_metrics(equity: pd.Series) -> Dict[str, float]:
    """
    Compute simple performance metrics: CAGR, annualized volatility, sharpe (rf=0), max drawdown
    equity is a pd.Series indexed by datetime
    """
    returns = equity.pct_change().dropna()
    total_period_days = (equity.index[-1] - equity.index[0]).days
    if total_period_days == 0:
        total_period_days = 1
    cagr = (equity.iloc[-1] / equity.iloc[0]) ** (365.0 / total_period_days) - 1.0
    ann_vol = returns.std() * np.sqrt(365 * 24)  # assume hourly bars -> 365*24
    sharpe = cagr / (ann_vol + 1e-9)
    # max drawdown
    cummax = equity.cummax()
    drawdown = (equity - cummax) / cummax
    max_dd = drawdown.min()
    return {"CAGR": float(cagr), "AnnVol": float(ann_vol), "Sharpe": float(sharpe), "MaxDrawdown": float(max_dd)}
