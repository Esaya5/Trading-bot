from datetime import datetime
from typing import List, Dict, Any

def format_datetime(dt: datetime) -> str:
    """
    Format datetime object to string
    
    Args:
        dt: Datetime object
    
    Returns:
        Formatted string
    """
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def calculate_percentage_change(start: float, end: float) -> float:
    """
    Calculate percentage change
    
    Args:
        start: Starting value
        end: Ending value
    
    Returns:
        Percentage change
    """
    if start == 0:
        return 0.0
    return ((end - start) / start) * 100

def calculate_profit_loss(
    entry_price: float,
    exit_price: float,
    quantity: float
) -> float:
    """
    Calculate profit/loss
    
    Args:
        entry_price: Entry price
        exit_price: Exit price
        quantity: Quantity traded
    
    Returns:
        Profit/loss amount
    """
    return (exit_price - entry_price) * quantity

def format_currency(amount: float, decimals: int = 2) -> str:
    """
    Format number as currency
    
    Args:
        amount: Amount
        decimals: Decimal places
    
    Returns:
        Formatted currency string
    """
    return f"${amount:,.{decimals}f}"
