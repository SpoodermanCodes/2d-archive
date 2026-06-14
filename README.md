# 🕹 Arcade Hub

A multi-game arcade hub built with Python + Kivy. Runs on desktop and deploys to Android/iOS via Buildozer. Five classic games in a single launcher with persistent high scores and full touch support.

---

## Games

- 🐍 **Snake** — swipe to steer, speed increases as you score
- 🟦 **Tetris** — swipe to move, tap to rotate, swipe down to hard drop
- 🏓 **Pong** — drag your paddle, beat the AI, first to 7 wins
- 👾 **Space Invaders** — drag to move, tap to shoot, enemies fire back in waves
- 🐦 **Flappy Bird** — tap to flap, survive the pipes

---

## Architecture

Each game is a self-contained Kivy `Screen` loaded into a central `ScreenManager`. The main menu is the only screen that knows about all games — individual game screens have zero coupling to each other.

```
arcade-hub/
├── main.py                  # app entry point, ScreenManager, main menu
├── games/
│   ├── snake.py
│   ├── tetris.py
│   ├── pong.py
│   ├── space_invaders.py
│   └── flappy_bird.py
├── shared/
│   ├── constants.py         # colors, block sizes, tetromino shapes
│   ├── scores.py            # persistent high score read/write (scores.json)
│   └── ui.py                # shared back button widget
├── assets/
│   ├── fonts/
│   ├── images/
│   └── sounds/
├── requirements.txt
├── buildozer.spec           # Android/iOS packaging config
└── scores.json              # auto-generated at runtime, not tracked by git
```

---

## Controls

| Game | Move | Action |
|---|---|---|
| Snake | Swipe direction | — |
| Tetris | Swipe left / right | Tap = rotate, Swipe down = hard drop |
| Pong | Drag paddle | — |
| Space Invaders | Drag ship | Tap = shoot |
| Flappy Bird | — | Tap = flap |

---

## Setup

**Step 1 — Install dependencies**

```bash
pip install -r requirements.txt
```

**Step 2 — Run**

```bash
python main.py
```

---

## Mobile Build (Android)

Requires Linux or WSL. Run from inside the project folder:

```bash
pip install buildozer
buildozer android debug deploy run
```

The `buildozer.spec` targets API 33, `arm64-v8a` and `armeabi-v7a`. No changes needed for a basic build.

> iOS builds use `kivy-ios` on macOS — see the [Kivy iOS docs](https://kivy.org/doc/stable/guide/packaging-ios.html).

---

## High Scores

Scores are saved automatically to `scores.json` in the project root after each game session. The file is excluded from version control via `.gitignore` — it is generated fresh on first run.

---

## Push to GitHub

```bash
git init
git add .
git commit -m "initial commit"
git remote add origin https://github.com/<your-username>/arcade-hub.git
git push -u origin main
```

---

## Developer Notes

- Each game's speed or difficulty lives inside its own file — there is no shared difficulty config yet. If you want to tune values (e.g. Flappy Bird gravity, Space Invaders fire rate), look for the constants at the top of each game file.
- The Tetris line-clear scoring uses the standard Nintendo system: 100 / 300 / 500 / 800 for 1 / 2 / 3 / 4 lines.
- Pong AI speed is fixed at 3px/frame — increase the value in `pong.py` to make the AI harder.
- Touch swipe detection uses a 20px minimum threshold. On high-DPI screens this may feel insensitive — increase the threshold in each game's `on_touch_up` if needed.

---

## License

MIT
