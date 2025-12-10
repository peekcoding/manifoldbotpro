"""
LLM-based trading strategy using OpenAI or Anthropic models
"""
import os
from typing import Optional, Literal
from .base_strategy import BaseStrategy, StrategySignal


class LLMStrategy(BaseStrategy):
    """Strategy that uses LLMs to analyze markets"""

    def __init__(
        self,
        name: str = "LLM Strategy",
        provider: Literal["openai", "anthropic"] = "openai",
        model: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        Initialize LLM strategy.

        Args:
            name: Strategy name
            provider: "openai" or "anthropic"
            model: Model name (defaults to gpt-4 or claude-3-sonnet)
            api_key: API key (if not in env)
        """
        super().__init__(name)
        self.provider = provider
        self.api_key = api_key

        if provider == "openai":
            self.model = model or "gpt-4o-mini"
            self._init_openai()
        elif provider == "anthropic":
            self.model = model or "claude-3-5-sonnet-20241022"
            self._init_anthropic()
        else:
            raise ValueError(f"Unknown provider: {provider}")

    def _init_openai(self):
        """Initialize OpenAI client"""
        try:
            from openai import OpenAI
            api_key = self.api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OpenAI API key required")
            self.client = OpenAI(api_key=api_key)
        except ImportError:
            raise ImportError("openai package required. Install with: pip install openai")

    def _init_anthropic(self):
        """Initialize Anthropic client"""
        try:
            from anthropic import Anthropic
            api_key = self.api_key or os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("Anthropic API key required")
            self.client = Anthropic(api_key=api_key)
        except ImportError:
            raise ImportError("anthropic package required. Install with: pip install anthropic")

    def analyze(self, market: dict) -> StrategySignal:
        """
        Analyze market using LLM.

        Args:
            market: Market data dictionary

        Returns:
            StrategySignal with trading recommendation
        """
        question = market.get("question", "")
        description = market.get("description", "")
        current_prob = market.get("probability", 0.5)

        prompt = self._build_prompt(question, description, current_prob)

        try:
            if self.provider == "openai":
                response = self._query_openai(prompt)
            else:
                response = self._query_anthropic(prompt)

            return self._parse_response(response, current_prob)

        except Exception as e:
            print(f"Error analyzing market with LLM: {e}")
            return StrategySignal(
                should_bet=False,
                outcome="YES",
                confidence=0.0,
                estimated_probability=current_prob,
                reasoning=f"Error: {str(e)}"
            )

    def _build_prompt(self, question: str, description: str, current_prob: float) -> str:
        """Build analysis prompt"""
        return f"""Analyze this prediction market and estimate the probability of YES.

Question: {question}

Description: {description}

Current market probability: {current_prob:.1%}

Please provide:
1. Your estimated probability of YES (0-100%)
2. Your confidence in this estimate (0-100%)
3. Brief reasoning (2-3 sentences)

Respond in this exact format:
PROBABILITY: [number]
CONFIDENCE: [number]
REASONING: [your reasoning]

Example:
PROBABILITY: 65
CONFIDENCE: 75
REASONING: Based on historical data and current trends, the outcome is more likely than not. However, there is uncertainty due to external factors that could change the situation.
"""

    def _query_openai(self, prompt: str) -> str:
        """Query OpenAI API"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are an expert prediction market analyst. Provide objective probability estimates based on facts and reasoning."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content

    def _query_anthropic(self, prompt: str) -> str:
        """Query Anthropic API"""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.content[0].text

    def _parse_response(self, response: str, current_prob: float) -> StrategySignal:
        """Parse LLM response into StrategySignal"""
        try:
            lines = response.strip().split("\n")
            probability = None
            confidence = None
            reasoning = ""

            for line in lines:
                if line.startswith("PROBABILITY:"):
                    probability = float(line.split(":")[1].strip()) / 100
                elif line.startswith("CONFIDENCE:"):
                    confidence = float(line.split(":")[1].strip()) / 100
                elif line.startswith("REASONING:"):
                    reasoning = line.split(":", 1)[1].strip()

            if probability is None or confidence is None:
                raise ValueError("Could not parse probability or confidence")

            # Determine if we should bet
            prob_diff = abs(probability - current_prob)
            should_bet = prob_diff >= 0.05 and confidence >= 0.6

            # Determine outcome
            outcome = "YES" if probability > current_prob else "NO"

            return StrategySignal(
                should_bet=should_bet,
                outcome=outcome,
                confidence=confidence,
                estimated_probability=probability,
                reasoning=reasoning
            )

        except Exception as e:
            print(f"Error parsing LLM response: {e}")
            print(f"Response was: {response}")
            return StrategySignal(
                should_bet=False,
                outcome="YES",
                confidence=0.0,
                estimated_probability=current_prob,
                reasoning=f"Parse error: {str(e)}"
            )
