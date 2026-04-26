import os, warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.animation import FuncAnimation
from network import get_trained_model

# ── Palette ───────────────────────────────────────────────────────────────────
BG       = "#0d1117"
PANEL    = "#161b22"
GRID     = "#21262d"
RISK_COL = "#f85149"
SAFE_COL = "#3fb950"
THRESH   = 80

SENSORS = [
    {"key": "Extruder_Temp_C",    "label": "Extruder Temp",    "unit": "°C",  "color": "#f0883e", "init": 271.0, "ylim": (268.5, 274.0), "floor": 268.5},
    {"key": "Melt_Pressure_Bar",  "label": "Melt Pressure",    "unit": "Bar", "color": "#58a6ff", "init": 180.0, "ylim": (175.0, 186.0), "floor": 175.0},
    {"key": "Godet1_Torque_Nm",   "label": "Godet Torque",     "unit": "Nm",  "color": "#3fb950", "init":  10.0, "ylim": (6.5,   14.0),  "floor":   6.5},
    {"key": "Fiber_Tension_cN",   "label": "Fiber Tension",    "unit": "cN",  "color": "#a371f7", "init":   3.1, "ylim": (0.0,    7.5),  "floor":   0.0},
]

# ── Style ─────────────────────────────────────────────────────────────────────
plt.rcParams.update({
    "figure.facecolor":  BG,
    "axes.facecolor":    PANEL,
    "axes.edgecolor":    GRID,
    "axes.labelcolor":   "#8b949e",
    "axes.titlecolor":   "#e6edf3",
    "xtick.color":       "#8b949e",
    "ytick.color":       "#8b949e",
    "grid.color":        GRID,
    "grid.linestyle":    "--",
    "grid.alpha":        0.5,
    "legend.facecolor":  PANEL,
    "legend.edgecolor":  GRID,
    "font.family":       "monospace",
    "font.size":         8.5,
})

# ── Init ──────────────────────────────────────────────────────────────────────
df         = pd.read_csv("synthetic_fiber_dataset.csv")
total_rows = len(df)
ai         = get_trained_model()
ai.risk_threshold = THRESH   # keep display and detection in sync

MAX_POINTS = 100
time_idx   = np.arange(MAX_POINTS)

# One rolling buffer per sensor + risk
bufs     = {s["key"]: np.full(MAX_POINTS, s["init"]) for s in SENSORS}
risk_buf = np.zeros(MAX_POINTS)

# ── Layout ────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(13, 8), facecolor=BG)
fig.canvas.manager.set_window_title("Fiber Risk Monitor")

# 3 rows × 2 cols; bottom row spans full width for risk
gs = gridspec.GridSpec(
    3, 2, figure=fig,
    hspace=0.45, wspace=0.35,
    top=0.91, bottom=0.07, left=0.07, right=0.97,
    height_ratios=[1, 1, 0.85],
)

fig.suptitle("Fiber Production · Live AI Risk Monitor",
             color="#e6edf3", fontsize=12, fontweight="bold", y=0.97)

sensor_axes = [
    fig.add_subplot(gs[0, 0]),
    fig.add_subplot(gs[0, 1]),
    fig.add_subplot(gs[1, 0]),
    fig.add_subplot(gs[1, 1]),
]
ax_risk = fig.add_subplot(gs[2, :])

# ── Sensor panels ─────────────────────────────────────────────────────────────
lines = []
fills = []

for ax, s in zip(sensor_axes, SENSORS):
    ax.set_xlim(0, MAX_POINTS - 1)
    ax.set_ylim(*s["ylim"])
    ax.set_title(f"{s['label']}  ({s['unit']})", color=s["color"],
                 fontsize=8.5, pad=4, loc="left")
    ax.tick_params(labelbottom=False, labelsize=7.5)
    ax.grid(True)

    # Baseline mean marker
    mean_val = ai.scaler.mean_[SENSORS.index(s)]
    ax.axhline(mean_val, color=s["color"], lw=0.6, ls=":", alpha=0.35)

    buf  = bufs[s["key"]]
    line, = ax.plot(time_idx, buf, color=s["color"], lw=1.5, alpha=0.9)
    fill  = ax.fill_between(time_idx, buf, s["floor"], color=s["color"], alpha=0.10)

    lines.append(line)
    fills.append(fill)

# ── Risk panel ────────────────────────────────────────────────────────────────
ax_risk.set_xlim(0, MAX_POINTS - 1)
ax_risk.set_ylim(0, 110)
ax_risk.set_ylabel("AI Risk (%)", color="#8b949e", labelpad=5)
ax_risk.set_xlabel("Samples  →",  color="#8b949e", labelpad=3)
ax_risk.grid(True)

ax_risk.axhspan(THRESH, 110, color=RISK_COL, alpha=0.06)
ax_risk.axhline(THRESH, color=RISK_COL, lw=0.8, ls="--", alpha=0.45)
ax_risk.text(MAX_POINTS - 2, THRESH + 2, f"threshold {THRESH}%",
             color=RISK_COL, alpha=0.5, ha="right", fontsize=7)

l_risk,   = ax_risk.plot(time_idx, risk_buf, color=RISK_COL, lw=2, zorder=3)
fill_risk  = ax_risk.fill_between(time_idx, risk_buf, 0,
                                   color=RISK_COL, alpha=0.18, zorder=2)

status_text = ax_risk.text(
    0.012, 0.88, "",
    transform=ax_risk.transAxes,
    bbox=dict(boxstyle="round,pad=0.4", facecolor=PANEL,
              edgecolor=SAFE_COL, linewidth=1.2),
    color="#e6edf3", fontsize=8, zorder=5, verticalalignment="top",
)

# ── Animation ─────────────────────────────────────────────────────────────────
def update(frame):
    global fill_risk, fills

    if frame >= total_rows:
        ani.event_source.stop()
        return

    row     = df.iloc[frame]
    sensors = [row[s["key"]] for s in SENSORS]
    opinion = ai.get_ai_state(sensors)

    # Roll all buffers
    for s, val in zip(SENSORS, sensors):
        buf       = bufs[s["key"]]
        buf[:]    = np.roll(buf, -1)
        buf[-1]   = val

    risk_buf[:] = np.roll(risk_buf, -1)
    risk_buf[-1] = opinion["risk"]

    # Update sensor lines + fills
    for i, (ax, s) in enumerate(zip(sensor_axes, SENSORS)):
        buf = bufs[s["key"]]
        lines[i].set_ydata(buf)
        fills[i].remove()
        fills[i] = ax.fill_between(time_idx, buf, s["floor"],
                                    color=s["color"], alpha=0.10)

    # Update risk
    l_risk.set_ydata(risk_buf)
    fill_risk.remove()
    fill_risk = ax_risk.fill_between(time_idx, risk_buf, 0,
                                      color=RISK_COL, alpha=0.18, zorder=2)

    # Status box
    is_anomaly  = opinion["risk"] >= THRESH
    edge_col    = RISK_COL if is_anomaly else SAFE_COL
    icon        = "⚠  ANOMALY" if is_anomaly else "✓  NORMAL"
    status_text.set_text(
        f"{icon}\n"
        f"Risk        {opinion['risk']:.1f}%\n"
        f"Confidence  {opinion['confidence']:.1f}%"
    )
    status_text.get_bbox_patch().set_edgecolor(edge_col)

    # Live value in each sensor title
    for ax, s, val in zip(sensor_axes, SENSORS, sensors):
        ax.set_title(f"{s['label']}  ({s['unit']})   {val:.2f}",
                     color=s["color"], fontsize=8.5, pad=4, loc="left")


ani = FuncAnimation(fig, update, frames=total_rows, interval=20, blit=False)
plt.show()
