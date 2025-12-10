"""
Main trading bot logic
"""
import time
from typing import List, Optional
from .api_client import ManifoldAPIClient
from .strategies.base_strategy import BaseStrategy, StrategySignal
from .utils import calculate_kelly_bet, format_market_summary


class ManifoldBot:
    """Main trading bot for Manifold Markets"""

    def __init__(
        self,
        api_key: str,
        target_user: str = "MikhailTal",
        max_bet_amount: float = 100,
        min_confidence: float = 0.6,
        poll_interval: int = 300,
        dry_run: bool = False
    ):
        """
        Initialize the trading bot.

        Args:
            api_key: Manifold Markets API key
            target_user: Username to target markets from
            max_bet_amount: Maximum bet size in Mana
            min_confidence: Minimum confidence threshold to place bets
            poll_interval: Seconds between market checks
            dry_run: If True, don't place actual bets
        """
        self.client = ManifoldAPIClient(api_key)
        self.target_user = target_user
        self.max_bet_amount = max_bet_amount
        self.min_confidence = min_confidence
        self.poll_interval = poll_interval
        self.dry_run = dry_run

        self.strategies: List[BaseStrategy] = []
        self.processed_markets = set()

        print(f"Bot initialized - Target: {target_user}, Max bet: M${max_bet_amount}")
        print(f"Dry run mode: {dry_run}")

    def add_strategy(self, strategy: BaseStrategy):
        """Add a trading strategy to the bot"""
        self.strategies.append(strategy)
        print(f"Added strategy: {strategy.name}")

    def run(self, max_iterations: Optional[int] = None):
        """
        Run the bot continuously.

        Args:
            max_iterations: Optional limit on iterations (for testing)
        """
        if not self.strategies:
            raise ValueError("No strategies added. Add at least one strategy before running.")

        print(f"\n{'='*60}")
        print(f"Starting bot - monitoring {self.target_user}'s markets")
        print(f"{'='*60}\n")

        iteration = 0
        while True:
            try:
                if max_iterations and iteration >= max_iterations:
                    print("Reached max iterations, stopping.")
                    break

                iteration += 1
                print(f"\n--- Iteration {iteration} ---")
                self._check_markets()
                print(f"Sleeping for {self.poll_interval} seconds...")
                time.sleep(self.poll_interval)

            except KeyboardInterrupt:
                print("\n\nBot stopped by user.")
                break
            except Exception as e:
                print(f"Error in main loop: {e}")
                print("Continuing after 60 seconds...")
                time.sleep(60)

    def _check_markets(self):
        """Check target user's markets and process them"""
        try:
            markets = self.client.get_user_markets(self.target_user, limit=50)
            print(f"Found {len(markets)} markets by {self.target_user}")

            new_markets = [m for m in markets if m["id"] not in self.processed_markets]
            print(f"New markets to analyze: {len(new_markets)}")

            for market in new_markets:
                self._process_market(market)
                self.processed_markets.add(market["id"])

        except Exception as e:
            print(f"Error checking markets: {e}")

    def _process_market(self, market: dict):
        """Process a single market"""
        print(f"\n{'-'*60}")
        print(format_market_summary(market))
        print(f"{'-'*60}")

        # Skip if market is closed or resolved
        if market.get("isResolved", False) or market.get("closeTime", float("inf")) < time.time() * 1000:
            print("Market is closed or resolved, skipping.")
            return

        # Only process binary markets for now
        if market.get("outcomeType") != "BINARY":
            print(f"Skipping non-binary market (type: {market.get('outcomeType')})")
            return

        # Run all strategies
        signals = []
        for strategy in self.strategies:
            try:
                signal = strategy.analyze(market)
                signals.append((strategy, signal))
                print(f"\n{strategy.name}:")
                print(f"  Should bet: {signal.should_bet}")
                print(f"  Outcome: {signal.outcome}")
                print(f"  Confidence: {signal.confidence:.1%}")
                print(f"  Est. probability: {signal.estimated_probability:.1%}")
                print(f"  Reasoning: {signal.reasoning}")
            except Exception as e:
                print(f"Error in strategy {strategy.name}: {e}")

        # Decide whether to bet based on signals
        self._execute_trades(market, signals)

    def _execute_trades(self, market: dict, signals: List[tuple]):
        """Execute trades based on strategy signals"""
        # Simple consensus: bet if any strategy says to bet with sufficient confidence
        for strategy, signal in signals:
            if signal.should_bet and signal.confidence >= self.min_confidence:
                self._place_bet(market, signal, strategy)
                return  # Only place one bet per market for now

        print("\nNo trade signal met confidence threshold.")

    def _place_bet(self, market: dict, signal: StrategySignal, strategy: BaseStrategy):
        """Place a bet on a market"""
        current_prob = market.get("probability", 0.5)

        # Calculate bet size using Kelly criterion
        bet_size = calculate_kelly_bet(
            probability=signal.estimated_probability,
            market_prob=current_prob,
            bankroll=1000,  # Could track actual bankroll
            max_bet=self.max_bet_amount,
            fraction=0.25
        )

        if bet_size < 1:
            print(f"\nBet size too small (M${bet_size:.2f}), skipping.")
            return

        print(f"\n{'='*60}")
        print(f"TRADE SIGNAL - {strategy.name}")
        print(f"Market: {market['question']}")
        print(f"Outcome: {signal.outcome}")
        print(f"Bet size: M${bet_size:.2f}")
        print(f"Confidence: {signal.confidence:.1%}")
        print(f"{'='*60}")

        if self.dry_run:
            print("[DRY RUN] Bet not placed (dry run mode)")
            return

        try:
            result = self.client.place_bet(
                contract_id=market["id"],
                amount=bet_size,
                outcome=signal.outcome
            )
            print(f"Bet placed successfully! Bet ID: {result.get('id', 'unknown')}")
        except Exception as e:
            print(f"Error placing bet: {e}")
