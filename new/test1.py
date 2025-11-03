import cv2 as cv
import numpy as np
from pathlib import Path

# --- inputs (fixed) ---
BG_PATH   = "bkgnd_13.jpg"
REAL_PATH = "test.jpg"

#ROI
POLY_PTS = [(1608, 1351), (3230, 1308), (4339, 1666), (571, 1704)]  # or []

def main():
    bg   = cv.imread(BG_PATH,  cv.IMREAD_GRAYSCALE)
    real = cv.imread(REAL_PATH, cv.IMREAD_GRAYSCALE)

    if real.shape != bg.shape:
        real = cv.resize(real, (bg.shape[1], bg.shape[0]), interpolation=cv.INTER_AREA)

    H, W = bg.shape
    mask = np.zeros((H, W), dtype=np.uint8)
    if POLY_PTS:
        cv.fillPoly(mask, [np.array(POLY_PTS, np.int32)], 255)
    else:
        mask[:, :] = 255  # full image

    # Backround subtraction post mask
    diff = cv.absdiff(real, bg)
    diff = cv.bitwise_and(diff, diff, mask=mask)

    # Processing steps
    blur = cv.medianBlur(diff, 15)
    _th, thresh = cv.threshold(blur,0,255,cv.THRESH_BINARY | cv.THRESH_OTSU)

    canny = cv.Canny(thresh, 15, 50)

   # output
    cv.imwrite('Canny.png', canny)
    cv.imwrite('Diff.png', diff)
    cv.imwrite('Blur.png', blur)
    cv.imwrite('Thresh.png', thresh)
    print("Done.")




if __name__ == "__main__":
   main()
