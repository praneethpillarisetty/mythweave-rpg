# Mythweave RPG (BeeWare / Briefcase)

This is an MVP tabletop-fantasy RPG app:
- Data-driven JSON “Campaign Packs”
- Campaign list screen
- Scene player (text + choice buttons)
- Dice roller (e.g., 1d20+3, 2d6+1)
- Pack loader uses importlib.resources so it works when packaged for Android.

## Run locally (optional)
If you do have Briefcase installed locally:
```bash
briefcase dev
```

## Build Android in GitHub Actions (no local installs)
1. Push to `main`
2. Go to **GitHub → Actions → Build Android (Briefcase)**
3. Open the latest run
4. Download **Artifacts → android-dist**

The packaged output is inside `dist/**`.
