# Importing Libraries
import serial
import time
arduino = serial.Serial(port='COM5', baudrate=115200, timeout=.1)
arduino.timeout = None


def keyclick(key: str):
    arduino.write(bytes(f"k{key}\n", 'utf-8'))


def keypress(key: str):
    arduino.write(bytes(f"u{key}\n", 'utf-8'))


def keyrelease(key: str):
    arduino.write(bytes(f"y{key}\n", 'utf-8'))


def movemouse(x: int, y: int):
    if x > 127:
        x = 127
    if x < -127:
        x = -127
    if y > 127:
        y = 127
    if y < -127:
        y = -127
    arduino.write(bytes(f"m{str(x).zfill(4)}{str(y).zfill(4)}\n", 'utf-8'))
    print(arduino.readline())


def mousereset():
    times = 10
    while times > 0:
        movemouse(-127, -127)
        times -= 1


def mousepress():
    arduino.write(bytes(f"p\n", 'utf-8'))


def mouserightclick():
    arduino.write(bytes(f"b\n", 'utf-8'))


def mouserelease():
    arduino.write(bytes(f"h\n", 'utf-8'))


def mouseclick():
    mousepress()
    time.sleep(.5)
    mouserelease()
