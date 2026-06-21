import logging
from typing import List, Optional
import ccxt

logger = logging.getLogger(__name__)

class MarketDataFetcher:
    """Fetches market data from exchanges"""
    
    def __init__(self, exchange: str, api_key: str = '', api_secret: str = ''):
        """
        Initialize MarketDataFetcher
        
        Args:
            exchange: Exchange name (e.g., 'binance')
            api_key: Exchange API key (optional)
            api_secret: Exchange API secret (optional)
        """
        self.exchange_name = exchange
        
        # Initialize exchange
        exchange_class = getattr(ccxt, exchange)
        self.exchange = exchange_class({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True
        })
        
        logger.info(f"MarketDataFetcher initialized for {exchange}")
    
    def fetch_ohlcv(self, symbol: str, timeframe: str = '1h', limit: int = 100) -> Optional[List]:
        """
        Fetch OHLCV (candlestick) data
        
        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            timeframe: Timeframe (e.g., '1m', '5m', '1h', '1d')
            limit: Number of candles to fetch
        
        Returns:
            OHLCV data or None if error
        """
        try:
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            logger.debug(f"Fetched {len(ohlcv)} candles for {symbol}")
            return ohlcv
        
        except Exception as e:
            logger.error(f"Error fetching OHLCV data: {str(e)}")
            return None
    
    def fetch_ticker(self, symbol: str) -> Optional[dict]:
        """
        Fetch ticker data
        
        Args:
            symbol: Trading pair
        
        Returns:
            Ticker data or None if error
        """
        try:
            ticker = self.exchange.fetch_ticker(symbol)
            return ticker
        
        except Exception as e:
            logger.error(f"Error fetching ticker: {str(e)}")
            return None
    
    def fetch_order_book(self, symbol: str, limit: int = 20) -> Optional[dict]:
        """
        Fetch order book data
        
        Args:
            symbol: Trading pair
            limit: Number of bids/asks to fetch
        
        Returns:
            Order book data or None if error
        """
        try:
            orderbook = self.exchange.fetch_order_book(symbol, limit=limit)
            return orderbook
        
        except Exception as e:
            logger.error(f"Error fetching order book: {str(e)}")
            return None
