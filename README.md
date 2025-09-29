# Crypto Research Toolkit

A small, professional Python toolbox for fetching crypto data, computing indicators, and running simple backtests.

## Features
- CoinGecko historical data fetch (no API key)
- EMA & RSI implementations
- EMA crossover strategy (configurable)
- Simple backtester with slippage/fees & performance metrics
- CLI to run an end-to-end backtest
- Unit tests

## Install
```bash
git clone https://github.com/YourGitHubHandle/crypto-research.git
cd crypto-research
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
