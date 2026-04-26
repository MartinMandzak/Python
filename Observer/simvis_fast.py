import os, warnings
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.animation import FuncAnimation
from matplotlib.patches import FancyBboxPatch
from network import get_trained_model

# ── Palette ──────────────────────────────────────────────────────────────────
BG        = "#0d1117"
PANEL     = "#161b22"
GRID      = "#21262d"
TEMP_COL  = "#f0883e"   # warm orange
TENS_COL  = "#a371f7"   # purple
RISK_COL  = "#f85149"   # red
SAFE_COL  = "#3fb950"   # green
THRESH    = 80           # risk % threshold line

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
    "grid.alpha":        0.6,
    "legend.facecolor":  PANEL,
    "legend.edgecolor":  GRID,
    "legend.labelcolor": "#e6edf3",
    "font.family":       "monospace",
    "font.size":         9,
})

# ── Init ──────────────────────────────────────────────────────────────────────
df         = pd.read_csv("synthetic_fiber_dataset.csv")
total_rows = len(df)
ai         = get_trained_model()

MAX_POINTS  = 100
time_idx    = np.arange(MAX_POINTS)
temp_buf    = np.full(MAX_POINTS, 271.0)
press_buf   = np.full(MAX_POINTS, 180.0)
torque_buf  = np.full(MAX_POINTS, 10.0)
tension_buf = np.full(MAX_POINTS, 3.1)
risk_buf    = np.zeros(MAX_POINTS)

# ── Layout ────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(12, 7), facecolor=BG)
fig.canvas.manager.set_window_title("Fiber Risk Monitor")

gs = gridspec.GridSpec(2, 1, figure=fig, hspace=0.08, top=0.91, bottom=0.08,
                       left=0.07, right=0.93)
ax_sensors = fig.add_subplot(gs[0])
ax_risk    = fig.add_subplot(gs[1], sharex=ax_sensors)

fig.suptitle("Fiber Production · Live AI Risk Monitor",
             color="#e6edf3", fontsize=12, fontweight="bold", y=0.97)

# ── Sensor panel ─────────────────────────────────────────────────────────────
ax_sensors.set_ylim(260, 285)
ax_sensors.set_ylabel("Temperature (°C)", color=TEMP_COL, labelpad=6)
ax_sensors.tick_params(labelbottom=False)
ax_sensors.grid(True)

ax_tens = ax_sensors.twinx()
ax_tens.set_ylim(2.5, 4.0)
ax_tens.set_ylabel("Tension (cN)", color=TENS_COL, labelpad=6)
ax_tens.tick_params(colors=TENS_COL)
ax_tens.spines["right"].set_edgecolor(TENS_COL)

l_temp, = ax_sensors.plot(time_idx, temp_buf,    color=TEMP_COL, lw=1.5,
                           label="Temp (°C)", alpha=0.9)
fill_temp = ax_sensors.fill_between(time_idx, temp_buf, 260,
                                     color=TEMP_COL, alpha=0.08)

l_tens, = ax_tens.plot(time_idx, tension_buf, color=TENS_COL, lw=1.5,
                        label="Tension (cN)", alpha=0.9)
fill_tens = ax_tens.fill_between(time_idx, tension_buf, 2.5,
                                  color=TENS_COL, alpha=0.08)

lines  = [l_temp, l_tens]
labels = [l.get_label() for l in lines]
ax_sensors.legend(lines, labels, loc="upper left", framealpha=0.6, fontsize=8)

# ── Risk panel ────────────────────────────────────────────────────────────────
ax_risk.set_ylim(0, 110)
ax_risk.set_xlim(0, MAX_POINTS - 1)
ax_risk.set_ylabel("AI Risk (%)", color="#8b949e", labelpad=6)
ax_risk.set_xlabel("Samples  →", color="#8b949e", labelpad=4)
ax_risk.grid(True)

# Danger zone shading
ax_risk.axhspan(THRESH, 110, color=RISK_COL, alpha=0.06)
ax_risk.axhline(THRESH, color=RISK_COL, lw=0.8, ls="--", alpha=0.5)
ax_risk.text(MAX_POINTS - 1, THRESH + 2, f"threshold {THRESH}%",
             color=RISK_COL, alpha=0.55, ha="right", fontsize=7)

l_risk, = ax_risk.plot(time_idx, risk_buf, color=RISK_COL, lw=2, zorder=3)
fill_risk = ax_risk.fill_between(time_idx, risk_buf, 0,
                                  color=RISK_COL, alpha=0.18, zorder=2)

# Status box
status_text = ax_risk.text(
    0.015, 0.82, "",
    transform=ax_risk.transAxes,
    bbox=dict(boxstyle="round,pad=0.4", facecolor=PANEL,
              edgecolor=SAFE_COL, linewidth=1.2),
    color="#e6edf3", fontsize=8, zorder=5,
    verticalalignment="top",
)

# ── Animation ─────────────────────────────────────────────────────────────────
def update(frame):
    global fill_risk, fill_tens, fill_temp

    if frame >= total_rows:
        ani.event_source.stop()
        return l_temp, l_tens, l_risk, status_text

    row     = df.iloc[frame]
    sensors = [
        row["Extruder_Temp_C"],
        row["Melt_Pressure_Bar"],
        row["Godet1_Torque_Nm"],
        row["Fiber_Tension_cN"],
    ]

    opinion = ai.get_ai_state(sensors)

    for buf in [temp_buf, press_buf, torque_buf, tension_buf, risk_buf]:
        buf[:] = np.roll(buf, -1)

    temp_buf[-1]    = sensors[0]
    press_buf[-1]   = sensors[1]
    torque_buf[-1]  = sensors[2]
    tension_buf[-1] = sensors[3]
    risk_buf[-1]    = opinion["risk"]

    l_temp.set_ydata(temp_buf)
    l_tens.set_ydata(tension_buf)
    l_risk.set_ydata(risk_buf)

    # Redraw filled areas
    fill_temp.remove(); fill_tens.remove(); fill_risk.remove()
    fill_temp = ax_sensors.fill_between(time_idx, temp_buf,    260,
                                         color=TEMP_COL, alpha=0.08)
    fill_tens = ax_tens.fill_between(   time_idx, tension_buf, 2.5,
                                         color=TENS_COL, alpha=0.08)
    fill_risk = ax_risk.fill_between(   time_idx, risk_buf,    0,
                                         color=RISK_COL, alpha=0.18, zorder=2)

    # Status box — colour edge green/red depending on state
    is_anomaly = opinion["is_anomaly"]
    edge_col   = RISK_COL if is_anomaly else SAFE_COL
    status_icon = "⚠  ANOMALY" if is_anomaly else "✓  NORMAL"
    status_text.set_text(
        f"{status_icon}\n"
        f"Risk        {opinion['risk']:.1f}%\n"
        f"Confidence  {opinion['confidence']:.1f}%"
    )
    status_text.get_bbox_patch().set_edgecolor(edge_col)

    return l_temp, l_tens, l_risk, status_text


ani = FuncAnimation(fig, update, frames=total_rows, interval=20, blit=False)
plt.show()
