import random
import time
import pyautogui
import arduino
import eyes

greenColor = (0, 240, 171)
orangeColor = (239, 113, 22)
maxElapsedTime = 5
colorThreshold = 15


def fish():
    print('initiating fish action...')
    arduino.mousepress()
    time.sleep(random.uniform(1.8, 2.1))
    arduino.mouserelease()

    fishing = None
    print('waiting fish action...')
    startWaitingTime = time.time()
    while fishing is None:
        fishing = eyes.lookAnywhere('fishing.png')
        now = time.time()
        elapsed = now - startWaitingTime
        if elapsed > 6:
            time.sleep(random.uniform(.5, 1.5))
            return

    print('now fishing')

    gotfish = None
    print('waiting fish...')
    while gotfish is None:
        gotfish = eyes.lookAnywhere('gotfish.png')

    print('got fish')

    arduino.mouseclick()
    fishing = True
    clicking = False
    lastNotFoundTime = time.time()
    while fishing:
        green = eyes.lookAnywhere('green.png', threshold=0.3)
        if green and not clicking:
            arduino.mousepress()
            clicking = True
            lastNotFoundTime = time.time()
            time.sleep(random.uniform(1, 2))
        if green is None:
            if clicking:
                arduino.mouserelease()
                clicking = False
                lastNotFoundTime = time.time()
            else:
                if (time.time() - lastNotFoundTime) > maxElapsedTime:
                    break
    arduino.mouseclick()


def locate_color(color, point) -> bool:
    s = pyautogui.screenshot(
        region=(point[0]-50, point[1]-50, point[0]+50, point[1]+50))
    for x in range(s.width):
        for y in range(s.height):
            pixel = s.getpixel((x, y))
            if pixel[0] > color[0] - colorThreshold and pixel[0] < color[0] + colorThreshold and \
                    pixel[1] > color[1] - colorThreshold and pixel[1] < color[1] + colorThreshold and \
                    pixel[2] > color[2] - colorThreshold and pixel[2] < color[2] + colorThreshold:
                return True
    return False


def repair():
    print('start repairing')
    arduino.keyclick('\t')
    time.sleep(random.uniform(.2, .6))
    repair = None
    while repair is None:
        repair = eyes.lookAnywhere('repair.png', threshold=0.3)
    print(f'repair {repair}')
    arduino.mousereset()
    time.sleep(random.uniform(.2, .6))
    print('moving mouse')
    times = 10
    while times > 0:
        arduino.movemouse(repair[0], repair[1])
        times -= 1
    print('mouse moved')
    time.sleep(random.uniform(.2, .6))
    arduino.mouseclick()
    time.sleep(random.uniform(.2, .6))


def fishing():
    time.sleep(3)
    arduino.mousereset()
    time.sleep(2)
    arduino.mouseclick()
    while True:
        time.sleep(random.uniform(1, 3))
        fish()
        print('Fishing done')


def repairing():
    time.sleep(3)
    print('reset mouse')
    arduino.mousereset()
    time.sleep(2)
    print('click')
    arduino.mouseclick()
    repair()


repairing()
