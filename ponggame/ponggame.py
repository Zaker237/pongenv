import numpy as np
import time
from typing import Tuple
from pongenv.utils import Action, NUM_ACTIONS
from pongenv.exceptions import PongNumPlayersException, PongEnvException
from ponggame.paddle import Paddle
from ponggame.ball import Ball


class PongGame(object):
    """The PongGame object implement a pong game when 2 players
    are playing again each other.

    :param num_players: The number of players, it will help when the game will
                        have a computer player.
    :param win_score: The max scrore to teach, the first player to react it has win.
    :param game_width: The width of the game's windows.
    :param game_height: The height of the game's windows.
    :param paddle_width: The width of each paddle in the game.
    :param paddle_height: The height of each paddle in the game.
    :param ball_raduis: The raduis of the ball.
    """
    def __init__(
        self,
        rng: np.random.RandomState,
        num_players: int,
        win_score: int = 10,
        game_width: int = 700,
        game_height: int = 100,
        paddle_width: int = 100,
        paddle_height: int = 20,
        ball_raduis: float = 0.5
    ) -> None:
        # check the number of player
        if num_players < 1 or num_players > 2:
            raise PongNumPlayersException('num_players should be 1 or 2')

        #TODO: check paddel and ball dimension
        if paddle_height > game_height or paddle_width > game_width:
            raise ValueError(
                "The Paddle dimmensions can't be higher than game the dimention"
            )

        if game_width - paddle_width < 200:
            raise ValueError("the paddle is too large for the game dimensions.")

        if paddle_height > 150:
            raise ValueError("Too height paddle.")

        self.win_score = win_score
        self.finished = False
        self.num_players = num_players
        self.active_player = rng.choice(num_players)
        self.game_width = game_width
        self.game_height = game_height
        self.paddle_width = paddle_width
        self.paddle_height = paddle_height
        self.ball_raduis = ball_raduis

        # game start time
        self.start_time = time.time()
        self.init_game()

    def init_game(self) ->None:
        self.top_paddle = Paddle(
            self.game_width//2 - self.paddle_width//2,
            self.game_height - 10 - self.paddle_height,
            self.paddle_width,
            self.paddle_height
        )
        self.bottom_paddle = Paddle(
            self.game_width//2 - self.paddle_width//2,
            10,
            self.paddle_width,
            self.paddle_height
        )
        self.ball = Ball(
            self.game_width // 2,
            self.game_height // 2,
            self.ball_raduis
        )

    def sample_action(self, player: int) -> Action:
        actions = np.array(Action)[self.get_possible_actions()[player]]

        return self.rng.choice(actions)
    
    def get_possible_actions(self) -> np.ndarray:
        # for every player which action is possible
        actions = np.zeros((self.num_players, NUM_ACTIONS), bool)

        return actions

    def get_scores(self) -> np.ndarray:
        scores = np.zeros((self.num_players, 1), dtype=np.int16)

        return scores.sum(1)

    def take_actions(self, actions: np.ndarray) -> int:
        active_player = self.active_payer
        possible_actions = self.get_possible_actions()
        if not possible_actions[actions].all():
            raise PongEnvException("Invalid Action chosed")
        if not actions.any(1).all():
            raise PongEnvException("Not all Agent chosed an action!")
        if actions.sum() != self.num_players:
            raise PongEnvException("An Agent chosed mor than one action!")

    # Games methods

    def handel_collision(self):
        # when the ball hits the right wall
        if self.ball.x + self.ball.raduis >= self.game_width:
            self.ball.y_velocity *= -1
        # when the ball hits the right wall
        elif self.ball.x - self.ball.raduis <= 0:
            self.ball.y_velocity *= -1

        if self.ball.y_velocity < 0:
            if self.ball.x >= self.bottom_paddle.x and \
                self.ball.x <= self.bottom_paddle.x * self.bottom_paddle.width:
                if self.ball.y - self.ball.raduis <= self.bottom_paddle.y + self.bottom_paddle.height:
                    self.ball.y_velocity *= -1

                    middle_x = self.bottom_paddle.x + self.bottom_paddle.height / 2
                    difference_in_x = middle_x - self.ball.x
                    reduction_factor = (self.bottom_paddle.width / 2) / self.ball.MAX_VELOCITY
                    x_vel = difference_in_x / reduction_factor
                    self.ball.x_velocity = -1 * x_vel
        else:
            if self.ball.x >= self.top_paddle.x and self.ball.x <= self.top_paddle.x * self.top_paddle.width:
                if self.ball.y + self.ball.raduis >= self.top_paddle.y:
                    self.ball.y_velocity *= -1

                    middle_x = self.top_paddle.x + self.top_paddle.width / 2
                    difference_in_x = middle_x - self.ball.x
                    reduction_factor = (self.top_paddle.width / 2) / self.ball.MAX_VELOCITY
                    x_vel = difference_in_x / reduction_factor
                    self.ball.x_velocity = -1 * x_vel

    def handle_time(self):
        # current duration
        current_game_duration = time.time() - self.start_time
        factor = (current_game_duration - (current_game_duration % 100)) / 100
        self.ball.update_velocity(factor)
