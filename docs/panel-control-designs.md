# Cold Orbit — Panel Control Designs

Fabrication reference for every drilled hole and cutout on the console.
All dimensions in mm. Hole diameters are placeholders — verify against
real parts before drilling. See `cad/console/cold-orbit-console.FCMacro`
for the authoritative coordinates.

---

## Touchscreen mode-select panel

**Panel:** `PanelTsModes`  
**Size:** 400 × 80 mm  
**Plane:** slanted touchscreen console, −55° tilt, directly above the
touchscreen panel  
**Controls:** 8 mutually exclusive square illuminated push buttons.
Backlight serves as the selection indicator — no separate LED cutout.
Selection is enforced in firmware; buttons are electrically independent.
No Arm switch — this panel is a display selector, not a weapons control.

### Mode list (left to right)

| # | Label | What it selects |
|---|---|---|
| 1 | ENGINEERING | Engineering system overview (reactor, power allocation) |
| 2 | PROPULSION | Propulsion status (engine temp, RCS, thrust) |
| 3 | FTL | FTL drive status and jump destination |
| 4 | TURRETS | Turret targeting and fire mode |
| 5 | MISSILES | Missile loadout and targeting |
| 6 | COMMS | Communications log and message queue |
| 7 | HARDPOINTS | Active hardpoint module status |
| 8 | MAP | Drift star map — 26 systems (A–Z) with named stars, for navigation reference alongside FTL destination selection |

### Hole coordinates (local panel frame, origin at panel centre)

| # | Label | x (mm) | y (mm) | Size |
|---|---|---|---|---|
| 1 | ENGINEERING | −154.0 | 0.0 | BTN_SQ (34 × 34 mm) |
| 2 | PROPULSION  | −110.0 | 0.0 | BTN_SQ |
| 3 | FTL         |  −66.0 | 0.0 | BTN_SQ |
| 4 | TURRETS     |  −22.0 | 0.0 | BTN_SQ |
| 5 | MISSILES    |   22.0 | 0.0 | BTN_SQ |
| 6 | COMMS       |   66.0 | 0.0 | BTN_SQ |
| 7 | HARDPOINTS  |  110.0 | 0.0 | BTN_SQ |
| 8 | MAP         |  154.0 | 0.0 | BTN_SQ |

Mounting holes: M4 clearance (D_MOUNT = 4.5 mm) at (±185, ±25).

### Pitch note

7-button design used 52 mm pitch. 8-button design uses 44 mm pitch within
the same 400 mm panel. Inter-button gap = 44 − 34 = 10 mm. Panel width
and HOTAS geometry are unchanged.
