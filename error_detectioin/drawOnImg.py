import cv2 as cv
import numpy as np

points = []
def click_event(event, x, y, flags, param):
    if event == cv.EVENT_LBUTTONDOWN:
        points.append((x, y))
        cv.circle(img, (x,y), 3, (0,0,255), -1)
        cv.imshow("image", img)

img = cv.imread("front_view.png")
cv.imshow("image", img)
cv.setMouseCallback("image", click_event)
cv.waitKey(0)
cv.destroyAllWindows()

print("Polygon points:", points)