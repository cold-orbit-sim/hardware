# Panel control designs

Prose control lists for each panel, kept in sync with the control layout
built in `cad/console/cold-orbit-console.FCMacro`. This file did not exist
before the inertial dampeners change (2026-08) — it currently only has the
Propulsion section that change required. Other panels' sections should be
added as they get similar treatment; don't infer their content from this
file until they're written.

## Propulsion (7.7)

Sublight engine controls only — separate from the FTL jump drive, which has
its own panel. Main throttle magnitude lives on the HOTAS lever, not here.

**Arm gates the stack.** As with every panel that has an Arm switch, nothing
below it is live until armed. All of the controls below except Emergency
Cutoff and Arm itself are inert pre-arm — including the inertial dampeners
toggle.

Physical layout, top to bottom:

| Row | Left | Centre | Right |
|---|---|---|---|
| Top | Emergency Cutoff (E-stop) | — | Arm (toggle) |
| Upper-mid | Ignition (knob) | — | Propellant Mix (knob, LEAN↔RICH) |
| Lower-mid | — | Engine Temp (bargraph) | — |
| Bottom | RCS (button) | Inertial Dampeners (toggle) | Reverse Thrust (button) |

- **Emergency Cutoff** — destructive, kept visually separate from the
  routine controls (large E-stop, left of Arm rather than grouped with it).
- **Arm** — gates everything else on the panel. Prominent, top row.
- **Ignition** / **Propellant Mix** — mix richness drives engine
  temperature, so they're read together: mix sits directly above temp's
  row, cutoff/arm pair the row above that.
- **Engine Temp** — not cosmetic. Overheating disables propulsion, and that
  disable state is also what aborts an in-progress FTL jump. Kept adjacent
  to Propellant Mix so the causal read (rich mix → rising temp) holds.
- **RCS / Inertial Dampeners / Reverse Thrust** — one bottom-row group of
  flight-behaviour toggles/buttons, left to right. Inertial dampeners is a
  plain on/off toggle: no LED, since the toggle's own physical position
  already shows its state.

See `f_propulsion()` in `cold-orbit-console.FCMacro` for exact coordinates
and hole-diameter constants — this file describes layout intent, the macro
is the source of truth for numbers.
