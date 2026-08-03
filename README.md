# Cold Orbit — Hardware

CAD, panel layouts and fabrication files for **Cold Orbit**, an open-source
physical starship bridge simulator.

The player operates a bounty-hunting drone ship remotely from a physical
console — a full seated bridge with hardware panels, HOTAS, pedals and
screens, driven by a Godot simulation core over wired MQTT.

Part of the [cold-orbit-sim](https://github.com/cold-orbit-sim) project.

## Status

Layout and panel control design are complete. Nothing here has been cut,
drilled or assembled yet — **every dimension is provisional.**

## Repository layout

```
cad/
  console/        full bridge assembly — all 16 panels in 3D space
  main-panel/     turrets / screen surround / missiles face plates
docs/             design notes
```

### `cad/console/`

| File | What it is |
|---|---|
| `cold-orbit-console.FCMacro` | FreeCAD macro. Builds every panel as a separate solid in its seated-player position |
| `console_layout.py` | Same layout data, rendered as front/side/plan/isometric check views with matplotlib. Lets you validate geometry without opening FreeCAD |
| `console-layout.png` | Rendered output of the above |

### `cad/main-panel/`

| File | What it is |
|---|---|
| `cold-orbit-main-panels.FCMacro` | FreeCAD macro. Builds the three main-panel faces as 3D solids |
| `gen_panels.py` | Regenerates the DXFs from the same parameters. Requires `ezdxf` |
| `cold-orbit-panel-turrets.dxf` | 2D cutting template, turret controls |
| `cold-orbit-panel-screen.dxf` | 2D cutting template, 27" screen surround |
| `cold-orbit-panel-missiles.dxf` | 2D cutting template, missile controls |
| `preview-split.png` | The three panels shown assembled |

DXF layers: `OUTLINE`, `CUTOUTS`, `HOLES`, `MOUNT`, `TEXT`.

## Running the FreeCAD macros

1. **Macro → Macros…** and note the user macros location.
2. Copy the `.FCMacro` file into that folder.
3. Reopen **Macro → Macros…**, select it, **Execute**.

Both macros carry a `PARAMETERS` block at the top. Edit, re-run, and the
geometry rebuilds. Each run adds new objects, so delete the previous ones
or start a fresh document first.

The DXFs import directly via **File → Import** with no macro involved.

## Coordinate system

Player-centric, millimetres. Origin is the floor directly below the
player's eye line.

| Axis | Direction |
|---|---|
| X | +right / −left, 0 = player centreline |
| Y | +forward, away from the player |
| Z | +up from floor |

Panels are oriented by `yaw` (rotation about Z, 0 = facing straight back at
the player) and `tilt` (0 = vertical, +ve leans the top away so the face
points downward, −ve lays it back so the face points upward).

Seated eye reference: `(0, 0, 1150)`.

## Panels

| Panel | Placement |
|---|---|
| Screen, Cameras, Comms, Turrets, Missiles | Flush vertical plane, Y = 750 |
| Touchscreen + mode strip | Slanted console, −55° |
| HOTAS mounting plates | Flat, ±330 either side of the touchscreen |
| Hardpoints ×4 | Two wings, 50° yaw, stacked two high per side |
| Propulsion / FTL | Triangle between console and wings, 35° yaw + 35° layback |
| Engineering | Overhead, 65° tilt |

## Known issues

These are unresolved and will change the geometry:

- **Every hole diameter is a placeholder.** Toggle 12 mm, button 16 mm,
  LED 5 mm, encoder 8 mm, knob 22 mm, bargraph 26 × 10 mm. Measure real
  parts before drilling.
- **Screen apertures are unverified.** 27" main and touchscreen visible
  areas are assumed, not measured.
- **HOTAS mounting plates are modelled as zero-height planes.** A real
  throttle stands 150–250 mm proud, and the Propulsion panel sits directly
  above the left plate at Z 614–826. Likely a collision.
- **Knee clearance is unchecked.** The touchscreen's lower edge is at
  Z 511, Y 400 — plausibly where knees and pedals want to be.
- **Hardpoint wings reach X ±771**, at the edge of comfortable seated
  lateral reach.
- **5 mm ply is thin for the screen surround.** A 45 mm border around a
  597 mm aperture will flex. Consider a stiffening frame or thicker stock
  for that panel.

No frame, mounts or joinery are modelled. Panels are floating faces.

## Constraints

Carried from the project's master plan:

- Hand tools only — no CNC, no stationary woodworking equipment
- Fully modular, breaking down for single-trip car-trunk transport
- Affordable off-the-shelf parts throughout
- Open source from day one

## Licence

Hardware designs: **CERN-OHL**. See [`LICENSE`](LICENSE) — the full text
still needs adding.
