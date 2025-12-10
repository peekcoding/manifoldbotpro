"""
Example script to run the trading bot
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mikhailtal_trader import ManifoldBot
from mikhailtal_trader.strategies import LLMStrategy
from mikhailtal_trader.utils import load_config


def main():
    """Run the trading bot"""
    print("Loading configuration...")
    config = load_config()

    print(f"Target user: {config['target_user']}")
    print(f"Max bet amount: M${config['max_bet_amount']}")
    print(f"Min confidence: {config['min_confidence']:.1%}")

    # Initialize bot
    bot = ManifoldBot(
        api_key=config["manifold_api_key"],
        target_user=config["target_user"],
        max_bet_amount=config["max_bet_amount"],
        min_confidence=config["min_confidence"],
        poll_interval=config["poll_interval"],
        dry_run=False  # Set to False to place real bets
    )

    # Add OpenAI strategy
    print("Adding GPT strategy...")
    strategy = LLMStrategy(
        name="GPT-4o-mini Strategy",
        model="gpt-4o-mini",
        api_key=config["openai_api_key"]
    )
    bot.add_strategy(strategy)

    # Run bot
    print("\nStarting bot...")
    print("Press Ctrl+C to stop\n")

    try:
        bot.run()
    except KeyboardInterrupt:
        print("\n\nBot stopped.")


if __name__ == "__main__":
    main()
