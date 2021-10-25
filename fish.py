import random
import time
import pyautogui
import arduino

greenColor = (0, 240, 171)
orangeColor = (239, 113, 22)
squareSize = 30
maxElapsedTime = 6
colorThreshold = 15
pxModifier = 4
verticalOffset = 5000


def fish():
    print('initiating fish action...')
    arduino.mousepress()
    time.sleep(random.uniform(1.8, 2.1))
    arduino.mouserelease()

    fishing = None
    print('waiting fish action...')
    startWaitingTime = time.time()
    while fishing is None:
        fishing = pyautogui.locateCenterOnScreen('fishing.png', confidence=0.8)
        now = time.time()
        elapsed = now - startWaitingTime
        if elapsed > 6:
            time.sleep(random.uniform(.5, 1.5))
            return

    # arduino.movemouse(str(fishing[0]).zfill(4), str(fishing[1]).zfill(4))
    print('now fishing')

    gotfish = None
    print('waiting fish...')
    while gotfish is None:
        gotfish = pyautogui.locateCenterOnScreen('gotfish.png', confidence=0.8)

    print('got fish')

    arduino.mouseclick()
    fishing = True
    clicking = False
    lastNotFoundTime = time.time()
    while fishing:
        greenfound = locate_color(greenColor, gotfish)
        if greenfound and not clicking:
            print('clicking...')
            arduino.mousepress()
            clicking = True
            lastNotFoundTime = time.time()
        if not greenfound:
            if clicking:
                print('releasing...')
                arduino.mouserelease()
                clicking = False
                lastNotFoundTime = time.time()
            else:
                if (time.time() - lastNotFoundTime) > maxElapsedTime:
                    print('finished')
                    break
    print('cancel animation')
    arduino.mouseclick()


def locate_color(color, point: pyautogui.Point) -> bool:
    s = pyautogui.screenshot(
        region=(point.x-100, point.y-10, point.x+100, point.y+verticalOffset))
    for x in range(s.width // pxModifier):
        for y in range(s.height // pxModifier):
            pixel = s.getpixel((x*pxModifier, y*pxModifier))
            if pixel[0] > color[0] - colorThreshold and pixel[0] < color[0] + colorThreshold and \
                    pixel[1] > color[1] - colorThreshold and pixel[1] < color[1] + colorThreshold and \
                    pixel[2] > color[2] - colorThreshold and pixel[2] < color[2] + colorThreshold:
                return True
    return False


time.sleep(1)
arduino.mousereset()
time.sleep(3)
arduino.mouseclick()
while True:
    time.sleep(random.uniform(1, 3))
    fish()
    print('Fishing done')
