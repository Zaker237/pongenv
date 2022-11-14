import pygame
from typing import Tuple
from ponggame.ball import Ball
from ponggame.paddle import Paddle


# Const
WIDTH = 700
HEIGHT =  500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_RADUIS = 7
SCORE_FONT = pygame.font.SysFont("comicsans", 20)
WINNING_SCORE = 5
START_TIME = 0
TIME_ROUND = 1

# typing
BALL_STATE = Tuple[int, int, float, int, int]
PADDLE_STATE = Tuple[int, int, int, int]


def handel_paddel_movement(keys, left_paddle: Paddle, right_paddle: Paddle):
    if keys[pygame.K_w] and left_paddle.y - left_paddle.VELOCITY > 0:
        left_paddle.move(up=True)
    if keys[pygame.K_s] and left_paddle.y + left_paddle.VELOCITY + left_paddle.height <= HEIGHT:
        left_paddle.move(up=False)

    if keys[pygame.K_UP] and right_paddle.y - right_paddle.VELOCITY > 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and right_paddle.y + right_paddle.VELOCITY + right_paddle.height <= HEIGHT:
        right_paddle.move(up=False)
