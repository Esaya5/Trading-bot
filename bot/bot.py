import logging
from datetime import datetime
from config.settings import (
    EXCHANGE, API_KEY, API_SECRET, TRADING_PAIR,
    LOG_LEVEL, LOG_FILE
)
from utils.logger import setup_logger
from data.fetcher import MarketDataFetcher
from bot.strategies import MovingAverageCrossover
from bot.trader import Trader

logger = setup_logger(__name__, LOG_LEVEL, str(LOG_FILE))

class TradingBot:
    """Main trading bot class"""
    
    def __init__(self):
        """Initialize the trading bot"""
        self.exchange = EXCHANGE
        self.trading_pair = TRADING_PAIR
        self.data_fetcher = MarketDataFetcher(self.exchange, API_KEY, API_SECRET)
        self.strategy = MovingAverageCrossover()
        self.trader = Trader(self.exchange, API_KEY, API_SECRET)
        self.is_running = False
        
        logger.info(f"Trading Bot initialized for {self.trading_pair} on {self.exchange}")
    
    def start(self):
        """Start the trading bot"""
        self.is_running = True
        logger.info("Starting trading bot...")
        
        try:
            while self.is_running:
                self.update()
        except KeyboardInterrupt:
            logger.info("Bot interrupted by user")
            self.stop()
        except Exception as e:
            logger.error(f"Error in bot loop: {str(e)}")
            self.stop()
    
    def update(self):
        """Update bot with latest market data and execute trades"""
        try:
            # Fetch latest market data
            ohlcv = self.data_fetcher.fetch_ohlcv(self.trading_pair)
            
            if ohlcv is None or len(ohlcv) == 0:
                logger.warning("No market data fetched")
                return
            
            # Analyze market with strategy
            signal = self.strategy.analyze(ohlcv)
            
            if signal == 'BUY':
                logger.info(f"BUY signal detected for {self.trading_pair}")
                self.trader.place_order(self.trading_pair, 'buy')
            
            elif signal == 'SELL':
                logger.info(f"SELL signal detected for {self.trading_pair}")
                self.trader.place_order(self.trading_pair, 'sell')
            
            else:
                logger.debug("No clear trading signal")
        
        except Exception as e:
            logger.error(f"Error during bot update: {str(e)}")
    
    def stop(self):
        """Stop the trading bot"""
        self.is_running = False
        logger.info("Trading bot stopped")

if __name__ == '__main__':
    bot = TradingBot()
    bot.start()
