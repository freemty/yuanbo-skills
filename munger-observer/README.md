# Munger Observer - OpenClaw Skill

> **Daily wisdom review applying Charlie Munger's mental models to your work and thinking**

An OpenClaw skill that automatically reviews your daily activity through the lens of Charlie Munger's mental models, helping you detect cognitive biases, blind spots, and hidden traps before they become problems.

## What It Does

The Munger Observer reads your daily activity (memory logs, session history, decisions made) and applies classic mental models to surface insights:

- 🔄 **Inversion** — What could go wrong? Where are the failure modes?
- 🎯 **Second-Order Thinking** — And then what? Consequences of consequences?
- 💰 **Incentive Analysis** — What behaviors are being rewarded?
- ⚖️ **Opportunity Cost** — What's NOT being done?
- 🧠 **Bias Detection** — Confirmation bias, sunk cost fallacy, social proof, availability bias
- 🎓 **Circle of Competence** — Operating within known territory?
- 🛡️ **Margin of Safety** — What's the buffer if things go wrong?

## Installation

### Option 1: ClawHub (Recommended)

```bash
clawhub install munger-observer
```

### Option 2: Manual Installation

```bash
git clone https://github.com/jiahao-shao1/openclaw-skill-munger-observer.git ~/.openclaw/skills/munger-observer
```

## Usage

### Manual Trigger

Ask your OpenClaw agent:
- "Run Munger Observer"
- "Review my thinking today"
- "Check for blind spots"
- "Apply mental models to today's work"

### Automated Daily Review (Recommended)

Set up a cron job for automatic daily review:

```bash
# Add to OpenClaw cron (via openclaw CLI or config)
# Recommended: End of workday (e.g., 8pm)
```

Example cron configuration:
```json
{
  "name": "munger-observer",
  "schedule": {
    "kind": "cron",
    "expr": "0 20 * * *",
    "tz": "Asia/Shanghai"
  },
  "payload": {
    "kind": "agentTurn",
    "message": "Run Munger Observer for today"
  },
  "sessionTarget": "isolated",
  "delivery": {
    "mode": "announce",
    "channel": "telegram",
    "to": "self-improvement"
  }
}
```

## Example Output

```
🧠 **Munger Observer** — March 1, 2026

**Opportunity Cost Alert:** Heavy focus on infrastructure today. The content queue is aging — are drafts decaying in value while we polish tools?

**Second-Order Check:** Speed improvement is good first-order thinking. Second-order: faster responses may raise expectations for response quality. Speed without substance is a trap.

— "Invert, always invert." — Carl Jacobi (Munger's favorite)
```

When nothing notable is found:
```
🧠 **Munger Observer** — March 1, 2026

All clear — no cognitive landmines detected today.

— "Invert, always invert."
```

## Mental Models Applied

### 1. Inversion
> "Tell me where I'm going to die, so I'll never go there." — Charlie Munger

Instead of asking "How do I succeed?", ask "How could this fail spectacularly?"

### 2. Second-Order Thinking
> "And then what?"

Look beyond immediate consequences to the ripple effects.

### 3. Incentive Analysis
> "Show me the incentive and I'll show you the outcome." — Charlie Munger

What behaviors are being rewarded? Hidden incentive structures?

### 4. Opportunity Cost
> "The cost of a thing is the amount of what I will call life which is required to be exchanged for it." — Henry David Thoreau

What's NOT being done? What's the best alternative foregone?

### 5. Bias Detection

Common cognitive biases the Observer watches for:
- **Confirmation bias** — Only seeking validating information
- **Sunk cost fallacy** — Continuing because of past investment
- **Social proof** — Doing it because others do
- **Availability bias** — Overweighting recent/vivid information

### 6. Circle of Competence
> "Know what you know and know what you don't know." — Charlie Munger

Are you operating within known territory or outside? If outside, appropriate humility?

### 7. Margin of Safety
> "The three most important words in investing: margin of safety." — Benjamin Graham

What's the buffer if things go wrong? Cutting it too close anywhere?

## Why This Matters

Charlie Munger's approach to thinking:
- **Multidisciplinary** — Draw from psychology, economics, physics, biology
- **Inversion-first** — Start by avoiding stupidity rather than seeking brilliance
- **Checklist-driven** — Systematic application of mental models
- **Bias-aware** — Constant vigilance against cognitive traps

This skill automates that systematic review, making it a daily habit rather than an occasional exercise.

## Requirements

- OpenClaw installed and configured
- Daily memory logs enabled (`memory/YYYY-MM-DD.md`)
- Recommended: Cron job for automated daily review

## Philosophy

> "It is remarkable how much long-term advantage people like us have gotten by trying to be consistently not stupid, instead of trying to be very intelligent." — Charlie Munger

The Munger Observer doesn't try to make you smarter. It tries to help you avoid being dumb.

## License

MIT

## Author

Created by [Jiahao Shao](https://github.com/jiahao-shao1)

- Website: https://jiahao-shao1.github.io/
- Twitter: [@jiahaoshao1](https://twitter.com/jiahaoshao1)
- Email: jhshao1027@gmail.com

## Acknowledgments

- Built for [OpenClaw](https://github.com/openclaw/openclaw)
- Inspired by Charlie Munger's mental models and Poor Charlie's Almanack
- "Invert, always invert" — Carl Jacobi

## Further Reading

- [Poor Charlie's Almanack](https://www.poorcharliesalmanack.com/)
- [The Psychology of Human Misjudgment](https://fs.blog/great-talks/psychology-human-misjudgment/) — Charlie Munger's famous speech
- [Mental Models: The Best Way to Make Intelligent Decisions](https://fs.blog/mental-models/) — Farnam Street
