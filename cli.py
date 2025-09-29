"""
cli.py
Minimal CLI for quickly running a backtest.
"""
import argparse
from .api import fetch_market_chart
from .data import prepare_price_series
from .strategy import ema_crossover_signals
from .backtester import run_backtest, performance_metrics
from .utils import setup_logging, plot_equity_curve
import logging

logger = logging.getLogger(__name__)


def main():
    setup_logging()
    parser = argparse.ArgumentParser(description="Crypto Research Toolkit - simple backtest CLI")
    parser.add_argument("--coin", default="bitcoin", help="CoinGecko id (default: bitcoin)")
    parser.add_argument("--days", type=int, default=60, help="Historical days to fetch (default: 60)")
    parser.add_argument("--fast", type=int, default=12, help="Fast EMA span")
    parser.add_argument("--slow", type=int, default=26, help="Slow EMA span")
    args = parser.parse_args()

    logger.info("Fetching data for %s (%d days)", args.coin, args.days)
    raw = fetch_market_chart(coin=args.coin, days=args.days)
    df = prepare_price_series(raw)
    df_signals = ema_crossover_signals(df, fast=args.fast, slow=args.slow)
    results = run_backtest(df_signals)
    metrics = performance_metrics(results["equity"])
    logger.info("Backtest metrics: %s", metrics)
    print("Performance metrics:")
    for k, v in metrics.items():
        print(f"{k}: {v:.4f}")
    plot_equity_curve(results["equity"], title=f"{args.coin} EMA{args.fast}/{args.slow} Equity")
