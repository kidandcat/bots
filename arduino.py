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


def movemouse(x: str, y: str):
    arduino.write(bytes(f"m{x}{y}\n", 'utf-8'))
    print(arduino.readline())


def mousereset():
    arduino.write(bytes(f"r\n", 'utf-8'))
    print(arduino.readline())


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
