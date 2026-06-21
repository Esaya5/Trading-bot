import logging
from typing import Optional
import ccxt
from config.settings import (
    TRADE_AMOUNT, STOP_LOSS, TAKE_PROFIT
)

logger = logging.getLogger(__name__)

class Trader:
    """Handles order placement and execution"""
    
    def __init__(self, exchange: str, api_key: str, api_secret: str):
        """
        Initialize Trader
        
        Args:
            exchange: Exchange name (e.g., 'binance')
            api_key: Exchange API key
            api_secret: Exchange API secret
        """
        self.exchange_name = exchange
        
        # Initialize exchange
        exchange_class = getattr(ccxt, exchange)
        self.exchange = exchange_class({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True
        })
        
        logger.info(f"Trader initialized for {exchange}")
    
    def place_order(self, symbol: str, side: str, amount: Optional[float] = None) -> bool:
        """
        Place a market order
        
        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            side: 'buy' or 'sell'
            amount: Order amount (uses TRADE_AMOUNT from config if not specified)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if amount is None:
                amount = TRADE_AMOUNT
            
            order = self.exchange.create_market_order(
                symbol,
                side,
                amount
            )
            
            logger.info(f"Order placed: {side.upper()} {amount} {symbol}")
            logger.debug(f"Order details: {order}")
            
            return True
        
        except Exception as e:
            logger.error(f"Error placing order: {str(e)}")
            return False
    
    def get_balance(self, symbol: Optional[str] = None) -> dict:
        """
        Get account balance
        
        Args:
            symbol: Specific symbol to get balance for (optional)
        
        Returns:
            Balance dictionary
        """
        try:
            balance = self.exchange.fetch_balance()
            
            if symbol:
                return {symbol: balance.get(symbol, {})}
            
            return balance
        
        except Exception as e:
            logger.error(f"Error fetching balance: {str(e)}")
            return {}
    
    def get_open_orders(self, symbol: Optional[str] = None) -> list:
        """
        Get open orders
        
        Args:
            symbol: Specific symbol (optional)
        
        Returns:
            List of open orders
        """
        try:
            orders = self.exchange.fetch_open_orders(symbol)
            return orders
        
        except Exception as e:
            logger.error(f"Error fetching open orders: {str(e)}")
            return []
    
    def cancel_order(self, order_id: str, symbol: str) -> bool:
        """
        Cancel an open order
        
        Args:
            order_id: Order ID
            symbol: Trading pair
        
        Returns:
            True if successful, False otherwise
        """
        try:
            self.exchange.cancel_order(order_id, symbol)
            logger.info(f"Order {order_id} cancelled")
            return True
        
        except Exception as e:
            logger.error(f"Error cancelling order: {str(e)}")
            return False
