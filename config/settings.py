import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / 'logs'
DATA_DIR = BASE_DIR / 'data'

# Create directories if they don't exist
LOGS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)

# Exchange Configuration
EXCHANGE = os.getenv('EXCHANGE', 'binance')
API_KEY = os.getenv('API_KEY', '')
API_SECRET = os.getenv('API_SECRET', '')

# Trading Configuration
TRADING_PAIR = os.getenv('TRADING_PAIR', 'BTC/USDT')
TRADE_AMOUNT = float(os.getenv('TRADE_AMOUNT', 100))

# Strategy Parameters
BUY_THRESHOLD = float(os.getenv('BUY_THRESHOLD', 0.02))
SELL_THRESHOLD = float(os.getenv('SELL_THRESHOLD', 0.02))
STOP_LOSS = float(os.getenv('STOP_LOSS', 0.05))
TAKE_PROFIT = float(os.getenv('TAKE_PROFIT', 0.10))

# Risk Management
MAX_TRADES_PER_DAY = int(os.getenv('MAX_TRADES_PER_DAY', 5))
MAX_PORTFOLIO_RISK = float(os.getenv('MAX_PORTFOLIO_RISK', 0.02))

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = LOGS_DIR / os.getenv('LOG_FILE', 'trading_bot.log')

# Backtesting
BACKTEST_START_DATE = os.getenv('BACKTEST_START_DATE', '2023-01-01')
BACKTEST_END_DATE = os.getenv('BACKTEST_END_DATE', '2024-01-01')
BACKTEST_INITIAL_BALANCE = float(os.getenv('BACKTEST_INITIAL_BALANCE', 10000))
