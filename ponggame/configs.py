import pygame
from typing import Tuple
from ponggame.ball import Ball
from ponggame.paddle import Paddle


# Const
WIDTH = 700
HEIGHT =  500
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PADDLE_WIDTH = 200
PADDLE_HEIGHT = 20
BALL_RADUIS = 7
WINNING_SCORE = 5
START_TIME = 0
TIME_ROUND = 1

# typing
BALL_STATE = Tuple[int, int, float, int, int]
PADDLE_STATE = Tuple[int, int, int, int]
