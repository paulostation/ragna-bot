import cv2
from mss import mss
from PIL import Image
import numpy as np
from time import sleep
import win32gui

GAME_RES = (800, 600)

class Vision:
    def __init__(self):
        self.static_templates = {
            
            'planta_carnivora': 'assets/1368.png',
        }

        self.templates = { k: cv2.imread(v, 0) for (k, v) in self.static_templates.items() }

        rect = self.find_game_window()

        self.monitor = {
            # 'top': int((1080 / 2) - (GAME_RES[1] / 2)), 'left': int((1920 / 2) - (GAME_RES[0] / 2)), 'width': GAME_RES[0] + 20, 'height': GAME_RES[1] + 20
            'top': 0, 'left': 0, 'width': 1920, 'height': 1080
        }
        self.screen = mss()

        self.frame = None

    def take_screenshot(self):
        sct_img = self.screen.grab(self.monitor)
        img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
        img = np.array(img)
        img = self.convert_rgb_to_bgr(img)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(img_gray,cv2.CV_64F)
        cv2.imwrite("ss.png", laplacian)

        return img_gray

    def find_game_window(self):
        print("About to grab game coordinates, please open the game.")

        answer = input("Is the game open?")
        proceed = answer.lower() == 'y'
        while not proceed:
            answer = input("Is the game open?")
            proceed = answer.lower() == 'y'
        
        print("Waiting 3 seconds to open game window...")
        sleep(3)
        # Detect the window 
        windows_list = []
        toplist = []
        def enum_win(hwnd, result):
            win_text = win32gui.GetWindowText(hwnd)
            windows_list.append((hwnd, win_text))

        win32gui.EnumWindows(enum_win, toplist)

        # Game handle
        game_hwnd = 0
        for (hwnd, win_text) in windows_list:
            if "Ragnarok" in win_text:
                game_hwnd = hwnd
        rect = win32gui.GetWindowRect(game_hwnd)
        return rect
            

    def get_image(self, path):
        return cv2.imread(path, 0)

    def bgr_to_rgb(self, img):
        b,g,r = cv2.split(img)
        return cv2.merge([r,g,b])

    def convert_rgb_to_bgr(self, img):
        return img[:, :, ::-1]

    def match_template(self, img_grayscale, template, threshold=0.9):
        """
        Matches template image in a target grayscaled image
        """

        res = cv2.matchTemplate(img_grayscale, template, cv2.TM_CCOEFF_NORMED)
        matches = np.where(res >= threshold)
        return matches

    def find_template(self, name, image=None, threshold=0.9):
        if image is None:
            if self.frame is None:
                self.refresh_frame()

            image = self.frame

        return self.match_template(
            image,
            self.templates[name],
            threshold
        )

    def scaled_find_template(self, name, image=None, threshold=0.9, scales=[1.0, 0.9, 1.1]):
        if image is None:
            if self.frame is None:
                self.refresh_frame()

            image = self.frame

        initial_template = self.templates[name]
        for scale in scales:
            scaled_template = cv2.resize(initial_template, (0,0), fx=scale, fy=scale)
            matches = self.match_template(
                image,
                scaled_template,
                threshold
            )
            if np.shape(matches)[1] >= 1:
                return matches
        return matches

    def refresh_frame(self):
        self.frame = self.take_screenshot()
