# file: main_bg_compare.py
# Minimal "router" that selects one of 25 background deletion images based on current Z (mm)
# and calls your downstream processing function.
import face_view as fv
from pathlib import Path
from typing import Optional, Tuple

# ------------ config ------------
# First printed Z and layer height for converting Z <-> layer (edit to your slicer settings)
FIRST_LAYER_Z = 0.20     # mm
LAYER_HEIGHT  = 0.20     # mm  (your "Layer_Height")

# Match window for Z milestones (accounts for mesh/babystepping jitter)
Z_TOL = 0.05  # mm

# Define 25 background slots with their target Z heights (mm) and file paths.
# Edit the Zs and paths to match your background captures.
BG_MILESTONES: list[Tuple[float, str]] = [
    (-2.0,  "imgs/bkgnd_00.jpg"),
    (-1.0,  "imgs/bkgnd_01.jpg"),
    (0.0,  "imgs/bkgnd_02.jpg"),
    (1.0,  "imgs/bkgnd_03.jpg"),
    (2.0,  "imgs/bkgnd_04.jpg"),
    (3.0,  "imgs/bkgnd_05.jpg"),
    (4.0,  "imgs/bkgnd_06.jpg"),
    (5.0,  "imgs/bkgnd_07.jpg"),
    (6.0,  "imgs/bkgnd_08.jpg"),
    (7.0,  "imgs/bkgnd_09.jpg"),
    (8.0, "imgs/bkgnd_10.jpg"),
    (9.0, "imgs/bkgnd_11.jpg"),
    (10.0, "imgs/bkgnd_12.jpg"),
    (13.0, "imgs/bkgnd_13.jpg"),
    (16.0, "imgs/bkgnd_14.jpg"),
    (19.0, "imgs/bkgnd_15.jpg"),
    (22.0, "imgs/bkgnd_16.jpg"),
    (25.0, "imgs/bkgnd_17.jpg"),
    (28.0, "imgs/bkgnd_18.jpg"),
    (30.0, "imgs/bkgnd_19.jpg"),
    (35.0, "imgs/bkgnd_20.jpg"),
    (40.0, "imgs/bkgnd_21.jpg"),
    (45.0, "imgs/bkgnd_22.jpg"),
    (50.0, "imgs/bkgnd_23.jpg"),
    (55.0, "imgs/bkgnd_24.jpg"),
]
# --------------------------------


# === Your variable names ===
# Curr_Layer_Height = detected layer height in mm (i.e., current Z of the print)
# Curr_Layer        = current layer number (if you have it; otherwise None)
# Layer_Height      = layer height for front view (we use LAYER_HEIGHT)
# s_IMG             = slicer image path for this moment
# r_IMG             = real image path captured at this moment


def Z_HEIGHT2LAYER(curr_Layer_Height: float,
                   first_layer_z: float = FIRST_LAYER_Z,
                   layer_h: float = LAYER_HEIGHT) -> int:
    """
    Convert current Z (aka Curr_Layer_Height) -> integer layer index.
    Rounds to nearest layer index based on first printed Z and nominal layer height.
    """
    if layer_h <= 0:
        raise ValueError("layer_h must be > 0")
    # shift by first-layer Z, then divide by layer height
    return max(0, int(round((curr_Layer_Height - first_layer_z) / layer_h)))


def _pick_bg_by_z(curr_z: float, tol: float = Z_TOL) -> Optional[str]:
    """Return the background image path whose milestone Z matches curr_z within ±tol."""
    for z_target, bg_path in BG_MILESTONES:
        if abs(curr_z - z_target) <= tol:
            return bg_path
    return None


# ---- hook to your processing code ----
def run_bg_diff(bg_path: str, s_IMG: str, r_IMG: str) -> None:
    """
    Call your existing diff/cleanup pipeline here.
    Replace this body with: from your_module import process; process(bg_path, s_IMG, r_IMG)
    Keep it minimal for now.
    """
    print(f"[COMPARE] bg={bg_path}  s_IMG={s_IMG}  r_IMG={r_IMG}")


# ---- single-step entrypoint you call from your poller/timer ----
def step_compare(curr_z: Optional[float],
                 s_IMG: str,
                 r_IMG: str,
                 curr_layer: Optional[int] = None,
                 prefer_layer: bool = False) -> Optional[str]:
    """
    Decide which background to use and run the comparison once.
    Returns the bg path used, or None if no milestone matched.
    - If prefer_layer=True and curr_layer is provided, tries layer-based selection first.
    - Otherwise falls back to Z-based selection.
    """
    bg = None
    if prefer_layer and curr_layer is not None:
        bg = _pick_bg_by_layer(curr_layer)

    if bg is None and curr_z is not None:
        bg = _pick_bg_by_z(curr_z)

    if bg is None:
        return None  # no milestone hit this tick

    # Sanity: ensure the file exists; skip if missing
    if not Path(bg).exists():
        print(f"[SKIP] Missing background file: {bg}")
        return None

    run_bg_diff(bg, s_IMG, r_IMG)
    return bg


# ----------------- example usage -----------------
if __name__ == "__main__":
    # Example values; replace these with your live data feed:
    Curr_Layer_Height = 10.02  # <- your current Z (mm)
    Curr_Layer        = None   # or an int if you have true layer
    s_IMG             = "slicer_imgs/z_10.0.png"
    r_IMG             = "real_imgs/z_10.0.jpg"

    used_bg = step_compare(
        curr_z=Curr_Layer_Height,
        s_IMG=s_IMG,
        r_IMG=r_IMG,
        curr_layer=Curr_Layer,
        prefer_layer=False
    )
    if used_bg:
        print(f"[OK] Used background: {used_bg}")
    else:
        print("[WAIT] No milestone matched this tick.")
