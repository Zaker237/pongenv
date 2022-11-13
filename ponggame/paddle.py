import pygame
from ponggame.utils import WHITE, PADDLE_STATE


class Paddle(object):
    COLOR = WHITE
    VELOCITY = 4

    def __init__(self, x, y, width, height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win):
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True):
        if up:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y