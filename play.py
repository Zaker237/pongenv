import pygame
pygame.init()
import numpy as np
from numpy.random import MT19937
from numpy.random import RandomState, SeedSequence
from typing import List
from ponggame.game import Ball, Paddle, PongGame
from ponggame.configs import WIDTH, HEIGHT, PADDLE_HEIGHT, PADDLE_WIDTH
from ponggame.configs import BALL_RADUIS, WHITE, BLACK
from gameenv.utils import Action


class PyGameBall(Ball):
    COLOR = (255, 255, 255)
    def __init__(self, x: int, y: int, raduis: float) -> None:
        super().__init__(x, y, raduis)

    def draw(self, win) ->None:
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.raduis)


class PyGamePaddle(Paddle):
    COLOR = (255, 255, 255)
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        super().__init__(x, y, width, height)

    def draw(self, win) ->None:
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.width, self.height))


FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
SCORE_FONT = pygame.font.SysFont("comicsans", 40)


def draw(win, paddles: List[PyGamePaddle], ball: PyGameBall, scores: np.ndarray) ->None:
    # fill the backgroud in black
    win.fill(BLACK)
    bottom_score_text = SCORE_FONT.render(f"{scores[1]}", 1, WHITE)
    top_score_text = SCORE_FONT.render(f"{scores[0]}", 1, WHITE)
    win.blit(top_score_text, (20, HEIGHT//2 - 10 - 20 - top_score_text.get_height()/2))
    win.blit(bottom_score_text, (20, HEIGHT//2 - 10 + 20 + bottom_score_text.get_height()/2))

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


def handel_paddel_movement(keys, b_paddle: Paddle, t_paddle: Paddle):
    if keys[pygame.K_d] and b_paddle.x + b_paddle.VELOCITY + b_paddle.width <= WIDTH:
        b_paddle.move(right=True)
    if keys[pygame.K_a] and b_paddle.x - b_paddle.VELOCITY > 0:
        b_paddle.move(right=False)

    if keys[pygame.K_RIGHT] and t_paddle.x + t_paddle.VELOCITY + t_paddle.width  <= WIDTH:
        t_paddle.move(right=True)
    if keys[pygame.K_LEFT] and t_paddle.x - t_paddle.VELOCITY > 0:
        t_paddle.move(right=False)


def concert_keys(keys):
    results = {}
    if keys[pygame.K_d]:
        results["bottom"] = Action.MOVETORIGHT
    if keys[pygame.K_a]:
        results["bottom"] = Action.MOVETOLEFT

    if keys[pygame.K_RIGHT]:
        results["top"] = Action.MOVETORIGHT
    if keys[pygame.K_LEFT]:
        results["top"] = Action.MOVETOLEFT

    return results


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

    while run:
        clock.tick(FPS)
        draw(WIN, [b_paddle, t_paddle], ball, game.scores)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        keys = pygame.key.get_pressed()
        
        # handel_paddel_movement(keys, b_paddle, t_paddle)
        game_keys = concert_keys(keys)
        game.handel_paddel_movement(game_keys)
        ball.move()
        game.handel_collision()
        game.check_scores()


if __name__ == "__main__":
    main()