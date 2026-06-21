import logging
import numpy as np
from typing import List, Tuple

logger = logging.getLogger(__name__)

class MarketAnalyzer:
    """Analyzes market data"""
    
    @staticmethod
    def calculate_sma(data: List[float], period: int) -> List[float]:
        """
        Calculate Simple Moving Average
        
        Args:
            data: Price data
            period: MA period
        
        Returns:
            SMA values
        """
        return np.convolve(data, np.ones(period)/period, mode='valid').tolist()
    
    @staticmethod
    def calculate_ema(data: List[float], period: int) -> List[float]:
        """
        Calculate Exponential Moving Average
        
        Args:
            data: Price data
            period: EMA period
        
        Returns:
            EMA values
        """
        ema = []
        multiplier = 2 / (period + 1)
        ema.append(np.mean(data[:period]))
        
        for price in data[period:]:
            ema_value = price * multiplier + ema[-1] * (1 - multiplier)
            ema.append(ema_value)
        
        return ema
    
    @staticmethod
    def calculate_volatility(data: List[float], period: int = 20) -> float:
        """
        Calculate price volatility (standard deviation)
        
        Args:
            data: Price data
            period: Period for calculation
        
        Returns:
            Volatility value
        """
        if len(data) < period:
            return 0.0
        
        returns = np.diff(data[-period:]) / data[-period:-1]
        volatility = np.std(returns)
        
        return float(volatility)
    
    @staticmethod
    def calculate_rsi(data: List[float], period: int = 14) -> float:
        """
        Calculate Relative Strength Index
        
        Args:
            data: Price data
            period: RSI period
        
        Returns:
            RSI value
        """
        if len(data) < period:
            return 50.0
        
        deltas = np.diff(data[-period:])
        seed = deltas[:1]
        up = seed[seed >= 0].sum() / period
        down = -seed[seed < 0].sum() / period
        
        rs = up / down if down != 0 else 0
        rsi = 100 - 100 / (1 + rs)
        
        return float(rsi)
