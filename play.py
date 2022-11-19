import pygame
import numpy as np
from numpy.random import MT19937
from numpy.random import RandomState, SeedSequence
from typing import List
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


FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")


def draw(win, paddles: List[PyGamePaddle], ball: PyGameBall, bottom_score: int, top_score: int) ->None:
    # fill the backgroud in black
    win.fill(BLACK)
    bottom_score_text = SCORE_FONT.render(f"Score: {bottom_score}", 1, WHITE)
    top_score_text = SCORE_FONT.render(f"Score: {top_score}", 1, WHITE)
    win.blit(bottom_score_text, (WIDTH//4 - bottom_score_text.get_width()//2, 20))
    win.blit(top_score_text, (WIDTH*(3/4) - top_score_text.get_width()//2, 20))

    for paddle in paddles:
        paddle.draw(win)
    
    ball.draw(win)
    # draw the separator
    for i in range(10, WIDTH, WIDTH//20):
        if i % 2 == 1:
            continue
        else:
            pygame.draw.rect(win, WHITE, (i, HEIGHT//2 - 5, WIDTH//20, 10))

    pygame.display.update()


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

    b_score = 0
    t_score = 0

    while run:
        clock.tick(FPS)
        draw(WIN, [b_paddle, t_paddle], ball, b_score, t_score)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        keys = pygame.key.get_pressed()
        
        # handel_paddel_movement(keys, b_paddle, t_paddle)

        ball.move()
        # handel_collision(ball, b_paddle, t_paddle)



if __name__ == "__main__":
    main()