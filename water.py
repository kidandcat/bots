import random
import time
import arduino

while True:
    time.sleep(random.uniform(3.9, 4.1))
    arduino.keyclick('e')
