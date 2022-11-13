import pygame
from ponggame.utils import WHITE, PADDLE_STATE


class Paddle(object):
    COLOR = WHITE
    VELOCITY = 4

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, win) ->None:
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))

    def move(self, up=True) -> None:
        if up:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY

    def reset(self) ->None:
        self.x = self.original_x
        self.y = self.original_y

    def as_state(self) ->PADDLE_STATE:
        return(
            self.x,
            self.y,
            self.width,
            self.height
        )
