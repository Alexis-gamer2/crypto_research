"""
utils.py
Logging and plotting helpers.
"""
import logging
import matplotlib.pyplot as plt
import pandas as pd

def setup_logging(level=logging.INFO):
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        level=level
    )

def plot_equity_curve(equity: pd.Series, title: str = "Equity Curve"):
    plt.figure(figsize=(10, 5))
    plt.plot(equity.index, equity.values)
    plt.title(title)
    plt.xlabel("Time")
    plt.ylabel("Equity")
    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.show()
