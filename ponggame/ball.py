import pygame
from ponggame.utils import WHITE, BALL_STATE


class Ball(object):
    """The Ball object represents the ball used in pong game.

    :param x: The current x position of the paddle on the game board.
    :param y: The current y position of the paddle on the game board.
    :param raduis: The raduis of the ball.
    """
    MAX_VELOCITY = 5
    COLOR = WHITE

    def __init__(self, x: int, y: int, raduis: float) ->None:
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.raduis = raduis
        self.x_velocity = self.MAX_VELOCITY
        self.y_velocity = 0

    def draw(self, win) ->None:
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.raduis)

    def move(self) ->None:
        self.x += self.x_velocity
        self.y += self.y_velocity

    def update_velocity(self, factor) ->None:
        pass

    def reset(self) ->None:
        self.x = self.original_x
        self.y = self.original_y
        self.x_velocity *= -1
        # self.x_velocity = self.MAX_VELOCITY
        self.y_velocity = 0

    def as_state(self) ->BALL_STATE:
        return (
            self.x,
            self.y,
            self.raduis,
            self.x_velocity,
            self.y_velocity
        )
