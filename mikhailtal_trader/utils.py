"""
Utility functions for the trading bot
"""
import os
from dotenv import load_dotenv
from typing import Optional


def load_config() -> dict:
    """
    Load configuration from environment variables.

    Returns:
        Dictionary of configuration values
    """
    load_dotenv()

    config = {
        "manifold_api_key": os.getenv("MANIFOLD_API_KEY"),
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "anthropic_api_key": os.getenv("ANTHROPIC_API_KEY"),
        "bot_username": os.getenv("BOT_USERNAME"),
        "target_user": os.getenv("TARGET_USER", "MikhailTal"),
        "max_bet_amount": float(os.getenv("MAX_BET_AMOUNT", "100")),
        "min_confidence": float(os.getenv("MIN_CONFIDENCE", "0.6")),
        "poll_interval": int(os.getenv("POLL_INTERVAL_SECONDS", "300")),
    }

    # Validate required keys
    if not config["manifold_api_key"]:
        raise ValueError("MANIFOLD_API_KEY is required in .env file")

    return config


def calculate_kelly_bet(
    probability: float,
    market_prob: float,
    bankroll: float,
    max_bet: float,
    fraction: float = 0.25
) -> float:
    """
    Calculate bet size using fractional Kelly criterion.

    Args:
        probability: Estimated true probability (0-1)
        market_prob: Current market probability (0-1)
        bankroll: Available bankroll
        max_bet: Maximum bet amount
        fraction: Kelly fraction (default 0.25 for quarter Kelly)

    Returns:
        Recommended bet size
    """
    if probability <= market_prob or probability <= 0 or probability >= 1:
        return 0

    # Kelly formula: f = (bp - q) / b
    # where b = odds, p = win probability, q = 1-p
    b = (1 - market_prob) / market_prob  # Odds
    kelly_fraction = (b * probability - (1 - probability)) / b

    # Apply fractional Kelly for safety
    bet_size = kelly_fraction * fraction * bankroll

    # Cap at max_bet
    return min(max(bet_size, 0), max_bet)


def format_market_summary(market: dict) -> str:
    """
    Format market data into a readable summary.

    Args:
        market: Market dictionary from API

    Returns:
        Formatted string summary
    """
    question = market.get("question", "Unknown")
    prob = market.get("probability", 0)
    volume = market.get("volume", 0)
    creator = market.get("creatorUsername", "Unknown")

    return f"""
Market: {question}
Creator: {creator}
Current Probability: {prob:.1%}
Volume: M${volume:.0f}
    """.strip()
