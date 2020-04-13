import math
import random

class Actor:
    def __init__(self, name, image, image_x_size, image_y_size, x, y, x_change, y_change, state=""):
        self.type = name
        self.image = image
        self.image_x_size = image_x_size
        self.image_y_size = image_y_size
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.x_change = x_change
        self.y_change = y_change
        self.state = state

    def stay_inbound(self, auto_go_down=False):
        if self.x <= 0:
            self.x = 0
            if auto_go_down:
                self.y += self.y_change
                self.x_change = self.x_change * -1
        elif self.x >= (800 - self.image_x_size):
            self.x = (800 - self.image_x_size)
            if auto_go_down:
                self.y += self.y_change
                self.x_change = self.x_change * -1

    def move_auto(self):
        if self.state != "end":
            self.x += self.x_change
            self.stay_inbound(True)

    def move_right(self):
        if self.state != "end":
            self.x += self.x_change
            self.stay_inbound()

    def move_left(self):
        if self.state != "end":
            self.x -= self.x_change
            self.stay_inbound()

    def move_up(self):
        if self.state != "end":
            self.y -= self.y_change

    def stop_moving(self):
        self.x -= 0
        self.stay_inbound()

    def reset(self, random_change_x=True):
        if self.state != "end":
            self.x = self.original_x
            self.y = self.original_y
            if random_change_x:
                self.x_change = random.randint(1, 3)

    def is_hit(self, actor):
        distance = math.sqrt(math.pow((self.x - actor.x), 2) + math.pow((self.y - actor.y), 2))
        if distance < 27:
            return True
        return False

    def change_state(self, new_state):
        self.state = new_state
