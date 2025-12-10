# Setup Guide

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Get Your Manifold API Key

1. Go to https://manifold.markets
2. Create an account (or login)
3. Visit your profile page
4. Click "Edit Profile"
5. Find the "API Key" section and click "Refresh" to generate a new key
6. Copy the API key

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```
MANIFOLD_API_KEY=your_actual_api_key_here
OPENAI_API_KEY=your_openai_key_here  # Optional
BOT_USERNAME=your_manifold_username
```

### 4. Test in Dry-Run Mode

```bash
python examples/run_bot.py
```

The bot will run in dry-run mode by default (no real bets placed).

### 5. Run for Real

Edit `examples/run_bot.py` and change:
```python
dry_run=True  # Change to False
```

Then run:
```bash
python examples/run_bot.py
```

## What It Does

1. Fetches all markets created by MikhailTal
2. Analyzes each market using AI (GPT or Claude)
3. Estimates probability and confidence
4. Places bets when:
   - Probability differs from market by >5%
   - Confidence is >60%
5. Uses Kelly criterion for bet sizing

## Monitoring

The bot will print:
- Markets found
- Analysis results
- Trading decisions
- Bet confirmations

Press `Ctrl+C` to stop the bot at any time.

## Tips

- Start with small `MAX_BET_AMOUNT` (e.g., 10-50 Mana)
- Use `MIN_CONFIDENCE` of 0.6 or higher
- Monitor the bot for first few hours
- Check your bets at https://manifold.markets/profile

## Troubleshooting

**"MANIFOLD_API_KEY is required"**
- Make sure you created `.env` file and added your API key

**"No strategies configured"**
- Add `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` to `.env`

**Rate limit errors**
- The bot has built-in rate limiting (500 req/min)
- If you see errors, increase `POLL_INTERVAL_SECONDS`

**No markets found**
- Check that MikhailTal has active markets
- Try visiting https://manifold.markets/MikhailTal
