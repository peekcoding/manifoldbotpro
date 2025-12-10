"""
Base strategy class for all trading strategies
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class StrategySignal:
    """Signal from a trading strategy"""

    should_bet: bool
    outcome: str  # "YES" or "NO"
    confidence: float  # 0-1
    estimated_probability: float  # 0-1
    reasoning: str
    suggested_amount: Optional[float] = None


class BaseStrategy(ABC):
    """Abstract base class for trading strategies"""

    def __init__(self, name: str):
        """
        Initialize strategy.

        Args:
            name: Strategy name
        """
        self.name = name

    @abstractmethod
    def analyze(self, market: dict) -> StrategySignal:
        """
        Analyze a market and return a trading signal.

        Args:
            market: Market data dictionary

        Returns:
            StrategySignal with trading recommendation
        """
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name='{self.name}')"
