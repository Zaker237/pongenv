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


def handel_collision(ball: Ball, left_paddle: Paddle, right_paddle: Paddle):
    if ball.y + ball.raduis >= HEIGHT:
        ball.y_velocity *= -1
    elif ball.y - ball.raduis <= 0:
        ball.y_velocity *= -1

    if ball.x_velocity < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y * left_paddle.height:
            if ball.x - ball.raduis <= left_paddle.x + left_paddle.width:
                ball.x_velocity *= -1

                middle_y = left_paddle.y + left_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VELOCITY
                y_vel = difference_in_y / reduction_factor
                ball.y_velocity = -1 * y_vel
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y * right_paddle.height:
            if ball.x + ball.raduis >= right_paddle.x:
                ball.x_velocity *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VELOCITY
                y_vel = difference_in_y / reduction_factor
                ball.y_velocity = -1 * y_vel
