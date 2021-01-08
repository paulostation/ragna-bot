
import time
from ahk import AHK
from random import randint

class Controller:
    def __init__(self):
        self.mouse = AHK()
        self.keyboard = None#KeyboardController()

    def random_walk(self):
        offset_x = 3
        offset_y = 22

        center_x = (1024 + offset_x) / 2
        center_y = (768 + offset_y) / 2

        range = 150
        x = center_x + randint(-range, range)
        y = center_y + randint(-range, range)
        self.mouse.mouse_move(x=x, y=y, speed=3, blocking=True)
        time.sleep(0.5)
        self.mouse.click(x, y)
        time.sleep(0.5)

    def atacar(self, x, y):
        x += 25
        y += 25
        
        print("About to  attack")
        
        self.mouse.mouse_position = (x, y)
        time.sleep(0.2)
        self.mouse.click()
        time.sleep(5)