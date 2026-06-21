#!/usr/bin/env python3
"""
Trading Bot Main Entry Point

Usage:
    python main.py
"""

import logging
from bot.bot import TradingBot
from utils.logger import setup_logger
from config.settings import LOG_LEVEL, LOG_FILE

# Setup logger
logger = setup_logger(__name__, LOG_LEVEL, str(LOG_FILE))

def main():
    """
    Main entry point for the trading bot
    """
    logger.info("="*50)
    logger.info("Trading Bot Starting...")
    logger.info("="*50)
    
    try:
        # Initialize and start bot
        bot = TradingBot()
        bot.start()
    
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        raise

if __name__ == '__main__':
    main()
