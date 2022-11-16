import pygame
from ponggame.utils import WHITE, PADDLE_STATE


class Paddle(object):
    """The Paddle object represent the paddle used in pong game.

    :param original_x: The original x position of the paddle on the game board.
    :param original_y: The original y position of the paddle on the game board.
    :param x: The current x position of the paddle on the game board.
    :param y: The current y position of the paddle on the game board.
    :param width: The width of of the paddle.
    :param height: The height of of the paddle.
    """
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
