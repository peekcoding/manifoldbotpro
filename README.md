# MikhailTal Trader Bot

An intelligent trading bot for Manifold Markets that trades exclusively on markets created by user [MikhailTal](https://manifold.markets/MikhailTal).

## Features

- **Targeted Trading**: Only trades on MikhailTal's markets
- **AI-Powered Analysis**: Uses LLMs (OpenAI/Claude) to analyze market questions
- **Smart Strategies**: Multiple trading strategies including:
  - LLM-based probability estimation
  - Sentiment analysis
  - Pattern recognition
- **Risk Management**: Configurable bet sizing and confidence thresholds
- **Clean Architecture**: Well-structured, maintainable Python code

## Installation

1. Clone the repository:
```bash
git clone https://github.com/peekcoding/manifoldbotpro.git
cd mikhailtal-trader
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys
```

## Configuration

Edit `.env` file with your credentials:

- `MANIFOLD_API_KEY`: Your Manifold Markets API key (required)
- `OPENAI_API_KEY`: OpenAI API key (optional, for GPT strategies)
- `BOT_USERNAME`: Your bot's Manifold username
- `MAX_BET_AMOUNT`: Maximum bet size in Mana (default: 100)
- `MIN_CONFIDENCE`: Minimum confidence to place bet (default: 0.6)

## Usage

### Basic Usage

```bash
python examples/run_bot.py
```

### Advanced Usage

```python
from mikhailtal_trader import ManifoldBot
from mikhailtal_trader.strategies import LLMStrategy

# Initialize bot
bot = ManifoldBot(api_key="your_api_key")

# Add strategy
strategy = LLMStrategy(model="gpt-4")
bot.add_strategy(strategy)

# Run bot
bot.run()
```

## Trading Strategies

### 1. LLM Strategy
Uses large language models to analyze market questions and estimate probabilities.

### 2. Sentiment Strategy
Analyzes market description and comments for sentiment signals.

### 3. Pattern Strategy
Identifies patterns in market behavior and historical data.

## Development

### Project Structure

```
mikhailtal-trader/
├── mikhailtal_trader/       # Main package
│   ├── api_client.py        # Manifold API client
│   ├── bot.py               # Core bot logic
│   ├── strategies/          # Trading strategies
│   │   ├── base_strategy.py
│   │   └── llm_strategy.py
│   └── utils.py             # Utility functions
├── tests/                   # Test suite
├── examples/                # Example scripts
└── README.md
```

### Running Tests

```bash
pytest tests/
```

## Contributing

Contributions welcome! This project aims to:
- Improve upon manifoldbot patterns
- Demonstrate clean, maintainable code
- Achieve profitable trading performance

## Demo In video
[Download Video](https://drive.google.com/file/d/1R8TSFK5jbiUyo32x5F6Fe6pIzozCTf1-/view?usp=sharing)


## License

MIT License

## Acknowledgments

Built on insights from [manifoldbot](https://github.com/microprediction/manifoldbot) by Peter Cotton.
