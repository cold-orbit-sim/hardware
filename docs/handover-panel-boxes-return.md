# Return Handover: Panel Boxes → Planning

**From:** Claude Code implementation session  
**File:** `cad/console/cold-orbit-console.FCMacro`  
**Status:** Box geometry complete; two measurement constants need real values before fabricating.

---

## What was done

Box enclosures have been added to all panels in the FCMacro. Every panel's front face is unchanged; boxes are purely additive.

Three cases were implemented:

**Case 1 — standard rectangular panels (13 panels)**  
All upright and tilted rectangular panels now have a `BoxXxx` shape in the `WALLS` dict: a five-piece shell (back panel + left/right/top/bottom walls, each `PLY_T` thick) extending 200 mm (`BOX_D`) perpendicular to the panel face. Covers: Screen, Cameras, Comms, Turrets, Missiles, TsModes, Touchscreen, Hardpoints 1–4, Engineering centre, Engineering Left/Right.

**Case 2 — Propulsion/FTL wing panels**  
A two-triangle PLY_T-thick skirt (`PropulsionDeskExt`, `FtlDeskExt`) runs from the panel assembly's bottom edge (P1–P2 from `propulsion_ftl_walls`) straight down in world Z to `DESK_H`. The P1–P2 edge is non-horizontal (P1.Z ≈ 538 mm inner, P2.Z ≈ 727 mm outer), so the skirt is a shaped quad split into two triangles along the P1–P2d diagonal.

**Case 3 — HOTAS horizontal deck**  
`BoxHotasLeft` / `BoxHotasRight`: standard box shell with depth = `HOTAS_Z − DESK_H` (guard against mis-set DESK_H). At default DESK_H = 0.0 (floor), box depth ≈ 538 mm — the housing hangs from the underside of the deck to the floor.

---

## New constants requiring measurement

| Constant | Default | Meaning | Where |
|---|---|---|---|
| `BOX_D` | `200.0` mm | Box depth perpendicular to panel front face | PARAMETERS section |
| `DESK_H` | `0.0` mm | World-Z of the surface the console stands on | PARAMETERS section |

`DESK_H` is the most important one to set. It affects both the Prop/FTL skirt depth and the HOTAS box depth. Set to the Z height of the shelf/desk/platform the console base rests on. If the console is floor-standing with no base platform, 0.0 is correct.

---

## What to pick up next

1. **Set DESK_H.** Measure the surface the Prop/FTL panels and HOTAS deck will bottom out against. Update `DESK_H` in the PARAMETERS section. This is a single-line change.

2. **Contact checks for boxes.** The macro already prints contact distances for face panels (HOTAS Side/Back, Propulsion, Engineering fills). No equivalent check exists for box-to-box adjacency. Consider adding `_gap` checks for:
   - `BoxTurrets` ↔ `BoxHardpoint1/2` (should be ~0 wall-to-wall)
   - `BoxMissiles` ↔ `BoxHardpoint3/4` (same)
   - `BoxScreen` ↔ `BoxTurrets` / `BoxMissiles` (should be 0)
   - `BoxHotasLeft/Right` ↔ `PropulsionDeskExt/FtlDeskExt` (lower edges should meet)

3. **Joinery detail pass.** Boxes are modelled as butt-jointed slabs (left/right walls run full panel height; top/bottom fit between them). No rabbet, dado, or finger joint modelled. This is appropriate for layout/CNC-template purposes but a woodwork pass will need to decide the real joint style and may adjust PLY_T offsets accordingly.

4. **EngFill triangles.** `EngLeftFill` and `EngRightFill` (the structural connector triangles between engineering and hardpoint panels) do not have boxes — they are gap-fill structural pieces, not panel enclosures. If they need housing, that's a separate decision.

5. **PLY_T confirmation.** Still at 5.0 mm placeholder. Confirm against actual sheet stock before the first CNC cut.

---

## Files changed

- `cad/console/cold-orbit-console.FCMacro` — box constants + `_face_box_world`, `_bx`, `_prop_ftl_desk_ext` functions; 21 new WALLS entries; updated GROUPS list
- `docs/handover-back-panel-boxes.md` — detailed implementation handback
- `docs/handover-panel-boxes-return.md` — this file
