# Trading Bot

A Python-based cryptocurrency/stock trading bot with automated trading strategies.

## Features

- Real-time market data fetching
- Automated trading strategies
- Portfolio tracking
- Risk management
- Backtesting capabilities
- Configurable trading parameters

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Esaya5/trading-bot.git
cd trading-bot
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure your settings:
```bash
cp .env.example .env
# Edit .env with your API keys and preferences
```

## Usage

### Start the trading bot:
```bash
python main.py
```

### Run backtesting:
```bash
python backtest.py
```

## Project Structure

```
trading-bot/
├── main.py              # Entry point
├── backtest.py          # Backtesting script
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore rules
├── config/
│   └── settings.py     # Configuration settings
├── bot/
│   ├── __init__.py
│   ├── bot.py          # Main bot logic
│   ├── trader.py       # Trading execution
│   └── strategies.py    # Trading strategies
├── data/
│   ├── __init__.py
│   ├── fetcher.py      # Market data fetcher
│   └── analyzer.py     # Data analysis
└── utils/
    ├── __init__.py
    ├── logger.py       # Logging utilities
    └── helpers.py      # Helper functions
```

## Configuration

Edit `.env` file with your settings:

```
# Exchange Settings
EXCHANGE=binance
API_KEY=your_api_key
API_SECRET=your_api_secret

# Trading Pair
TRADING_PAIR=BTC/USDT

# Bot Settings
BUY_THRESHOLD=0.02
SELL_THRESHOLD=0.02
STOP_LOSS=0.05
TAKE_PROFIT=0.10

# Logging
LOG_LEVEL=INFO
```

## API Support

Currently supports:
- Binance
- Coinbase
- Kraken

## Risk Disclaimer

⚠️ **This bot is for educational purposes only.** Trading cryptocurrencies and stocks carries risk. Use this bot at your own risk and with small amounts you can afford to lose.

## License

MIT License

## Contributing

Pull requests are welcome. For major changes, please open an issue first.
