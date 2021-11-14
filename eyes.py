import cv2
import numpy as np
from PIL import Image
import pyautogui


def lookAnywhere(template, threshold=0.1):
    img = pyautogui.screenshot()
    return look(img, template, threshold)


def look(image, template, threshold=0.1):
    method = cv2.TM_SQDIFF_NORMED
    small_image = cv2.imread(template)
    large_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    result = cv2.matchTemplate(small_image, large_image, method)
    mnVal, _, mnLoc, _ = cv2.minMaxLoc(result)
    MPx, MPy = mnLoc
    if mnVal > threshold:
        # print(f"{template} not found with {mnVal}")
        return None
    im = Image.open(template)
    width, height = im.size
    return MPx + (width//2), MPy + (height//2)
