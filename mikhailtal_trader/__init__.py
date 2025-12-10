"""
MikhailTal Trader - A trading bot for Manifold Markets
"""

from .bot import ManifoldBot
from .api_client import ManifoldAPIClient

__version__ = "0.1.0"
__all__ = ["ManifoldBot", "ManifoldAPIClient"]
