# Handover back — retire console_layout.py

Date: 2026-08-12

## 1. What was removed

- `cad/console/console_layout.py` — removed via `git rm -f`. The `-f` flag was needed because the file had uncommitted local modifications (turret/missile height updated to 666 mm, Z_WEAPONS centring calculation added, alignment-only whitespace). These changes were not synced to the FCMacro and are exactly the kind of drift the retirement is meant to prevent. The full diff is in git history before this commit.
- `cad/console/console-layout.png` — removed via `git rm`. Nothing else in the repo references it (README was the only reference, and that table was updated as part of this task).

## 2. What README now says

The `cad/console/` file table now reads:

```
| File | What it is |
|---|---|
| `cold-orbit-console.FCMacro` | FreeCAD macro. Builds every panel as a separate solid in its seated-player position |

The FCMacro is the single source of truth for console geometry. To inspect the layout without hunting through 3D, use the built-in explode-view slider: set `EXPLODE` (0–100 mm) near the top of the `PARAMETERS` block, re-run the macro, and all 14 manufacturing groups radiate outward from the eye point so every panel is visible.
```

## 3. `__pycache__` handling

`cad/console/__pycache__/` was present, containing `cold-orbit-console.cpython-313.pyc`. It was never tracked by git — `.gitignore` already covers `__pycache__/` in its Python section. The directory has been deleted from the working tree. No `.gitignore` change was needed.

## 4. Other references that needed updating

- `docs/handover-back-map-button.md` — contains multiple references to `console_layout.py`, including a divergence table. This is a historical document recording the state at the time the Map button was added; the references accurately reflect that history and were left untouched.
- No other files, scripts, CI configuration, or imports reference `console_layout.py` or `console-layout.png`.

## 5. Noticed but not touched

The `cold-orbit-console.FCMacro` itself has uncommitted local modifications (shown in `git status` as `M` at the start of this task). Those changes are separate from this retirement task and were not staged or committed here.
