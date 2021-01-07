import time

import pydirectinput



class Controller:
    def __init__(self):
        self.mouse = MouseController()
        self.keyboard = KeyboardController()

    def adagas_ninja(self):

        self.keyboard.press('5')
        time.sleep(0.15)
        self.keyboard.release('5')
        time.sleep(0.5)
        self.keyboard.press('8')
        time.sleep(0.15)
        self.keyboard.release('8')
        time.sleep(0.5)
        self.keyboard.press('5')
        time.sleep(0.15)
        self.keyboard.release('5')
        time.sleep(0.5)
        self.keyboard.press('Z')
        time.sleep(0.15)
        self.keyboard.release('Z')

    def keypresses(self, keys, delays=None):

        if not delays:
            delays = [0.5 for n in keys]

        for i, key in enumerate(keys):
            pydirectinput.keyDown(key)
            time.sleep(0.01)
            pydirectinput.keyUp(key)
            time.sleep(delays[i])

    def press_and_hold(self, key, duration=1):

        pydirectinput.keyDown(key)
        time.sleep(duration)
        pydirectinput.keyUp(key)

    def atacar(self):
        pydirectinput.keyDown('z')
        time.sleep(0.01)
        pydirectinput.keyUp('z')
        time.sleep(1)

    def combo(self):

        self.keypresses(
            ['z', 'z', 'z'],
            delays=[0.05, 0.05, 0.05]
        )

    def run_left(self, duration=3):

        self.run('left', duration)

    def run_right(self, duration=3):

        self.run('right', duration)

    def jump(self, duration=3):

        self.keypresses(
            'up'
        )

    def walk_right(self, duration=3):

        self.walk('right', duration)

    def walk_left(self, duration=3):

        self.walk('left', duration)

    def walk(self, direction, duration):

        self.press_and_hold(direction, duration)

    def adaga(self):

        self.keypresses(
            ['up', 'up'],
            [0.5, 0.5]
        )

        pydirectinput.keyDown('down')
        time.sleep(0.01)
        pydirectinput.keyDown('z')
        time.sleep(0.01)
        pydirectinput.keyUp('z')
        time.sleep(0.01)
        pydirectinput.keyUp('down')


    def run(self, direction, duration):

        self.keypresses(
            [direction],
            delays=[0.001]
        )

        self.press_and_hold(direction, duration)

    def fatiar(self):

        self.keypresses(
            ['z'],
            delays=[0.0002]
        )

    def special_1(self):

        self.press_and_hold('z')

    def special_2(self):

        self.press_and_hold('z', duration=2)

    def move_mouse(self, x, y):
        def set_mouse_position(x, y):
            self.mouse.position = (int(x), int(y))
        def smooth_move_mouse(from_x, from_y, to_x, to_y, speed=0.2):
            steps = 40
            sleep_per_step = speed // steps
            x_delta = (to_x - from_x) / steps
            y_delta = (to_y - from_y) / steps
            for step in range(steps):
                new_x = x_delta * (step + 1) + from_x
                new_y = y_delta * (step + 1) + from_y
                set_mouse_position(new_x, new_y)
                time.sleep(sleep_per_step)
        return smooth_move_mouse(
            self.mouse.position[0],
            self.mouse.position[1],
            x,
            y
        )

    def left_mouse_click(self):
        self.mouse.click(Button.left)

    def left_mouse_drag(self, start, end):
        self.move_mouse(*start)
        time.sleep(0.2)
        self.mouse.press(Button.left)
        time.sleep(0.2)
        self.move_mouse(*end)
        time.sleep(0.2)
        self.mouse.release(Button.left)
        time.sleep(0.2)
