import pygame
from ponggame import PongGame
from ponggame.ball import Ball
from ponggame.paddle import Paddle


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