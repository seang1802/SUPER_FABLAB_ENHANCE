import QIDI-Z-AXIS
import face_view 
from pathlib import Path
from typing import Optional, Tuple

FIRST_LAYER_Z = 0.20     # mm
LAYER_HEIGHT  = 0.20     # mm  (your "Layer_Height")
CURR_Z = face_view.FUNC 


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


