# EscAIpe Velocity

A breakout-style arcade game about AI Safety. The ball is an AI model; the paddle is the AI Safety community. Destroy all the good bricks before the AI escapes.

## Requirements

- Python 3.8+
- pygame-ce

Install the dependency:

```bash
pip install pygame-ce
```

## Launch

```bash
python escaipe_velocity.py
```

## Controls

| Key | Action |
|-----|--------|
| `←` / `A` | Move paddle left |
| `→` / `D` | Move paddle right |
| `Space` | Launch ball / confirm |
| `Esc` / `P` | Pause / unpause |

## Brick types

| Brick | Effect |
|-------|--------|
| **SPD** (green) | Increases paddle speed |
| **WID** (blue) | Widens the paddle |
| **V+** (yellow) | Spawns a vertical paddle on the left wall |
| **+1** (red) | Spawns an extra ball |
| **MA** (orange) | Makes the ball's movement shaky |
| **GH** (purple) | Spawns a ghost ball that passes through bricks |

**Win condition:** destroy all SPD, WID, and V+ bricks across all 5 levels.
