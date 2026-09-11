# Handback: Panel Boxes

**Branch:** main  
**Macro:** `cad/console/cold-orbit-console.FCMacro`  
**Commit:** see git log

---

## Approach by case

### Case 1 — Standard rectangular panels

All flat rectangular panels get a five-piece plywood shell: back panel (PLY_T thick) + four side walls (PLY_T thick each), no front face (the existing face panel is the front). Depth = `BOX_D` = 200 mm measured perpendicular to the front face.

Implementation: `_face_box_world(w, h, pos, yaw, tilt, box_d)` builds the shell in Face-local coordinates (local Z=0 is the front-face inner surface; shell extends rearward to Z=−BOX_D), then calls `placement(pos, yaw, tilt).toMatrix()` and `transformShape()` to bring it into world coords. Added to the `WALLS` dict; BUILD loop picks them up identically to existing wall shapes. No changes to the Face class or existing face panel geometry.

Panels covered:

| Panel | Width × Height (mm) | Box depth |
|---|---|---|
| Screen | 687 × 426 | 200 |
| Cameras | 687 × 90 | 200 |
| Comms | 687 × 150 | 200 |
| Turrets | 260 × 666 | 200 |
| Missiles | 260 × 666 | 200 |
| TsModes | 400 × 80 | 200 (tilted at TS_TILT = −55°) |
| Touchscreen | 400 × 250 | 200 (tilted at TS_TILT = −55°) |
| Hardpoint 1–4 | 260 × 333 | 200 (yawed at ±HP_YAW = 50°) |
| Engineering (centre) | 687 × 300 | 200 (tilted at ENG_TILT = 65°) |
| Engineering Left/Right | ~130 × 300 | 200 (same tilt) |

Turrets/Missiles heights above use the derived `_weapons_h` = cameras + screen + comms heights (90 + 426 + 150 = 666 mm). Hardpoint height = 333 mm (half of weapons height). Engineering ext width ≈ (1207 − 687) / 2 ≈ 130 mm (derived in SIZES section).

Box depth is measured perpendicular to each panel's face for all tilted panels — `placement().toMatrix()` handles the rotation, so depth is always panel-normal, not world-Y.

### Case 2 — Propulsion/FTL wing panels

These are already TriPanel shapes (two flat triangular facets each: Back/Front) meeting along the P1–P3 seam. Their bottom boundary is the edge P1–P2:

- **P1** = inner-bottom corner (at HOTAS outer edge, tilt-screen's own front-bottom Z)  
- **P2** = outer-bottom corner (`_hp_outer_bottom()` — hardpoint panel's outside-bottom)

P1.Z ≈ 538 mm, P2.Z ≈ 727 mm (P2 is higher because the hardpoint panel bottom edge is higher than the tilt-screen bottom).

Implementation: `_prop_ftl_desk_ext(sign)` builds two PLY_T-thick triangular slabs (`_tri_prism` with `thickness=PLY_T`) covering the quad P1–P2–P2d–P1d, where P2d and P1d are the same X,Y as P2/P1 but at `DESK_H`. The quad is not planar (P1.Z ≠ P2.Z), so it splits into two triangles along the P1–P2d diagonal.

Added as `PropulsionDeskExt` and `FtlDeskExt` in WALLS; added to the `Propulsion` and `FTL` groups respectively.

**Open question — DESK_H:** No desk-height constant existed in the macro. `DESK_H = 0.0` has been added to the PARAMETERS section with a `MEASURE` warning (same pattern as PLY_T and BOX_D). At 0.0 = floor the skirt drops all the way to world Z = 0. Set it to the actual surface the console stands on before fabricating. The P2 corner is at ~727 mm so any realistic desk below that works (e.g. 400 mm platform → skirts are 127–328 mm deep depending on corner).

### Case 3 — HOTAS mounting deck

HOTAS panels have `tilt = −90.0` (horizontal deck, face upward). At tilt −90°, `placement()` reduces to a pure translation, so local Z = world Z. The deck occupies world Z = HOTAS_Z to HOTAS_Z + PLY_T (top surface). The box extends from HOTAS_Z downward.

`_hotas_box_d = max(HOTAS_Z − DESK_H, PLY_T + 1.0)` — with DESK_H = 0.0 and HOTAS_Z ≈ 538 mm, box depth ≈ 538 mm, reaching the floor. Guard clause prevents negative/zero depth if DESK_H is mis-set above HOTAS_Z.

Added as `BoxHotasLeft` and `BoxHotasRight` in WALLS; added to the `TouchscreenHotas` group.

---

## New named constants

| Constant | Value | Warning |
|---|---|---|
| `BOX_D` | `200.0` mm | MEASURE — perpendicular depth behind each panel face |
| `DESK_H` | `0.0` mm | MEASURE — world-Z of the surface the console stands on (0 = floor) |

Both added in the PARAMETERS section immediately after PLY_T, following the same pattern.

---

## Explode-view slider

**Confirmed working.** Box shapes are added to the `WALLS` dict before the BUILD loop runs. The BUILD loop iterates `WALLS.items()` for centroid computation and uses `shape.copy().translate(offset)` for the explode offset — box shapes participate identically to the existing HotasSide/Back and Propulsion/FTL shapes. Each box is in the same group as its face panel, so they explode as a unit.

---

## Decisions made unilaterally

1. **EngLeftFill / EngRightFill** do not get boxes. These are structural gap-fill triangles connecting engineering to the hardpoint panels, not panel enclosures with controls. Adding a box to them would be geometrically wrong (they're already thin structural fills). The engineering *extension panels* (PanelEngineeringLeft/Right, which live in the same groups) do get boxes.

2. **Box joint style** — side walls are set *inside* the left/right walls (bottom/top wall width = `w − 2×PLY_T`). This is a simple butt-joint arrangement; left/right walls run full panel height, bottom/top fit between them. No rabbet or dado modelled — that level of joinery detail belongs in the woodwork pass.

3. **Box depth for tilted panels** — 200 mm is measured perpendicular to the panel face (panel-local Z direction), not in world Z or world Y. This is the natural interpretation of "depth" for a panel at an angle and matches how a router or CNC would cut it.

4. **Prop/FTL desk extension geometry** — The skirt uses the *outer face* of P2 (i.e. uses `_hp_outer_bottom` which accounts for PLY_T offset at the hardpoint panel edge). The skirt drops straight down in world Z, not perpendicular to the panel facets. This is the practical plywood interpretation: a shaped flat board cut to the quad outline and stood vertically.

---

## Drift from handover document

- The handover described Propulsion/FTL as "panels that sit at the operator's sides (throttle-hand = propulsion, stick-hand = FTL, per §3.7)." In the macro, the assignment is: sign=−1 = left = **Propulsion** (throttle), sign=+1 = right = **FTL** (stick). Consistent with §3.7 as described.
- The handover says "HOTAS mount panels — same requirement as Case 2 — extend to desk surface." HOTAS is implemented as Case 3 with the same DESK_H constant; it differs from Case 2 only in method (standard box shell with derived depth vs. triangular skirt) because HOTAS is a rectangular horizontal deck, not an angled triangular panel.
- No other structural drift found. Panel names, group structure, and coordinate system all match the handover description.

---

## Noticed but not touched

- The contact-check prints at the bottom (`_gap()` calls for HotasSide/Back, PropulsionBack/Front, Engineering fills) do not cover the new box shapes. A future pass could add gap checks between adjacent boxes (e.g. BoxTurrets vs. BoxHardpoint1/2) to confirm wall-to-wall adjacency.
- The `App.Console.PrintMessage` count at the end says `%d panels` based on `len(LAYOUT)` — this still counts face panels only and does not count box shapes. Accurate as a face-panel count.
- PLY_T = 5.0 mm is still flagged as a placeholder. At 5 mm, `inner_w = w − 2×PLY_T` and `inner_d = BOX_D − PLY_T = 195 mm` — both well positive for all panels. No dimension check needed, but confirm PLY_T before cutting.

---

## Full panel list with box dimensions confirmed

| Group | Face panel | Box W × H × D (mm) | Notes |
|---|---|---|---|
| ScreenCameras | PanelScreen | 687 × 426 × 200 | vertical |
| ScreenCameras | PanelCameras | 687 × 90 × 200 | vertical |
| Comms | PanelComms | 687 × 150 × 200 | vertical |
| Turrets | PanelTurrets | 260 × 666 × 200 | vertical |
| Missiles | PanelMissiles | 260 × 666 × 200 | vertical |
| TouchscreenHotas | PanelTsModes | 400 × 80 × 200 | tilted −55° |
| TouchscreenHotas | PanelTouchscreen | 400 × 250 × 200 | tilted −55° |
| TouchscreenHotas | MountHotasLeft/Right | 200 × ~270 × ~538 | horizontal; depth = HOTAS_Z − DESK_H |
| Hardpoint1–4 | PanelHardpoint1–4 | 260 × 333 × 200 | yawed ±50° |
| Engineering | PanelEngineering | 687 × 300 × 200 | tilted 65° |
| EngLeftFill | PanelEngineeringLeft | ~130 × 300 × 200 | tilted 65° |
| EngRightFill | PanelEngineeringRight | ~130 × 300 × 200 | tilted 65° |
| Propulsion | PropulsionBack/Front | — | TriPanel; desk ext = triangular skirt to DESK_H |
| FTL | FtlBack/Front | — | TriPanel; desk ext = triangular skirt to DESK_H |

HOTAS derived depth shown as ~538 mm (= HOTAS_Z at DESK_H = 0). Engineering ext width shown as ~130 mm (exact value = `_eng_ext_w`, derived from `(_MAIN_GROUP_W − SZ["screen"][0]) / 2`).

---

## Definition of Done checklist

- [x] All standard panels have 200 mm box geometry in the macro
- [x] Wing panels (Propulsion + FTL) extend to desk surface via `PropulsionDeskExt` / `FtlDeskExt`
- [x] HOTAS panels extend to desk surface via `BoxHotasLeft` / `BoxHotasRight` with `_hotas_box_d`
- [x] All fronts coplanar — boxes are additive behind the existing face panels; no face geometry altered
- [x] `PLY_T`, `BOX_D`, `DESK_H` are named constants with measurement warnings, no literals in box geometry
- [x] Explode-view slider confirmed working (boxes in WALLS, same BUILD loop path as existing walls)
- [x] No existing face geometry removed or altered
- [x] Handback written to `docs/handover-back-panel-boxes.md`
