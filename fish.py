# 3 horas
# shutdown /s /t 10000
# 1 hora
# shutdown /s /t 3600
import random
import time
from numpy import isinf
import pyautogui
import arduino
import eyes

greenColor = (0, 240, 171)
orangeColor = (239, 113, 22)
maxElapsedTime = 5
colorThreshold = 15
repairIn = 10
moveIn = 2
horizontalMoves = 20
horizontalTicks = 50
fails = 1


def fish():
    global fails
    print('initiating fish action...')
    fishingmode = eyes.lookAnywhere('fishing_mode.png', threshold=0.2)
    if fishingmode == None:
        arduino.keyclick('i')
    arduino.mousepress()
    time.sleep(random.uniform(1.9, 2.05))
    arduino.mouserelease()

    fishing = None
    print('waiting fish action...')
    startWaitingTime = time.time()
    while fishing is None:
        fishing = eyes.lookAnywhere('fishing.png')
        now = time.time()
        elapsed = now - startWaitingTime
        if elapsed > maxElapsedTime:
            fails += 1
            return

    print('now fishing')

    gotfish = None
    print('waiting fish...')
    startWaitingTime2 = time.time()
    while gotfish is None:
        gotfish = eyes.lookAnywhere('gotfish.png')
        now = time.time()
        elapsed = now - startWaitingTime2
        if elapsed > 50:
            fails += 1
            return

    print('got fish')
    fails = 0

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
            time.sleep(random.uniform(1, 1.5))
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


def clickRef(ref):
    found = None
    timeout = time.time()
    while found is None:
        found = eyes.lookAnywhere(ref, threshold=0.3)
        if (time.time() - timeout) > 5:
            arduino.keyclick('\n')
            return
    time.sleep(random.uniform(.2, .6))
    arduino.movemouse(found[0], found[1])
    time.sleep(random.uniform(.2, .6))
    arduino.mouseclick()
    time.sleep(random.uniform(.2, .6))


def repair():
    print('start repairing')
    arduino.keyclick('\t')
    time.sleep(random.uniform(.2, .6))
    # clickRef('repair.png')
    # repair start
    arduino.movemouse(605, 1027)
    time.sleep(random.uniform(.2, .6))
    arduino.mouseclick()
    time.sleep(random.uniform(.2, .6))
    # repair end
    clickRef('yes.png')
    arduino.keyclick('\t')
    time.sleep(1)


def nomenu():
    timeout = time.time()
    menu = eyes.lookAnywhere('menu.png', threshold=0.3)
    while menu != None:
        arduino.keyclick('\t')
        time.sleep(1)
        menu = eyes.lookAnywhere('menu.png', threshold=0.3)
        if (time.time() - timeout) > 5:
            print('pressing enter')
            arduino.keyclick('\n')
            return


def move():
    arduino.keypress('s')
    time.sleep(1.2)
    arduino.keyrelease('s')
    time.sleep(random.uniform(.2, .6))
    arduino.keypress('w')
    time.sleep(.75)
    arduino.keyrelease('w')
    time.sleep(random.uniform(.2, .6))
    # arduino.keypress('a')
    # time.sleep(1)
    # arduino.keyrelease('a')
    # time.sleep(random.uniform(.2, .6))
    # arduino.keypress('d')
    # time.sleep(1.3)
    # arduino.keyrelease('d')


def fishing():
    global fails
    time.sleep(1)
    arduino.keyclick('i')
    times = 0
    movetimes = 0
    while True:
        print(f'fails {fails}')
        nomenu()
        if fails > 2:
            for _ in range(horizontalMoves):
                arduino.movemouserelative(horizontalTicks)
                time.sleep(random.uniform(.1, .2))
        fishingmode = eyes.lookAnywhere('fishing_mode.png', threshold=0.2)
        if fishingmode == None:
            arduino.keyclick('i')
        time.sleep(random.uniform(1, 3))
        fish()
        print(f'Fishing done {times}')
        times += 1
        if times > repairIn:
            repair()
            times = 0
        movetimes += 1
        if movetimes > moveIn:
            move()
            movetimes = 0


fishing()
