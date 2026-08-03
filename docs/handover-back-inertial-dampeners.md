# Handback: inertial dampeners toggle — Propulsion panel

Resync document for the planning conversation. Read this in full before
updating the master plan — several premises in the original handover don't
match the repo as it currently stands.

## 1. What changed, and why

- **`cad/console/cold-orbit-console.FCMacro`, `f_propulsion()`**: added an
  inertial dampeners toggle at `(0, -55)` using `D_TOGGLE`, with a
  `DAMPENERS` etched label above it. No LED cutout, per the brief — a
  toggle's position is its own indicator.
- **Docstring updated** to list the current control set and explain the
  bottom-row grouping and the Arm-gating behaviour.
- **`docs/panel-control-designs.md`** created (see §4 — this file didn't
  exist before) with a Propulsion section covering the full control list,
  physical layout, and the Arm-gating note.

**How the engine-temp displacement was resolved: it wasn't needed.** The
handover assumed RCS and reverse thrust were stacked in the right-hand
column and that inserting a bottom row would displace the engine temp
bargraph. Neither is true of the code as committed (single commit in this
repo's history — see §4.3). As of this session:

- RCS already sits at `(-50, -55)` and reverse thrust at `(50, -55)` — both
  already on the same bottom row, already split left/right.
- Engine temp's bargraph is on its own row, `slot(0, -20, 70, 14)` — 35 mm
  above the bottom row, not on it.

So the bottom row already had a free centre slot at `(0, -55)`, exactly
where the dampeners toggle needed to go. It was inserted there directly;
nothing else moved. Engine temp stays exactly where it was, still directly
above propellant mix, so the mix→temp causal read is unaffected — it was
never at risk.

## 2. Full current Propulsion control list (final state)

All coordinates are local to the panel face (mm, centred origin). Hole
diameters are the named constants from the `PARAMETERS` block — all still
placeholders pending real-part measurement.

| Control | Position (x, y) | Cutout | Constant | Label etched |
|---|---|---|---|---|
| Emergency Cutoff | (-50, 55) | round hole | `D_ESTOP` (30.0) | EMERGENCY CUTOFF |
| Arm | (50, 55) | round hole | `D_TOGGLE` (12.0) | ARM |
| Ignition | (-50, 15) | round hole | `D_KNOB` (22.0) | IGNITION |
| Propellant Mix | (50, 15) | round hole | `D_KNOB` (22.0) | PROPELLANT MIX, LEAN/RICH either side |
| Engine Temp | (0, -20) | slot 70×14 | — (bargraph, no named constant) | ENGINE TEMP |
| RCS | (-50, -55) | round hole | `D_BUTTON` (16.0) | RCS |
| **Inertial Dampeners (new)** | **(0, -55)** | **round hole** | **`D_TOGGLE` (12.0)** | **DAMPENERS** |
| Reverse Thrust | (50, -55) | round hole | `D_BUTTON` (16.0) | REVERSE |

Plus 4 corner mounting holes via `f.mounts()` (`D_MOUNT`, 4.5 mm) — see §6,
these are currently meaningless given the panel's zero-size bounding box.

Physical read, top to bottom: **Cutoff / Arm** → **Ignition / Mix** →
**Engine Temp** → **RCS / Dampeners / Reverse**.

Clearance check (by hand, since FreeCAD wasn't available to run — see §5):
dampeners-to-RCS edge gap ≈ 36 mm, dampeners-to-reverse edge gap ≈ 36 mm,
legend text gaps all ≥ 30 mm. No overlaps.

## 3. Final panel dimensions

**Unchanged, and not meaningfully "a dimension" right now — see §4.1.**
`SZ["propulsion"]` is still `(0.0, 0.0)`, exactly as before this change. I
did not grow or shrink anything. The 60 mm growth ceiling / 26 mm hardpoint
clearance from the handover doesn't currently apply to anything in this
codebase — full explanation below.

## 4. Drift from what the handover described

This is the important part — the repo has moved on more than the handover
knew.

**4.1 — `f_propulsion()` is not wired into the actual 3D layout.** There's
an explicit comment directly above the function (unchanged by me):

> NOT CURRENTLY WIRED INTO LAYOUT. Propulsion/FTL are now an angled,
> non-rectangular fit (2 triangular facets each...), not a flat yaw/tilt
> Face, so this control layout — built for a flat 204×189 rectangle — no
> longer has a panel to sit on. Kept rather than deleted...

The real 3D Propulsion geometry is built by `propulsion_ftl_walls()` as two
flat triangular facets (`PropulsionBack`, `PropulsionFront`), pinned by four
real corners (HOTAS's outer corner, the hardpoint panel's outer-bottom
corner, comms' outer edge, HOTAS's back-outer corner) that the code confirms
are not coplanar. There is no 35° yaw flat panel in the current build at
all. Porting the control set from `f_propulsion()` onto one of those two
triangles is explicitly unfinished.

I still made the change inside `f_propulsion()`, because the surrounding
comment frames it as the maintained "right starting point" for that future
port, and the task's real goal — get the dampeners toggle correctly speced
and positioned relative to its neighbours — holds regardless of which solid
eventually carries it. But **nothing about this change puts a dampeners
toggle into the buildable 3D model today.** That only happens once someone
does the triangular-facet port.

**4.2 — Because of 4.1, `SZ["propulsion"]` is an unused placeholder,
`(0.0, 0.0)`**, never overwritten anywhere else in the file (confirmed by
searching the whole macro). Every hole in `f_propulsion()` — before and
after this change — sits outside the panel's own (zero-area) bounding box.
This is pre-existing, not something this change caused or fixed. It means
the "nothing outside panel bounds" done-criterion is currently unverifiable
in any meaningful sense for this panel; I did not attempt to fix it, since
resolving it means finishing the triangular-facet port, which is out of
scope here.

**4.3 — The handover's "RCS and reverse thrust stacked in the right-hand
column" premise doesn't match the repo at any point in its history.** This
repo has exactly one commit (`initial commit`); `f_propulsion()` has looked
the way it's described in §2 (minus dampeners) since that commit. There's
no earlier state where RCS/reverse were stacked together. Worth mentioning
to whoever maintains the planning-side notes — that description didn't come
from this repo.

**4.4 — The "35° yaw" and "~26 mm hardpoint clearance" figures don't match
the current FreeCAD macro, but do match a stale duplicate.**
`cad/console/console_layout.py` (the separate matplotlib check-view script)
still has its own independent copy of panel sizes/positions, including:

```python
"propulsion": (280.0, 260.0)
...
("PanelPropulsion", "propulsion", (-420.0, 600.0, 720.0), 35.0, -35.0),
```

That's a flat-panel, fixed-yaw model of Propulsion — the design the FCMacro
has since moved away from in favour of the triangular walls (§4.1). The two
files currently disagree about what shape the Propulsion panel is. I didn't
touch `console_layout.py` — I made no dimensional change, and the task said
it shouldn't need touching unless I did — but this cross-file inconsistency
predates my change and will produce a misleading check-view render until
someone reconciles it.

**4.5 — `docs/` didn't exist.** README's repository-layout tree already
listed a planned `docs/` folder ("design notes"), but no such folder or
file existed yet. I created `docs/panel-control-designs.md` fresh, with
only the Propulsion section this task needed — I did not invent content for
any other panel.

**4.6 — `cad/main-panel/` doesn't exist either**, despite being referenced
in README's repository layout and file tables (turret/screen-surround/
missile face plates, DXFs, etc.). Unrelated to this task, but it means the
repo is less built-out than the handover's framing assumed.

## 5. Uncertain / decided myself — confirm or overrule

- **Label wording: `DAMPENERS`, not `INERTIAL DAMPENERS`.** Matches the
  existing terse convention (`REVERSE` for reverse thrust, `RCS` for RCS)
  rather than the full task name. Easy to change if you want the fuller
  wording etched.
- **Edited `f_propulsion()` in place despite it being unwired (§4.1)**,
  rather than waiting for the triangular-facet port. Judgement call — flag
  if you'd rather this kind of control-set change wait until the panel has
  a real solid to sit on.
- **Did not touch `console_layout.py`'s stale propulsion entry (§4.4).**
  No dimension changed here, so strictly out of scope per the brief, but it
  might be worth a follow-up task given it now visibly disagrees with the
  FCMacro.
- **Could not run the macro in FreeCAD** — not installed in this
  environment. Verified the file parses as valid Python (`ast.parse`) and
  hand-checked the new hole's clearances against its neighbours (§2), but
  "runs in FreeCAD without error" is unconfirmed by actual execution.
  Recommend running it locally before treating this as fully verified.
- **Created `docs/panel-control-designs.md` as a new file** rather than
  skipping the doc requirement since no file existed to update. If the
  planning side already has a different intended structure for this doc,
  this may need reshaping rather than extending.

## 6. Noticed, not touched

- `f.mounts()` in `f_propulsion()` places its 4 corner mounting holes near
  the panel's own centre (roughly ±15, ±15) rather than near real corners,
  because of the zero-size bounding box (§4.2). Cosmetic/meaningless right
  now, pre-existing, not part of this change.
- The `console_layout.py` / FCMacro divergence on Propulsion's shape (§4.4)
  will likely also affect **FTL**, which shares the same triangular-wall
  treatment (`propulsion_ftl_walls(1, "Ftl")`) — didn't check FTL's
  `console_layout.py` entry, but it's worth checking at the same time if
  this gets reconciled.
- Didn't investigate whether `LABELS["ts_modes_modes"]` (the touchscreen
  mode-strip label list, which includes `"PROPULSION"`) needs any update —
  out of scope for this change, not looked at closely.

---

**Committed to:** `claude/cold-orbit-hardware-setup-fbaz0g` (not yet merged
to `main` — see the earlier wiring-diagram handback for that branch's other
pending commit).
