import numpy as np
import time

class Game:

    def __init__(self, vision, controller):
        self.vision = vision
        self.controller = controller
        self.state = 'not started'

    def run(self):
        while True:
            self.vision.refresh_frame()
            if self.procurar_poring():
                pass
            else:
                self.log('Not doing anything')
                self.controller.random_walk()

    def procurar_poring(self):
        scales = [1.2, 1.1, 1.02, 1.01, 1.0, 0.99, 0.95]
        matches = self.vision.scaled_find_template('poring', threshold=0.75, scales=scales)
        if np.shape(matches)[1] >= 1:
            x = matches[1][0]
            y = matches[0][0]
            self.log("Achou o poring")
            self.controller.atacar(x, y)
            
        return np.shape(matches)[1] >= 1

    def log(self, text):
        print('[%s] %s' % (time.strftime('%H:%M:%S'), text))
