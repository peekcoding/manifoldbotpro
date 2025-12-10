"""
Manifold Markets API Client
"""
import requests
from typing import Dict, List, Optional, Any
import time


class ManifoldAPIClient:
    """Client for interacting with Manifold Markets API"""

    BASE_URL = "https://api.manifold.markets/v0"

    def __init__(self, api_key: str):
        """
        Initialize the API client.

        Args:
            api_key: Manifold Markets API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Key {api_key}",
            "Content-Type": "application/json"
        })
        self.request_count = 0
        self.last_request_time = time.time()

    def _rate_limit(self):
        """Simple rate limiting to stay under 500 req/min"""
        self.request_count += 1
        current_time = time.time()

        # Reset counter every minute
        if current_time - self.last_request_time > 60:
            self.request_count = 0
            self.last_request_time = current_time

        # If approaching limit, wait
        if self.request_count > 450:
            time.sleep(60 - (current_time - self.last_request_time))
            self.request_count = 0
            self.last_request_time = time.time()

    def get_user_markets(self, username: str, limit: int = 100) -> List[Dict[str, Any]]:
        """
        Get markets created by a specific user.

        Args:
            username: Username of the market creator
            limit: Maximum number of markets to return

        Returns:
            List of market dictionaries
        """
        self._rate_limit()

        # First, get user ID from username
        user_response = self.session.get(f"{self.BASE_URL}/user/{username}")
        user_response.raise_for_status()
        user_data = user_response.json()
        user_id = user_data.get("id")

        if not user_id:
            raise ValueError(f"User {username} not found")

        # Get markets by user ID
        self._rate_limit()
        params = {
            "userId": user_id,
            "limit": limit
        }

        response = self.session.get(f"{self.BASE_URL}/markets", params=params)
        response.raise_for_status()
        return response.json()

    def get_market(self, market_id: str) -> Dict[str, Any]:
        """
        Get details for a specific market.

        Args:
            market_id: Market ID

        Returns:
            Market data dictionary
        """
        self._rate_limit()
        response = self.session.get(f"{self.BASE_URL}/market/{market_id}")
        response.raise_for_status()
        return response.json()

    def get_market_probability(self, market_id: str) -> float:
        """
        Get current probability for a market.

        Args:
            market_id: Market ID

        Returns:
            Current probability (0-1)
        """
        self._rate_limit()
        response = self.session.get(f"{self.BASE_URL}/market/{market_id}/prob")
        response.raise_for_status()
        data = response.json()
        return data.get("prob", 0.5)

    def place_bet(
        self,
        contract_id: str,
        amount: float,
        outcome: str = "YES",
        limit_prob: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Place a bet on a market.

        Args:
            contract_id: Market contract ID
            amount: Bet amount in Mana
            outcome: "YES" or "NO"
            limit_prob: Optional limit probability for limit orders

        Returns:
            Bet confirmation data
        """
        self._rate_limit()

        payload = {
            "contractId": contract_id,
            "amount": amount,
            "outcome": outcome
        }

        if limit_prob is not None:
            payload["limitProb"] = limit_prob

        response = self.session.post(f"{self.BASE_URL}/bet", json=payload)
        response.raise_for_status()
        return response.json()

    def get_bets(self, username: Optional[str] = None, contract_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get bets by user or market.

        Args:
            username: Filter by username
            contract_id: Filter by contract ID

        Returns:
            List of bet dictionaries
        """
        self._rate_limit()

        params = {}
        if username:
            params["username"] = username
        if contract_id:
            params["contractId"] = contract_id

        response = self.session.get(f"{self.BASE_URL}/bets", params=params)
        response.raise_for_status()
        return response.json()

    def search_markets(
        self,
        term: Optional[str] = None,
        creator_id: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Search markets with filters.

        Args:
            term: Search term
            creator_id: Filter by creator ID
            limit: Maximum results

        Returns:
            List of market dictionaries
        """
        self._rate_limit()

        params = {"limit": limit}
        if term:
            params["term"] = term
        if creator_id:
            params["creatorId"] = creator_id

        response = self.session.get(f"{self.BASE_URL}/search-markets", params=params)
        response.raise_for_status()
        return response.json()
