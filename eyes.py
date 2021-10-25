import cv2
import numpy as np
import time
import pyautogui


def lookAnywhere():
    start = time.time()
    img = pyautogui.screenshot()
    res = look(img)
    end = time.time()
    print(f"lookAnywhere: {end - start} {res}")


def look(image):
    method = cv2.TM_SQDIFF_NORMED
    small_image = cv2.imread('fishing.png')
    large_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    result = cv2.matchTemplate(small_image, large_image, method)
    mnVal, _, mnLoc, _ = cv2.minMaxLoc(result)
    MPx, MPy = mnLoc
    if mnVal > 0.1:
        return None
    return MPx, MPy
