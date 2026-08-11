# Handover back — Map button (2026-08-11)

Task: add an eighth mode button, MAP, to the touchscreen mode-select panel.

---

## 1. What changed and how the pitch-vs-width tradeoff was resolved

**Files changed:**

`cad/console/cold-orbit-console.FCMacro`
- `LABELS["ts_modes_modes"]`: added `"MAP"` as the eighth entry (rightmost).
- `f_ts_modes()`: changed `spread(7, 52.0)` → `spread(8, 44.0)`.
  Panel size `SZ["ts_modes"]` kept at `(400.0, 80.0)` — unchanged.
- `f_ts_modes()` docstring updated (see section 3 below).

`docs/panel-control-designs.md` — created (directory did not previously
exist, though README already referenced it). Contains the full mode list
and hole coordinates for all 8 buttons.

`docs/handover-back-map-button.md` — this file.

**Pitch-vs-width decision: pitch tightened, panel unchanged.**

The ts_modes panel sits directly above the touchscreen on the same −55°
slanted surface. Both are 400 mm wide. `TS_EDGE_X` in the layout is
derived from `SZ["touchscreen"][0] / 2.0`, and the HOTAS side triangles
(`hotas_side`) are constructed flush against that edge. Widening ts_modes
without also widening the touchscreen panel would create a mismatch between
the two panels on the same surface; widening both would shift `TS_EDGE_X`,
displacing the HOTAS connections and rippling through the Propulsion/FTL
triangle geometry. Pitch tightening avoids all of that.

44 mm pitch in a 400 mm panel: outermost button centres at ±154 mm,
button edges at ±171 mm, panel edges at ±200 mm — 29 mm margin each side.
Mounting holes sit at x = ±185, giving 14 mm from button edge to mount
centre (11.75 mm clear of hole wall). Inter-button gap = 44 − 34 = 10 mm.
Tight but physically feasible for a row of square push buttons.

---

## 2. Full touchscreen mode-select control list (final state)

All 8 buttons at y = 0.0. Control size: BTN_SQ (34 × 34 mm square
illuminated push button). Pitch: 44 mm. Panel: 400 × 80 mm.

| # | Label | x (mm) | y (mm) | Constant |
|---|---|---|---|---|
| 1 | ENGINEERING | −154.0 | 0.0 | BTN_SQ |
| 2 | PROPULSION  | −110.0 | 0.0 | BTN_SQ |
| 3 | FTL         |  −66.0 | 0.0 | BTN_SQ |
| 4 | TURRETS     |  −22.0 | 0.0 | BTN_SQ |
| 5 | MISSILES    |   22.0 | 0.0 | BTN_SQ |
| 6 | COMMS       |   66.0 | 0.0 | BTN_SQ |
| 7 | HARDPOINTS  |  110.0 | 0.0 | BTN_SQ |
| 8 | MAP         |  154.0 | 0.0 | BTN_SQ |

Mounting holes: D_MOUNT (4.5 mm) at (±185, ±25).

No separate LED cutouts — backlight is the selection indicator, same as
the existing seven buttons.

---

## 3. Final panel dimensions

`SZ["ts_modes"]` = **(400.0, 80.0) — unchanged.**

No change to clearance against HOTAS plates or the touchscreen. HOTAS
deck geometry (`TS_EDGE_X`, `HOTAS_X`, Side/Back triangles) is unaffected.
The touchscreen panel immediately below is 400 × 250 mm — also unchanged.

Updated docstring in `f_ts_modes()`:

> 7.4 - Engineering, Propulsion, FTL, Turrets, Missiles, Comms, Hardpoints, Map.
> Square backlit buttons - the backlight is the selection indicator,
> so no separate LED cutout.
> 8 buttons at 44 mm pitch within the 400 mm panel (10 mm inter-button
> gap); panel width unchanged so HOTAS geometry is unaffected.

---

## 4. Drift from what the handover document assumed

**Handover doc said "an LED above each button."** Not true in the current
code. `f_ts_modes()` has always used `f.square()` (square illuminated
buttons, backlight = selection indicator) with no `f.hole()` for a
separate LED. The docstring explicitly records this: "no separate LED
cutout." This task therefore adds no LED for the MAP button either —
kept consistent with the existing seven.

**`docs/` directory did not exist.** README already mentioned it. Created
as part of this task, with `panel-control-designs.md` as its first file.

**`console_layout.py` has multiple pre-existing divergences from the
FCMacro** (see section 6 below for the full list). The `ts_modes` entry
is `(400.0, 80.0)` in both files — still in sync after this change, since
panel dimensions are unchanged. No update to `console_layout.py` needed
for this task.

**Propulsion/FTL "not wired into layout" status: unchanged.** The LAYOUT
list in the FCMacro still has a comment noting Propulsion/FTL are not flat
panels and are built via WALLS instead. This is by design (they are
triangular facets), not a gap. Status is the same as the previous handback
reported.

---

## 5. Decisions made here

**MAP placed rightmost (position 8).** The handover document didn't specify
an order. MAP is a new mode with no precedent in the existing sequence, and
adding it at the right end preserves the existing seven positions without
renumbering. If the planning side has a preferred order, the `LABELS` tuple
is the only place to change it.

**No LED cutout added.** Consistent with all seven existing mode buttons.
If the physical design later switches to separate indicator LEDs, all eight
buttons need updating together.

**`docs/panel-control-designs.md` started from scratch.** The file did not
previously exist. It covers only the ts_modes panel for now; other panels
can be added as they reach fabrication readiness.

---

## 6. Noticed but not touched

**`console_layout.py` divergences (pre-existing):**

| Entry | console_layout.py | FCMacro |
|---|---|---|
| `cameras` width | 687 mm (same as screen) | 1207 mm (full main-group width) |
| `engineering` width | 700 mm | 1207 mm (derived = cameras) |
| `hardpoint` height | 320 mm | 333 mm (derived from cameras+turrets+comms) |
| `propulsion` / `ftl` | flat panels in PANELS list | TriPanel in WALLS, not in LAYOUT |
| `TS_TOP_Y` / `TS_TOP_Z` | hardcoded (MAIN_Y−80, 700) | geometrically derived from comms position |
| `ts_modes` | (400, 80) ✓ | (400, 80) ✓ |

The propulsion/FTL and TS_TOP divergences were flagged in the previous
handback. The cameras/engineering/hardpoint width differences appear to
predate recent work. All four are pre-existing; this task touches none of
them. They are worth a dedicated sync pass before console_layout.py's
rendered output is used for clearance checks — the panel footprints it
draws for those items are wrong.

**README references `docs/` and `cad/main-panel/` directories.** `docs/`
now exists. `cad/main-panel/` still does not (not referenced by anything
in the FCMacro either). README's repo layout section is stale in that
regard.

**`cad/console/__pycache__/`** contains a compiled `.pyc` of the FCMacro
(from running it as a plain Python file, not via FreeCAD). `.gitignore`
doesn't currently exclude it. Not touched here.
