# Handover Back — Panel Wood Estimate

**From:** Claude Code  
**Task:** Extract panel dimensions from FCMacro, calculate timber for enclosed boxes  
**Source of truth:** `cad/console/cold-orbit-console.FCMacro` (read in full, 2026-09-10)

---

## Plywood thickness constant

`PLY_T = 5.0` mm — this is the **face panel thickness only** (used in `Part.makeBox` for each flat panel solid). It is **not** a box depth. No box depth constant exists in the macro.

**Box depth assumed: 80 mm throughout.** Flag as open question before cutting — see below.

---

## Panel dimensions (all rectangular Face panels)

Derived by tracing `SZ` dict and all downstream calculations in the macro.

| Panel | W (mm) | H (mm) | D (mm)* | Count | Area / box (mm²) | Total area (mm²) |
|---|---:|---:|---:|---:|---:|---:|
| Screen | 687 | 426 | 80 | 1 | 764,004 | 764,004 |
| Cameras | 687 | 90 | 80 | 1 | 247,980 | 247,980 |
| Comms | 687 | 150 | 80 | 1 | 340,020 | 340,020 |
| Turrets | 260 | 666 | 80 | 1 | 494,480 | 494,480 |
| Missiles | 260 | 666 | 80 | 1 | 494,480 | 494,480 |
| TsModes | 400 | 80 | 80 | 1 | 140,800 | 140,800 |
| Touchscreen | 400 | 250 | 80 | 1 | 304,000 | 304,000 |
| HOTAS mount | 200 | 270 | 80 | 2 | 183,200 | 366,400 |
| Hardpoint | 260 | 333 | 80 | 4 | 266,040 | 1,064,160 |
| Engineering (centre) | 687 | 300 | 80 | 1 | 570,120 | 570,120 |
| Engineering ext | 260 | 300 | 80 | 2 | 245,600 | 491,200 |
| **TOTAL** | | | | **16** | | **5,277,644** |

*D = assumed box depth, not from macro.

### Box area formula used

- Front + back: `2 × (W × H)`
- Top + bottom: `2 × (W × D)`
- Left + right: `2 × (H × D)`

---

## Derived dimension workings (non-obvious values)

**Turrets/Missiles H = 666 mm**  
`_weapons_h = cameras_h + screen_h + comms_h = 90 + 426 + 150 = 666`

**Hardpoint H = 333 mm**  
`SZ["hardpoint"][1] = _weapons_h / 2 = 333`

**Cameras W = 687 mm**  
`SZ["cameras"] = (SZ["screen"][0], 90)` — matches screen width exactly

**Comms W = 687 mm**  
Same derivation as cameras.

**Engineering centre W = 687 mm**  
`SZ["engineering"] = (SZ["screen"][0], 300)` — same

**Engineering ext W = 260 mm**  
`_eng_ext_w = (_MAIN_GROUP_W - SZ["screen"][0]) / 2 = (1207 - 687) / 2 = 260`  
where `_MAIN_GROUP_W = 260 + 687 + 260 = 1207`

**HOTAS mount H ≈ 270 mm**  
`TS_TILT = -55°`, so `_a = radians(35°)`, `UP_Y = cos(35°) = 0.8192`  
`TS_DEPTH = ts_modes_h + touchscreen_h = 80 + 250 = 330`  
`HOTAS_H = TS_TOP_Y - TS_Y_BOT = UP_Y × TS_DEPTH = 0.8192 × 330 ≈ 270 mm`  
(Used 270; exact is 270.3 — difference is 0.1% of the box area, irrelevant.)

---

## Totals

| | Value |
|---|---:|
| Raw area (rectangular panels) | **5.278 m²** |
| +15% waste factor | **6.069 m²** |
| Standard sheet (2440 × 1220 mm = 2.977 m²) | |
| **Sheets required** | **3 sheets** |

Sheet count: 6.069 / 2.977 = 2.04 → **3 sheets** (rounding up).

---

## Irregular wall panels — excluded from estimate

The macro's `WALLS` section contains six additional pieces that are **not rectangular flat panels** and cannot straightforwardly be treated as box faces:

| Wall piece | Shape | Count | Status |
|---|---|---|---|
| HotasLeftSide / HotasRightSide | Right triangle (connector) | 2 | Irregular — excluded |
| HotasLeftBack / HotasRightBack | Small rectangle (connector) | 2 | Small, excluded for now |
| PropulsionBack / PropulsionFront | Triangular facets (TriPanel) | 2 per side | Irregular — excluded |
| FtlBack / FtlFront | Triangular facets (TriPanel) | 2 per side | Irregular — excluded |
| EngLeftFill / EngRightFill | Triangular fill panel | 2 | Irregular — excluded |

These pieces were originally flat panels (Propulsion, FTL). They are now shaped non-rectangular connectors built from real touch-point geometry. Their surface areas are non-trivial to estimate without computing the actual triangle coordinates. Recommend treating their timber as an allowance from the waste already factored above, or computing separately once the physical shapes are confirmed from the CAD model.

---

## Open questions

1. **Box depth (80 mm assumed)** — nothing in the macro encodes this. 80 mm is a reasonable console enclosure depth for hand-cut construction, but it affects every side calculation. If the actual planned depth is 60, 100, or 120 mm, re-run the totals. At 60 mm the raw area drops to ~4.6 m² (still 3 sheets); at 120 mm it rises to ~6.6 m² (~4 sheets needed).

2. **HOTAS box geometry** — the HOTAS panels are horizontal mounting decks (tilt = -90°), not vertical panels. A "box" around a horizontal deck may have different proportions in practice. The 80 mm depth above was applied uniformly; adjust if the HOTAS enclosure is shallower.

3. **Wall connector pieces** — Propulsion, FTL, HOTAS Side/Back, and EngFill triangular panels are not included. If these also need enclosures or covers, timber estimate rises.

4. **Box construction method** — estimate assumes each panel gets its own 6-face box. If adjacent panels share walls (e.g. Cameras + Screen + Comms stacked into one tall box), the shared faces cancel and total area drops meaningfully.

---

## Drift from handover document

| Claim in handover | Reality in macro | Notes |
|---|---|---|
| "9 panel types" | 11 distinct rectangular shapes | Engineering split into 3 (centre + 2 ext); Propulsion and FTL are now TriPanel wall pieces, not Face panels — they dropped out of the panel-type count |
| "16 physical pieces" | 16 items in LAYOUT ✓ | Count correct |
| Plywood thickness TBD (9 or 12 mm) | `PLY_T = 5.0 mm` in macro, clearly labelled as a placeholder ("MEASURE AGAINST REAL PARTS BEFORE CUTTING ANYTHING") | The macro comment says to verify before cutting; 5 mm is thinner than either handover estimate |

---

## Decided unilaterally

- Box depth: 80 mm (not in macro — stated explicitly as assumption)
- HOTAS H: rounded from 270.3 mm to 270 mm (0.1% rounding, negligible)
- Irregular WALLS pieces excluded from area totals

## Noticed but not touched

- `PLY_T = 5.0` has a prominent `# >>> MEASURE AGAINST REAL PARTS BEFORE CUTTING ANYTHING <<<` comment next to it. It reads like a placeholder rather than a confirmed spec. Worth verifying before ordering stock.
- The macro still self-describes as "mostly a LAYOUT model — most panels are floating faces, no frame, no mounts, no joinery." Box construction design (joinery, edge treatment, rebates) is out of scope for this estimate.
