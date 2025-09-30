# front_view_xz_autolayer.py
# Usage: python front_view_xz_autolayer.py [in.gcode] [out.png]

import sys, re
from pathlib import Path
import numpy as np
import cv2 as cv

# consts
bed_w   = 220.0   # X span in mm (clamps X)
scale   = 8.0     # pixels per mm
z_eps   = 1e-4    # epsilon for Z comparisons

in_path  = sys.argv[1] if len(sys.argv) > 1 else "screw.gcode"
out_path = sys.argv[2] if len(sys.argv) > 2 else "front_view.png"

text  = Path(in_path).read_text(encoding="utf-8", errors="ignore")
lines = text.splitlines()

# --- Try to detect layer height from header comments ---
m = re.search(r'layer[\s_-]*height\s*[:=]\s*([0-9]*\.?[0-9]+)', text, re.I)
detected_layer_h = float(m.group(1)) if m else None
print(detected_layer_h)
x = y = z = e = 0.0
abs_xy = True  # G90
abs_e  = True  # M82
segments = []
z_max = 0.0
z_deltas = []   # collect positive Z jumps to infer layer height if needed
target_layer = 97   # Layer Print (ON)

# Parse XZ
for raw in lines:
    s = raw.split(";", 1)[0].strip()
    if not s:
        continue

    words = {}
    for tok in s.split():
        L = tok[0].upper()
        V = tok[1:]
        if L.isalpha() and V:
            try:
                words[L] = float(V)
            except ValueError:
                pass

    g = int(words["G"]) if "G" in words else None
    m = int(words["M"]) if "M" in words else None

    if g == 90: abs_xy = True
    elif g == 91: abs_xy = False
    if m == 82: abs_e = True
    elif m == 83: abs_e = False

    px, py, pz, pe = x, y, z, e

    if "X" in words: x = words["X"] if abs_xy else x + words["X"]
    if "Y" in words: y = words["Y"] if abs_xy else y + words["Y"]
    if "Z" in words: z = words["Z"] if abs_xy else z + words["Z"]
    if "E" in words: e = words["E"] if abs_e  else e + words["E"]
    if z - pz > z_eps:
        z_deltas.append(z - pz)

    # Extruding moves → XZ segments
    if g == 1 and e > pe:
        x0, z0 = max(0.0, min(bed_w, px)), max(0.0, pz)
        x1, z1 = max(0.0, min(bed_w, x)),  max(0.0, z)
        segments.append(((x0, z0), (x1, z1)))
        if z0 > z_max: z_max = z0
        if z1 > z_max: z_max = z1

# Layer Height
if detected_layer_h is not None:
    layer_h = detected_layer_h
elif z_deltas:
    layer_h = float(np.median(z_deltas))  # robust against z-hop noise / variable layers
else:
    layer_h = 0.2  # fallback

if target_layer is not None:
    z_top = (target_layer + 1) * layer_h
    segments = [((x0, z0), (x1, z1))
                for ((x0, z0), (x1, z1)) in segments
                if max(z0, z1) <= z_top + 1e-6]
    z_max = z_top

# Rasterize
if z_max <= 0.0:
    z_max = layer_h

w = max(1, int(round(bed_w * scale)))
h = max(1, int(round(z_max * scale)))
img = np.zeros((h, w), np.uint8)
line_w = max(1, int(round(layer_h * scale)))

def to_px(xx, zz):
    xx = max(0.0, min(bed_w, xx))
    zz = max(0.0, min(z_max, zz))
    return (int(round(xx * scale)), int(round((z_max - zz) * scale)))

for (p0, p1) in segments:
    cv.line(img, to_px(*p0), to_px(*p1), 255, line_w, cv.LINE_8)

cv.imwrite(out_path, img)
print(f"wrote {out_path} | segments: {len(segments)} | z_max: {z_max:.3f} mm | layer_h: {layer_h:.3f} mm")

print(z_max)
