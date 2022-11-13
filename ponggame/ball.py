import pygame
from ponggame.utils import WHITE

class Ball(object):
    MAX_VELOCITY = 5
    COLOR = WHITE

    def __init__(self, x, y, raduis):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.raduis = raduis
        self.x_velocity = self.MAX_VELOCITY
        self.y_velocity = 0

    def draw(self, win):
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.raduis)

    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.x_velocity *= -1
        # self.x_velocity = self.MAX_VELOCITY
        self.y_velocity = 0