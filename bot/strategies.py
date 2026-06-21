import logging
import numpy as np
from typing import List, Optional, Tuple

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


class MACDStrategy:
    """MACD (Moving Average Convergence Divergence) Strategy"""
    
    def __init__(self, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9):
        """
        Initialize MACD strategy
        
        Args:
            fast_period: Fast EMA period
            slow_period: Slow EMA period
            signal_period: Signal line EMA period
        """
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
        self.previous_signal = None
    
    def calculate_ema(self, data: np.ndarray, period: int) -> np.ndarray:
        """Calculate Exponential Moving Average"""
        if len(data) == 0:
            return np.array([])
        
        ema = np.zeros(len(data))
        ema[0] = data[0]
        multiplier = 2 / (period + 1)
        
        for i in range(1, len(data)):
            ema[i] = data[i] * multiplier + ema[i-1] * (1 - multiplier)
        
        return ema
    
    def analyze(self, ohlcv: List[List]) -> Optional[str]:
        """
        Analyze market data using MACD
        
        Args:
            ohlcv: OHLCV data
        
        Returns:
            'BUY', 'SELL', or None
        """
        if len(ohlcv) < self.slow_period + self.signal_period:
            return None
        
        closes = np.array([candle[4] for candle in ohlcv])
        
        # Calculate EMAs
        fast_ema = self.calculate_ema(closes, self.fast_period)
        slow_ema = self.calculate_ema(closes, self.slow_period)
        
        # Calculate MACD line
        macd_line = fast_ema - slow_ema
        
        # Calculate signal line
        signal_line = self.calculate_ema(macd_line, self.signal_period)
        
        # Generate signal based on crossover
        if len(macd_line) >= 2 and len(signal_line) >= 2:
            prev_diff = macd_line[-2] - signal_line[-2]
            curr_diff = macd_line[-1] - signal_line[-1]
            
            if prev_diff <= 0 and curr_diff > 0 and self.previous_signal != 'BUY':
                self.previous_signal = 'BUY'
                return 'BUY'
            elif prev_diff >= 0 and curr_diff < 0 and self.previous_signal != 'SELL':
                self.previous_signal = 'SELL'
                return 'SELL'
        
        return None


class BollingerBandsStrategy:
    """Bollinger Bands Strategy"""
    
    def __init__(self, period: int = 20, num_std_dev: float = 2.0):
        """
        Initialize Bollinger Bands strategy
        
        Args:
            period: SMA period
            num_std_dev: Number of standard deviations for bands
        """
        self.period = period
        self.num_std_dev = num_std_dev
    
    def analyze(self, ohlcv: List[List]) -> Optional[str]:
        """
        Analyze market data using Bollinger Bands
        
        Args:
            ohlcv: OHLCV data
        
        Returns:
            'BUY', 'SELL', or None
        """
        if len(ohlcv) < self.period:
            return None
        
        closes = np.array([candle[4] for candle in ohlcv])
        
        # Calculate SMA (middle band)
        sma = np.mean(closes[-self.period:])
        
        # Calculate standard deviation
        std_dev = np.std(closes[-self.period:])
        
        # Calculate bands
        upper_band = sma + (std_dev * self.num_std_dev)
        lower_band = sma - (std_dev * self.num_std_dev)
        
        current_price = closes[-1]
        
        # Generate signal
        if current_price < lower_band:
            return 'BUY'
        elif current_price > upper_band:
            return 'SELL'
        
        return None


class StochasticStrategy:
    """Stochastic Oscillator Strategy"""
    
    def __init__(self, period: int = 14, smooth_k: int = 3, smooth_d: int = 3, 
                 oversold: float = 20, overbought: float = 80):
        """
        Initialize Stochastic strategy
        
        Args:
            period: Stochastic period
            smooth_k: K line smoothing period
            smooth_d: D line smoothing period
            oversold: Oversold threshold
            overbought: Overbought threshold
        """
        self.period = period
        self.smooth_k = smooth_k
        self.smooth_d = smooth_d
        self.oversold = oversold
        self.overbought = overbought
    
    def calculate_stochastic(self, ohlcv: List[List]) -> Tuple[Optional[float], Optional[float]]:
        """
        Calculate Stochastic K and D lines
        
        Args:
            ohlcv: OHLCV data
        
        Returns:
            Tuple of (K value, D value) or (None, None) if insufficient data
        """
        if len(ohlcv) < self.period:
            return None, None
        
        highs = np.array([candle[2] for candle in ohlcv[-self.period:]])
        lows = np.array([candle[3] for candle in ohlcv[-self.period:]])
        closes = np.array([candle[4] for candle in ohlcv[-self.period:]])
        
        highest_high = np.max(highs)
        lowest_low = np.min(lows)
        
        if highest_high == lowest_low:
            return 50.0, 50.0
        
        # Calculate raw K
        k_raw = ((closes[-1] - lowest_low) / (highest_high - lowest_low)) * 100
        
        # For this simple version, we use current K as smoothed K
        k_value = k_raw
        d_value = k_raw  # In real implementation, D is SMA of K
        
        return k_value, d_value
    
    def analyze(self, ohlcv: List[List]) -> Optional[str]:
        """
        Analyze market data using Stochastic
        
        Args:
            ohlcv: OHLCV data
        
        Returns:
            'BUY', 'SELL', or None
        """
        k_value, d_value = self.calculate_stochastic(ohlcv)
        
        if k_value is None:
            return None
        
        if k_value < self.oversold:
            return 'BUY'
        elif k_value > self.overbought:
            return 'SELL'
        
        return None


class IchimokuStrategy:
    """Ichimoku Cloud Strategy"""
    
    def __init__(self, tenkan_period: int = 9, kijun_period: int = 26, 
                 senkou_b_period: int = 52, senkou_displacement: int = 26):
        """
        Initialize Ichimoku strategy
        
        Args:
            tenkan_period: Tenkan line period (9)
            kijun_period: Kijun line period (26)
            senkou_b_period: Senkou B period (52)
            senkou_displacement: Displacement for Senkou spans (26)
        """
        self.tenkan_period = tenkan_period
        self.kijun_period = kijun_period
        self.senkou_b_period = senkou_b_period
        self.senkou_displacement = senkou_displacement
    
    def calculate_ichimoku_lines(self, ohlcv: List[List]) -> dict:
        """
        Calculate Ichimoku lines
        
        Args:
            ohlcv: OHLCV data
        
        Returns:
            Dictionary with Ichimoku values
        """
        if len(ohlcv) < self.senkou_b_period:
            return {}
        
        highs = np.array([candle[2] for candle in ohlcv])
        lows = np.array([candle[3] for candle in ohlcv])
        
        # Tenkan (Conversion Line)
        tenkan_high = np.max(highs[-self.tenkan_period:])
        tenkan_low = np.min(lows[-self.tenkan_period:])
        tenkan = (tenkan_high + tenkan_low) / 2
        
        # Kijun (Base Line)
        kijun_high = np.max(highs[-self.kijun_period:])
        kijun_low = np.min(lows[-self.kijun_period:])
        kijun = (kijun_high + kijun_low) / 2
        
        # Senkou Span A
        senkou_a = (tenkan + kijun) / 2
        
        # Senkou Span B
        senkou_b_high = np.max(highs[-self.senkou_b_period:])
        senkou_b_low = np.min(lows[-self.senkou_b_period:])
        senkou_b = (senkou_b_high + senkou_b_low) / 2
        
        # Chikou (Lagging Span)
        current_close = ohlcv[-1][4]
        
        return {
            'tenkan': tenkan,
            'kijun': kijun,
            'senkou_a': senkou_a,
            'senkou_b': senkou_b,
            'close': current_close
        }
    
    def analyze(self, ohlcv: List[List]) -> Optional[str]:
        """
        Analyze market data using Ichimoku
        
        Args:
            ohlcv: OHLCV data
        
        Returns:
            'BUY', 'SELL', or None
        """
        lines = self.calculate_ichimoku_lines(ohlcv)
        
        if not lines:
            return None
        
        # Bullish signal: Price above cloud, Tenkan > Kijun
        if (lines['close'] > lines['senkou_a'] and 
            lines['close'] > lines['senkou_b'] and 
            lines['tenkan'] > lines['kijun']):
            return 'BUY'
        
        # Bearish signal: Price below cloud, Tenkan < Kijun
        elif (lines['close'] < lines['senkou_a'] and 
              lines['close'] < lines['senkou_b'] and 
              lines['tenkan'] < lines['kijun']):
            return 'SELL'
        
        return None


class CombinedStrategy:
    """
    Combined strategy using multiple indicators
    Requires confirmation from at least 2 strategies
    """
    
    def __init__(self):
        """Initialize combined strategy with multiple indicators"""
        self.strategies = {
            'macd': MACDStrategy(),
            'bollinger': BollingerBandsStrategy(),
            'rsi': RSIStrategy(),
            'stochastic': StochasticStrategy()
        }
    
    def analyze(self, ohlcv: List[List]) -> Optional[str]:
        """
        Analyze market data using multiple strategies
        
        Args:
            ohlcv: OHLCV data
        
        Returns:
            'BUY', 'SELL', or None (only if multiple strategies agree)
        """
        signals = {}
        buy_count = 0
        sell_count = 0
        
        for name, strategy in self.strategies.items():
            signal = strategy.analyze(ohlcv)
            if signal:
                signals[name] = signal
                if signal == 'BUY':
                    buy_count += 1
                elif signal == 'SELL':
                    sell_count += 1
        
        # Require at least 2 agreements
        if buy_count >= 2:
            logger.debug(f"Combined BUY signal: {signals}")
            return 'BUY'
        elif sell_count >= 2:
            logger.debug(f"Combined SELL signal: {signals}")
            return 'SELL'
        
        return None
