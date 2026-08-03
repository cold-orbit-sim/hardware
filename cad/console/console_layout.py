#!/usr/bin/env python3
"""
Cold Orbit - full console layout.
Defines every panel's size and placement, then renders check views.

Coordinate system (mm), player-centric:
    X  +right / -left   (0 = player centreline)
    Y  +forward, away from the player
    Z  +up from floor

Panel orientation is given as (yaw, tilt):
    yaw   rotation about Z. 0 = facing straight back at the player.
          +ve swings a panel's face toward +X (used for the left wing).
    tilt  0 = vertical.  +ve leans the top away (faces downward, used
          overhead).  -ve lays it back (faces upward, used for consoles).
"""
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ------------------------------------------------------------ ERGONOMIC REFS
EYE_Z    = 1150.0   # seated eye height above floor
MAIN_Y   = 750.0    # main panel plane, distance forward of player
Z_SCREEN = EYE_Z - 60.0

# ------------------------------------------------------------ PANEL SIZES
SZ = {
    "screen":     (687.0, 426.0),
    "cameras":    (687.0,  90.0),
    "comms":      (687.0, 150.0),
    "turrets":    (260.0, 426.0),
    "missiles":   (260.0, 426.0),
    "ts_modes":   (400.0,  80.0),
    "touchscreen":(400.0, 250.0),
    "hotas":      (200.0, 260.0),
    "hardpoint":  (260.0, 320.0),
    "propulsion": (280.0, 260.0),
    "ftl":        (220.0, 260.0),
    "engineering":(700.0, 300.0),
}

# ------------------------------------------------------------ MAIN PANEL BLOCK
# screen centred, cameras above, comms below, turrets left, missiles right.
_sw, _sh = SZ["screen"]
_ch      = SZ["cameras"][1]
_mh      = SZ["comms"][1]
_tw      = SZ["turrets"][0]

Z_CAM   = Z_SCREEN + _sh / 2 + _ch / 2
Z_COMMS = Z_SCREEN - _sh / 2 - _mh / 2
X_SIDE  = _sw / 2 + _tw / 2

# ------------------------------------------------------------ SLANTED CONSOLE
TS_TILT   = -55.0                       # lies back, faces up at the player
_a        = math.radians(90.0 + TS_TILT)
UP_Y, UP_Z = math.cos(_a), math.sin(_a)  # unit vector up-slope, in Y/Z

TS_TOP_Y = MAIN_Y - 80.0                 # top edge of the slanted console
TS_TOP_Z = 700.0


def down_slope(dist):
    """Point `dist` mm down-slope from the console's top edge."""
    return (TS_TOP_Y - UP_Y * dist, TS_TOP_Z - UP_Z * dist)


_y, _z = down_slope(SZ["ts_modes"][1] / 2)
TS_MODES_POS = (0.0, _y, _z)
_y, _z = down_slope(SZ["ts_modes"][1] + SZ["touchscreen"][1] / 2)
TS_POS = (0.0, _y, _z)

# ------------------------------------------------------------ SIDE WINGS
HP_YAW    = 50.0                         # hardpoint wing, swung in at the player
_r        = math.radians(HP_YAW)
_pivot_x  = -(_sw / 2 + _tw)             # outer edge of the turret panel
_half     = SZ["hardpoint"][0] / 2
HP_X      = _pivot_x - math.cos(_r) * _half
HP_Y      = MAIN_Y - math.sin(_r) * _half
HP_Z_MID  = 1050.0
HP_DZ     = SZ["hardpoint"][1] / 2 + 10.0

# ------------------------------------------------------------ PANEL TABLE
# name, size-key, (x, y, z), yaw, tilt
PANELS = [
    ("PanelScreen",      "screen",      (0.0, MAIN_Y, Z_SCREEN),      0.0,   0.0),
    ("PanelCameras",     "cameras",     (0.0, MAIN_Y, Z_CAM),         0.0,   0.0),
    ("PanelComms",       "comms",       (0.0, MAIN_Y, Z_COMMS),       0.0,   0.0),
    ("PanelTurrets",     "turrets",     (-X_SIDE, MAIN_Y, Z_SCREEN),  0.0,   0.0),
    ("PanelMissiles",    "missiles",    (X_SIDE, MAIN_Y, Z_SCREEN),   0.0,   0.0),

    ("PanelTsModes",     "ts_modes",    TS_MODES_POS,                 0.0, TS_TILT),
    ("PanelTouchscreen", "touchscreen", TS_POS,                       0.0, TS_TILT),

    ("MountHotasLeft",   "hotas",       (-330.0, 480.0, 560.0),       0.0, -90.0),
    ("MountHotasRight",  "hotas",       (330.0, 480.0, 560.0),        0.0, -90.0),

    ("PanelHardpoint1",  "hardpoint",   (HP_X, HP_Y, HP_Z_MID + HP_DZ),   HP_YAW, 0.0),
    ("PanelHardpoint2",  "hardpoint",   (HP_X, HP_Y, HP_Z_MID - HP_DZ),   HP_YAW, 0.0),
    ("PanelHardpoint3",  "hardpoint",   (-HP_X, HP_Y, HP_Z_MID + HP_DZ), -HP_YAW, 0.0),
    ("PanelHardpoint4",  "hardpoint",   (-HP_X, HP_Y, HP_Z_MID - HP_DZ), -HP_YAW, 0.0),

    ("PanelPropulsion",  "propulsion",  (-420.0, 600.0, 720.0),       35.0, -35.0),
    ("PanelFtl",         "ftl",         (420.0, 600.0, 720.0),       -35.0, -35.0),

    ("PanelEngineering", "engineering", (0.0, 300.0, EYE_Z + 500.0),  0.0,  65.0),
]


# ------------------------------------------------------------ GEOMETRY
def basis(yaw, tilt):
    """Return (u, v, n) unit vectors for a panel's local axes in world space."""
    a = math.radians(90.0 + tilt)
    ca, sa = math.cos(a), math.sin(a)
    # before yaw: u=(1,0,0)  v=(0,ca,sa)  n=(0,-sa,ca)
    y = math.radians(yaw)
    cy, sy = math.cos(y), math.sin(y)

    def rz(v):
        return (v[0] * cy - v[1] * sy, v[0] * sy + v[1] * cy, v[2])

    return rz((1.0, 0.0, 0.0)), rz((0.0, ca, sa)), rz((0.0, -sa, ca))


def corners(size_key, pos, yaw, tilt):
    w, h = SZ[size_key]
    u, v, _ = basis(yaw, tilt)
    out = []
    for su, sv in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        out.append(tuple(pos[i] + u[i] * su * w / 2 + v[i] * sv * h / 2
                         for i in range(3)))
    return out


# ------------------------------------------------------------ PREVIEW
def render():
    fig = plt.figure(figsize=(17, 11))
    views = [
        ("front  (looking forward, +Y)", 0, 2, (1, -1)),
        ("side   (player faces right)",  1, 2, (1, 1)),
        ("plan   (from above)",          1, 0, (1, 1)),
    ]
    for idx, (title, ai, bi, _) in enumerate(views, start=1):
        ax = fig.add_subplot(2, 2, idx)
        for name, key, pos, yaw, tilt in PANELS:
            c = corners(key, pos, yaw, tilt) + [None]
            c[-1] = c[0]
            xs = [p[ai] for p in c]
            ys = [p[bi] for p in c]
            col = ("#c33" if "Hotas" in name else
                   "#36c" if "Hardpoint" in name else
                   "#181" if name == "PanelEngineering" else "#333")
            ax.plot(xs, ys, color=col, lw=1.4)
        if ai == 0 and bi == 2:
            ax.plot([0], [EYE_Z], "o", color="#f60", ms=9)
        if ai == 1 and bi == 2:
            ax.plot([0], [EYE_Z], "o", color="#f60", ms=9)
        if ai == 1 and bi == 0:
            ax.plot([0], [0], "o", color="#f60", ms=9)
        ax.set_title(title + "   (orange = player eye)", fontsize=10)
        ax.set_aspect("equal")
        ax.grid(alpha=0.15)

    ax = fig.add_subplot(2, 2, 4, projection="3d")
    for name, key, pos, yaw, tilt in PANELS:
        c = corners(key, pos, yaw, tilt)
        c.append(c[0])
        col = ("#c33" if "Hotas" in name else
               "#36c" if "Hardpoint" in name else
               "#181" if name == "PanelEngineering" else "#333")
        ax.plot([p[0] for p in c], [p[1] for p in c], [p[2] for p in c],
                color=col, lw=1.2)
    ax.scatter([0], [0], [EYE_Z], color="#f60", s=45)
    ax.set_xlabel("X"); ax.set_ylabel("Y"); ax.set_zlabel("Z")
    ax.set_title("isometric", fontsize=10)
    ax.view_init(elev=18, azim=-70)
    try:
        ax.set_box_aspect((1400, 900, 1800))
    except Exception:
        pass

    fig.suptitle("Cold Orbit - full console layout check", fontsize=13)
    plt.tight_layout()
    plt.savefig("/home/claude/console-layout.png", dpi=100)


if __name__ == "__main__":
    render()
    print("panels:", len(PANELS))
    zs = [p[2] for n, k, pos, y, t in PANELS
          for p in corners(k, pos, y, t)]
    ys = [p[1] for n, k, pos, y, t in PANELS
          for p in corners(k, pos, y, t)]
    xs = [p[0] for n, k, pos, y, t in PANELS
          for p in corners(k, pos, y, t)]
    print(f"X {min(xs):8.1f} .. {max(xs):8.1f}")
    print(f"Y {min(ys):8.1f} .. {max(ys):8.1f}")
    print(f"Z {min(zs):8.1f} .. {max(zs):8.1f}")
