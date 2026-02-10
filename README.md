# AI-GAME

## Relic Siege (2D browser game)

You were right — this is now a real **2D game** (not terminal text), built with plain **HTML/CSS/JavaScript** so it runs with default software most people already have.

No game engines, no Godot/Unreal install, no extra dependencies.

## Run it

1. Open `index.html` directly in your browser, **or**
2. Serve it locally:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000`.

## Goal

- Beat **12 stages** in one run (tuned for roughly **25–35 minutes** on a first playthrough).
- Each stage requires:
  - Collecting relics
  - Defeating all enemies

## Controls

- Move: `WASD` or arrow keys
- Aim: mouse
- Shoot: left click (hold to fire)
- Dash: `Space` (cooldown)
- Pause: `P`
- Restart: button on the right panel
