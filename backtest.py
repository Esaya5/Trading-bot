#!/usr/bin/env python3
"""
Backtesting Module for Trading Bot

Usage:
    python backtest.py
"""

import logging
from datetime import datetime
from config.settings import (
    TRADING_PAIR, BACKTEST_START_DATE, BACKTEST_END_DATE,
    BACKTEST_INITIAL_BALANCE, LOG_LEVEL, LOG_FILE
)
from utils.logger import setup_logger
from data.fetcher import MarketDataFetcher
from bot.strategies import MovingAverageCrossover
from utils.helpers import calculate_percentage_change, format_currency

logger = setup_logger(__name__, LOG_LEVEL, str(LOG_FILE))

class Backtester:
    """Backtests trading strategies"""
    
    def __init__(self, initial_balance: float = 10000):
        """
        Initialize backtester
        
        Args:
            initial_balance: Initial balance for backtest
        """
        self.balance = initial_balance
        self.initial_balance = initial_balance
        self.position = 0  # Current position size
        self.trades = []  # List of executed trades
        self.equity_curve = []
    
    def run(self, symbol: str, ohlcv_data: list, strategy):
        """
        Run backtest on historical data
        
        Args:
            symbol: Trading pair
            ohlcv_data: Historical OHLCV data
            strategy: Trading strategy to test
        """
        logger.info(f"Starting backtest for {symbol}")
        logger.info(f"Initial Balance: {format_currency(self.balance)}")
        
        for i, candle in enumerate(ohlcv_data):
            time, open_p, high, low, close, volume = candle
            
            # Get trading signal
            signal = strategy.analyze(ohlcv_data[:i+1])
            
            if signal == 'BUY' and self.position == 0:
                # Execute buy
                self.position = self.balance / close
                self.balance = 0
                
                trade = {
                    'type': 'BUY',
                    'price': close,
                    'quantity': self.position,
                    'timestamp': time
                }
                self.trades.append(trade)
                logger.debug(f"BUY at {close}")
            
            elif signal == 'SELL' and self.position > 0:
                # Execute sell
                profit = self.position * close
                self.balance = profit
                
                trade = {
                    'type': 'SELL',
                    'price': close,
                    'quantity': self.position,
                    'timestamp': time
                }
                self.trades.append(trade)
                logger.debug(f"SELL at {close}")
                self.position = 0
            
            # Track equity
            current_equity = self.balance + (self.position * close if self.position > 0 else 0)
            self.equity_curve.append(current_equity)
        
        # Close any remaining position
        if self.position > 0:
            final_price = ohlcv_data[-1][4]
            self.balance = self.position * final_price
            self.position = 0
        
        self.print_results()
    
    def print_results(self):
        """
        Print backtest results
        """
        final_balance = self.balance
        profit = final_balance - self.initial_balance
        return_pct = calculate_percentage_change(self.initial_balance, final_balance)
        
        logger.info("\n" + "="*50)
        logger.info("BACKTEST RESULTS")
        logger.info("="*50)
        logger.info(f"Initial Balance: {format_currency(self.initial_balance)}")
        logger.info(f"Final Balance: {format_currency(final_balance)}")
        logger.info(f"Profit/Loss: {format_currency(profit)}")
        logger.info(f"Return: {return_pct:.2f}%")
        logger.info(f"Total Trades: {len(self.trades)}")
        logger.info(f"Buy Orders: {sum(1 for t in self.trades if t['type'] == 'BUY')}")
        logger.info(f"Sell Orders: {sum(1 for t in self.trades if t['type'] == 'SELL')}")
        logger.info("="*50 + "\n")

def main():
    """
    Main entry point for backtesting
    """
    logger.info("Backtest Starting...")
    
    # Note: In a real scenario, you would fetch historical data
    # For now, this is a template
    
    logger.info("Backtest template ready. Implement data fetching to run backtest.")

if __name__ == '__main__':
    main()
