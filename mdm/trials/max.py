"""
Matplotlib Masterpiece — Single-file expert-level example.

Features:
- Global rc styling + custom stylesheet
- Complex GridSpec layout with inset axes
- 3D rotating parametric surface (animated)
- Polar bar plot
- Heatmap with contour overlay and custom normalization
- Line + scatter plot with synced inset zoom
- Interactive widgets: Slider, Button, RadioButtons
- Animation (FuncAnimation) + event-driven updates
- Custom artist (Path / FancyBboxPatch) and LaTeX-rendered text
- Procedural image compositing (no external files)
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import gridspec, patches, transforms
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D  # registers 3d projection
from mpl_toolkits.axes_grid1.inset_locator import inset_axes, mark_inset
from matplotlib.widgets import Slider, Button, RadioButtons
from matplotlib.colors import Normalize, TwoSlopeNorm
from matplotlib.path import Path
from matplotlib.patches import PathPatch, FancyBboxPatch
import matplotlib.image as mpimg
import io
from PIL import Image, ImageDraw, ImageFont

# ---------------------------
# 0. Backend note (only informative)
# ---------------------------
# If running as a script, ensure a GUI backend is available:
# e.g. export MPLBACKEND=tkAgg (or set in code via matplotlib.use('tkAgg')) before importing pyplot.
# In Jupyter, use %matplotlib notebook or %matplotlib widget for interactive widgets/animations.

# ---------------------------
# 1. Global style / rcParams
# ---------------------------
plt.rcParams.update({
    "figure.facecolor": "#1e1e2f",
    "axes.facecolor": "#1e1e2f",
    "axes.edgecolor": "#cfcfe8",
    "axes.labelcolor": "#f0f0ff",
    "xtick.color": "#cfcfe8",
    "ytick.color": "#cfcfe8",
    "text.color": "#f6f6ff",
    "font.size": 10,
    "font.family": "DejaVu Sans",
    "figure.dpi": 110,
    "legend.facecolor": "#2b2b3b",
    "legend.edgecolor": "#888899",
    "grid.color": "#2f2f3f",
    "grid.linestyle": "--",
    "axes.grid": True,
})

# ---------------------------
# 2. Prepare data for multiple plots
# ---------------------------
# 3D parametric surface (saddle-like with radial ripples)
u = np.linspace(0, 2 * np.pi, 120)
v = np.linspace(0, np.pi, 80)
U, V = np.meshgrid(u, v)
R = 1.5 + 0.6 * np.sin(4 * U) * np.cos(3 * V)
X3 = R * np.cos(U) * np.sin(V)
Y3 = R * np.sin(U) * np.sin(V)
Z3 = np.cos(V) * (1 + 0.2 * np.sin(6 * U))

# Line and scatter data (main time-series)
t = np.linspace(0, 20, 1000)
base_signal = np.sin(2 * t) + 0.3 * np.sin(7 * t)
scatter_x = np.random.uniform(2, 18, 180)
scatter_y = np.sin(2 * scatter_x) + 0.3 * np.sin(7 * scatter_x) + 0.25 * np.random.randn(180)

# Heatmap grid
nx, ny = 120, 80
x = np.linspace(-3, 3, nx)
y = np.linspace(-2, 2, ny)
Xh, Yh = np.meshgrid(x, y)
Zheat = np.exp(-(Xh**2 + 1.5 * Yh**2)) * (1 + 0.3 * np.sin(5 * Xh) * np.cos(3 * Yh))

# Polar data
theta = np.linspace(0.0, 2 * np.pi, 16, endpoint=False)
radii = np.abs(np.sin(3 * theta) + 0.5 * np.cos(5 * theta)) + 0.2
width = (2 * np.pi) / len(theta) * 0.9

# ---------------------------
# 3. Build figure layout using GridSpec (complex dashboard)
# ---------------------------
fig = plt.figure(figsize=(14, 9), constrained_layout=False)
# We'll use a 3x3 grid; some elements will span multiple cells.
gs = gridspec.GridSpec(nrows=3, ncols=3, figure=fig, width_ratios=[1, 1, 1.2], height_ratios=[1, 1, 0.9], wspace=0.35, hspace=0.45)

# Main time-series (big)
ax_main = fig.add_subplot(gs[0:2, 0:2])
ax_main.set_title(r"Main signal: $s(t)=A\sin(2t)+0.3\sin(7t)$", fontsize=12, pad=12)
ax_main.set_xlabel("time (s)")
ax_main.set_ylabel("amplitude")

# Inset zoom inside main plot
ax_inset = inset_axes(
    ax_main,
    width="40%",
    height="35%",
    loc='upper right',
    bbox_to_anchor=(0, 0, 1, 1),  # ✅ define full axes area as bbox
    bbox_transform=ax_main.transAxes,
    borderpad=1
)
ax_inset.set_facecolor("#11111a")
ax_inset.tick_params(labelsize=8)

# 3D surface on the right column
ax3d = fig.add_subplot(gs[:, 2], projection='3d')  # spans all rows in right column
ax3d.set_title("Animated Parametric Surface", pad=12)

# Heatmap on lower-left
ax_heat = fig.add_subplot(gs[2, 0])
ax_heat.set_title("Heatmap + Contour", pad=8)

# Polar bar at lower-middle
ax_polar = fig.add_subplot(gs[2, 1], polar=True)
ax_polar.set_title("Angular Distribution (polar)", pad=10)

# Controls area (vertical) — we'll use the upper-left for the slider group
ax_ctrl = fig.add_subplot(gs[0, 1])
ax_ctrl.axis("off")  # will place widgets inside the space

# Space for small legends / image at top-right of the main grid (we'll overlay it)
ax_small = fig.add_subplot(gs[0, 0])
# We'll hide this axes' frame and reuse it for annotations
ax_small.set_xticks([])
ax_small.set_yticks([])
ax_small.patch.set_alpha(0)  # transparent

# ---------------------------
# 4. Populate the plots
# ---------------------------
# Main line + scatter
line_main, = ax_main.plot(t, base_signal, lw=1.8, label="base signal", zorder=2)
scat = ax_main.scatter(scatter_x, scatter_y, s=30, alpha=0.85, edgecolors='w', linewidths=0.6, label="samples", zorder=3)
ax_main.legend(loc='upper left', framealpha=0.3)

# Inset shows a zoomed region — initial window
zoom_center = 6.0
zoom_width = 1.8
def update_inset(center, width):
    mask = (t >= center - width/2) & (t <= center + width/2)
    ax_inset.clear()
    ax_inset.plot(t[mask], base_signal[mask], lw=1.2)
    ax_inset.scatter(scatter_x[(scatter_x >= center-width/2) & (scatter_x <= center+width/2)],
                     scatter_y[(scatter_x >= center-width/2) & (scatter_x <= center+width/2)],
                     s=20, zorder=3)
    ax_inset.set_title("Zoom", fontsize=9)
    ax_inset.tick_params(labelsize=8)
    ax_inset.set_facecolor("#11111a")

update_inset(zoom_center, zoom_width)

# Heatmap with custom normalization and contour overlay
norm = TwoSlopeNorm(vmin=Zheat.min(), vcenter=Zheat.mean(), vmax=Zheat.max())
im = ax_heat.imshow(Zheat, origin='lower', extent=[x.min(), x.max(), y.min(), y.max()], aspect='auto', norm=norm)
cont = ax_heat.contour(Xh, Yh, Zheat, levels=6, linewidths=0.8, alpha=0.9)
ax_heat.set_xlabel("x")
ax_heat.set_ylabel("y")
cb = fig.colorbar(im, ax=ax_heat, fraction=0.046, pad=0.04)
cb.ax.yaxis.set_tick_params(color="#e6e6ff")
for t_tick in cb.ax.get_yticklabels():
    t_tick.set_color("#e6e6ff")

# Polar bars
bars = ax_polar.bar(theta, radii, width=width, bottom=0.0, alpha=0.85)
ax_polar.set_theta_offset(np.pi/2)
ax_polar.set_theta_direction(-1)

# 3D surface initial draw
surf = ax3d.plot_surface(X3, Y3, Z3, rstride=3, cstride=3, cmap='viridis', linewidth=0.2, antialiased=True)
ax3d.set_box_aspect((np.ptp(X3), np.ptp(Y3), np.ptp(Z3)))  # aspect ratio
ax3d.view_init(elev=30, azim=30)

# ---------------------------
# 5. Custom artist: a stylized annotation (vector path + fancy box)
# ---------------------------
# Build a custom curve path and attach as an artist on ax_small
verts = [(0.05, 0.9), (0.15, 0.86), (0.25, 0.88), (0.35, 0.82), (0.48, 0.85)]
codes = [Path.MOVETO] + [Path.CURVE4] * (len(verts) - 1)
path = Path(verts, codes)
patch = PathPatch(path, transform=ax_small.transAxes, facecolor='none', lw=2.0, edgecolor="#ffcc66", alpha=0.95)
ax_small.add_patch(patch)

# Fancy box label
fbox = FancyBboxPatch((0.02, 0.94), 0.3, 0.04, transform=ax_small.transAxes,
                      boxstyle="round,pad=0.02", ec="#66ccff", fc="#2b2b3b", alpha=0.9, lw=1.2)
ax_small.add_patch(fbox)
ax_small.text(0.06, 0.955, r"Matplotlib — Expert Demo", transform=ax_small.transAxes, fontsize=10, va='center')

# ---------------------------
# 6. Procedural small image composited and placed as an annotation
# ---------------------------
def make_small_badge(text="MatPlot"):
    # create an RGBA image with PIL
    W, H = 280, 80
    im = Image.new("RGBA", (W, H), (30, 30, 44, 0))
    draw = ImageDraw.Draw(im)
    # rounded rectangle background
    draw.rounded_rectangle([(4, 4), (W-4, H-4)], radius=14, fill=(45, 55, 80, 230))
    # draw a simple sine icon
    xs = np.linspace(10, W-90, 120)
    ys = (np.sin((xs - 10)/6.5) * 18 + (H/2))
    for i in range(len(xs)-1):
        draw.line([(xs[i], ys[i]), (xs[i+1], ys[i+1])], fill=(255, 200, 90, 255), width=3)
    # add text
    try:
        fnt = ImageFont.truetype("DejaVuSans-Bold.ttf", 20)
    except Exception:
        fnt = ImageFont.load_default()
    draw.text((W-78, H/2 - 10), text, font=fnt, fill=(240, 240, 255, 255))
    return im

badge = make_small_badge("MatPlotX")
# place badge in figure coordinates
imbox_ax = fig.add_axes([0.78, 0.88, 0.18, 0.08], anchor='NE', zorder=10)
imbox_ax.imshow(badge)
imbox_ax.axis("off")

# ---------------------------
# 7. Widgets: Slider (amplitude), Button (reset), Radio (colormap), + event handlers
# ---------------------------
# Slider area inside ax_ctrl (we will draw an axis within that area)
slider_ax = fig.add_axes([0.55, 0.52, 0.33, 0.03])  # x, y, width, height (figure coords)
amp_slider = Slider(slider_ax, "Amplitude", 0.1, 2.0, valinit=1.0)

freq_slider_ax = fig.add_axes([0.55, 0.47, 0.33, 0.03])
freq_slider = Slider(freq_slider_ax, "Freq scale", 0.5, 3.5, valinit=1.0)

reset_ax = fig.add_axes([0.55, 0.41, 0.1, 0.04])
reset_btn = Button(reset_ax, "Reset")

col_ax = fig.add_axes([0.67, 0.41, 0.12, 0.12], facecolor='#11111a')
radio = RadioButtons(col_ax, ("viridis", "plasma", "cividis"), active=0)

# handler logic
def update_signal(val=None):
    A = amp_slider.val
    fscale = freq_slider.val
    new_y = A * np.sin(2 * fscale * t) + 0.3 * np.sin(7 * t)
    line_main.set_ydata(new_y)
    # adjust scatter to follow new signal (for visualization)
    global scatter_y
    scatter_y_mod = np.sin(2 * fscale * scatter_x) + 0.3 * np.sin(7 * scatter_x) + 0.2 * np.random.randn(len(scatter_x))
    scat.set_offsets(np.c_[scatter_x, scatter_y_mod])
    # update inset
    update_inset(zoom_center, zoom_width)
    fig.canvas.draw_idle()

def reset(event):
    amp_slider.reset()
    freq_slider.reset()

def change_cmap(label):
    surf.set_cmap(label)
    im.set_cmap(label)
    fig.canvas.draw_idle()

amp_slider.on_changed(update_signal)
freq_slider.on_changed(update_signal)
reset_btn.on_clicked(reset)
radio.on_clicked(change_cmap)

# ---------------------------
# 8. Animation: rotating 3D surface and an animated trace in main plot
# ---------------------------
# We'll animate: rotate the 3D view and add a moving vertical indicator line on main plot
vline = ax_main.axvline(zoom_center, color="#ff9999", linestyle="--", lw=1.1, zorder=1)
marker, = ax_main.plot([zoom_center], [np.interp(zoom_center, t, base_signal)], marker='o', markersize=6, color="#ffdd66", zorder=4)

def animate(frame):
    # rotate 3D surface
    azim = 30 + frame * 0.6
    elev = 28 + 6 * np.sin(frame * 0.02)
    ax3d.view_init(elev=elev, azim=azim)
    # update vline + marker across t
    pos = 2 + (frame % 800) * (18/800.0)  # cycles through 2..20
    vline.set_xdata([pos, pos])
    # update marker y-value to current underlying line (will follow current sliders)
    current_y = np.interp(pos, t, line_main.get_ydata())
    marker.set_data([pos], [current_y])
    return surf, vline, marker

ani = FuncAnimation(fig, animate, frames=1000, interval=30, blit=False)

# ---------------------------
# 9. Connect interactive click to re-center inset zoom (event-driven)
# ---------------------------
def on_click(event):
    # if click occurs in main axes, re-center the zoom and update inset
    if event.inaxes == ax_main:
        global zoom_center
        zoom_center = event.xdata if event.xdata is not None else zoom_center
        update_inset(zoom_center, zoom_width)
        fig.canvas.draw_idle()

cid = fig.canvas.mpl_connect('button_press_event', on_click)

# ---------------------------
# 10. Final polish: titles, LaTeX, layout tightening
# ---------------------------
# Add a global signature
fig.suptitle(r"\textbf{Matplotlib — Expert Showcase}  $\mathrm{(Animations,\ Interactivity,\ 3D,\ Polar,\ Heatmaps)}$",
             fontsize=16, y=0.97)

# A subtle footer annotation with transform
trans = transforms.blended_transform_factory(fig.transFigure, fig.transFigure)
fig.text(0.01, 0.01, "Generated procedurally — no external assets required", transform=trans, fontsize=8, color="#bfbfdc")

plt.subplots_adjust(left=0.05, right=0.95, top=0.92, bottom=0.06)

# Enable tight layout fallback for overlapping stuff
try:
    fig.tight_layout()
except Exception:
    pass

# ---------------------------
# 11. Show the figure
# ---------------------------
# If running in a script, plt.show() will block until the window is closed.
plt.show()
