import pygame
from ponggame import Ball, Paddle, PongGame
from ponggame.utils import WIDTH, HEIGHT, PADDLE_HEIGHT, PADDLE_WIDTH
from ponggame.utils import BALL_RADUIS, WHITE, BLACK, SCORE_FONT


class PyGameBall(Ball):
    def __init__(self, x: int, y: int, raduis: float) -> None:
        super().__init__(x, y, raduis)

    def draw(self, win) ->None:
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.raduis)


class PyGamePaddle(Paddle):
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        super().__init__(x, y, width, height)

    def draw(self, win) ->None:
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))