import logging
import numpy as np
from typing import List, Optional

logger = logging.getLogger(__name__)

class MovingAverageCrossover:
    """Moving Average Crossover Strategy"""
    
    def __init__(self, fast_period: int = 10, slow_period: int = 20):
        """
        Initialize Moving Average Crossover strategy
        
        Args:
            fast_period: Period for fast moving average
            slow_period: Period for slow moving average
        """
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.previous_signal = None
    
    def analyze(self, ohlcv: List[List]) -> Optional[str]:
        """
        Analyze market data and generate trading signal
        
        Args:
            ohlcv: OHLCV data (list of [time, open, high, low, close, volume])
        
        Returns:
            'BUY', 'SELL', or None
        """
        if len(ohlcv) < self.slow_period:
            return None
        
        # Extract closing prices
        closes = np.array([candle[4] for candle in ohlcv])
        
        # Calculate moving averages
        fast_ma = np.mean(closes[-self.fast_period:])
        slow_ma = np.mean(closes[-self.slow_period:])
        
        # Generate signal
        if fast_ma > slow_ma and self.previous_signal != 'BUY':
            self.previous_signal = 'BUY'
            return 'BUY'
        
        elif fast_ma < slow_ma and self.previous_signal != 'SELL':
            self.previous_signal = 'SELL'
            return 'SELL'
        
        return None

class RSIStrategy:
    """Relative Strength Index Strategy"""
    
    def __init__(self, period: int = 14, oversold: float = 30, overbought: float = 70):
        """
        Initialize RSI strategy
        
        Args:
            period: RSI calculation period
            oversold: Oversold threshold
            overbought: Overbought threshold
        """
        self.period = period
        self.oversold = oversold
        self.overbought = overbought
    
    def calculate_rsi(self, closes: np.ndarray) -> float:
        """
        Calculate RSI indicator
        
        Args:
            closes: Array of closing prices
        
        Returns:
            RSI value
        """
        if len(closes) < self.period:
            return 50
        
        deltas = np.diff(closes[-self.period:])
        seed = deltas[:1]
        up = seed[seed >= 0].sum() / self.period
        down = -seed[seed < 0].sum() / self.period
        
        rs = up / down if down != 0 else 0
        rsi = 100 - 100 / (1 + rs)
        
        return rsi
    
    def analyze(self, ohlcv: List[List]) -> Optional[str]:
        """
        Analyze market data using RSI
        
        Args:
            ohlcv: OHLCV data
        
        Returns:
            'BUY', 'SELL', or None
        """
        closes = np.array([candle[4] for candle in ohlcv])
        rsi = self.calculate_rsi(closes)
        
        if rsi < self.oversold:
            return 'BUY'
        elif rsi > self.overbought:
            return 'SELL'
        
        return None
