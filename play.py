import pygame
import numpy as np
from numpy.random import MT19937
from numpy.random import RandomState, SeedSequence

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


WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

def main() ->None:
    run = True
    clock = pygame.time.Clock()
    rng = RandomState(MT19937(SeedSequence(987654321)))
    run = True
    clock = pygame.time.Clock()

    b_paddle = PyGamePaddle(
        WIDTH//2 - PADDLE_WIDTH//2,
        10,
        PADDLE_WIDTH,
        PADDLE_HEIGHT
    )
    t_paddle = PyGamePaddle(
        WIDTH//2 - PADDLE_WIDTH//2,
        HEIGHT - 10 - PADDLE_HEIGHT,
        PADDLE_WIDTH,
        PADDLE_HEIGHT
    )

    ball = PyGameBall(WIDTH//2, HEIGHT//2, BALL_RADUIS)

    game = PongGame(
        ball,
        t_paddle,
        b_paddle,
        rng,
        win_score=10,
        game_height=HEIGHT,
        game_width=WIDTH
    )


if __name__ == "__main__":
    main()