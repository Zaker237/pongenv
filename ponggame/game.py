import numpy as np
import time
from typing import Dict
from gameenv.utils import Action, NUM_ACTIONS
from gameenv.exceptions import PongEnvException
from ponggame.paddle import Paddle
from ponggame.ball import Ball


class PongGame:
    """The PongGame object implement a pong game when 2 players
    are playing again each other.

    :param ball: is the object that represent the ball.
    :param botom_paddle: is the Paddle of the first player.
    :param top_paddle: The Paddle of the second player.
    :param win_score: The max scrore to teach, the first player to react it has win.
    :param game_width: The width of the game's windows.
    :param game_height: The height of the game's windows.
    """

    Num_PLAYERS = 2

    def __init__(
        self,
        ball: Ball,
        top_paddle: Paddle,
        botom_paddle: Paddle,
        rng: np.random.RandomState,
        win_score: int = 10,
        game_width: int = 700,
        game_height: int = 700
    ) -> None:

        #TODO: check paddel and ball dimension
        if top_paddle.height > game_height or botom_paddle.height > game_width:
            raise ValueError(
                "The Paddle dimmensions can't be higher than game the dimention"
            )

        if game_width - top_paddle.width < 200 or game_width - botom_paddle.width < 200:
            raise ValueError("the paddle is too large for the game dimensions.")

        if top_paddle.height > 150 or botom_paddle.height > 150:
            raise ValueError("Too height paddle.")

        self.win_score = win_score
        self.finished = False
        self.active_player = rng.choice(self.Num_PLAYERS)
        self.game_width = game_width
        self.game_height = game_height

        # ball and paddles
        self.ball = ball
        self.top_paddle = top_paddle
        self.bottom_paddle = botom_paddle

        # game start time
        self.start_time = time.time()

        # player score
        self.scores = np.zeros((1, 2), dtype=np.int16)

    def sample_action(self, player: int) -> Action:
        actions = np.array(Action)[self.get_possible_actions()[player]]

        return self.rng.choice(actions)
    
    def get_possible_actions(self) -> np.ndarray:
        # for every player which action is possible
        actions = np.zeros((self.num_players, NUM_ACTIONS), bool)
        # Action.STAY is always availlable for all players
        actions[:, Action.STAY] = True
        # first player actions
        if self.game_width - (self.bottom_paddle.x + self.bottom_paddle.width / 2) < 0.5:
            actions[0, Action.MOVETOLEFT] = True
        elif (self.bottom_paddle.x + self.bottom_paddle.width / 2) < 0.5:
            actions[0, Action.MOVETORIGHT] = True
        else:
            actions[0, :] = True
        # second player actions
        if self.game_width - (self.bottom_paddle.x + self.bottom_paddle.width / 2) < 0.5:
            actions[1, Action.MOVETOLEFT] = True
        elif (self.bottom_paddle.x + self.bottom_paddle.width / 2) < 0.5:
            actions[1, Action.MOVETORIGHT] = True
        else:
            actions[1, :] = True

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
        keys = {"top": Action.STAY, "bottom": Action.STAY}
        keys["top"] = possible_actions(1)
        keys["bottom"] = possible_actions(0)

        self.handel_paddel_movement(keys)

    def handel_collision(self):
        # when the ball hits the right wall
        if self.ball.x + self.ball.raduis >= self.game_width:
            self.ball.x_velocity *= -1
        # when the ball hits the right wall
        elif self.ball.x - self.ball.raduis <= 0:
            self.ball.x_velocity *= -1

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

    
    def handel_paddel_movement(self, keys: Dict[str, Action]) ->None:
        if not isinstance(keys, dict):
            raise ValueError("The list of action should be a dict")

        # player bottom
        if keys.get("bottom", Action.STAY) == Action.MOVETORIGHT and \
                self.bottom_paddle.x + self.bottom_paddle.VELOCITY + self.bottom_paddle.width <= self.game_width:
            self.bottom_paddle.move(right=True)
        if keys.get("bottom", Action.STAY) == Action.MOVETOLEFT and \
                self.bottom_paddle.x - self.bottom_paddle.VELOCITY > 0:
            self.bottom_paddle.move(right=False)

        # player top
        if keys.get("top", Action.STAY) == Action.MOVETORIGHT and \
                self.top_paddle.x + self.top_paddle.VELOCITY + self.top_paddle.width <= self.game_width:
            self.top_paddle.move(right=True)
        if keys.get("top", Action.STAY) == Action.MOVETOLEFT and \
                self.top_paddle.x - self.top_paddle.VELOCITY > 0:
            self.top_paddle.move(right=False)

    def handle_time(self):
        # current duration
        current_game_duration = time.time() - self.start_time
        factor = (current_game_duration - (current_game_duration % 100)) / 100
        self.ball.update_velocity(factor)

    def check_scores(self) ->bool:
        if self.ball.y < 0:
            self.scores += np.array([0, 1], np.int16)
        elif self.ball.y > self.game_height:
            self.scores += np.array([1, 0], dtype=np.int16)

        self.ball.reset()
        self.bottom_paddle.reset()
        self.top_paddle.reset()
        self.start_time = time.time()
