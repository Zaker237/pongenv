import numpy as np
# from typing import Dict, List, Tuple
from pongenv.utils import Action, NUM_ACTIONS
from pongenv.exceptions import PongNumPlayersException, PongEnvException



class PongGame(object):
    def __init__(
        self,
        num_players: int,
        rng: np.random.RandomState,
        max_score: int = 10
    ) -> None:
        if num_players < 1 or num_players > 2:
            raise PongNumPlayersException('num_players should be 1 or 2')

        self.finished = False

        self.num_players = num_players

        self.active_player = rng.choice(num_players)

    def sample_action(self, player: int) -> Action:
        actions = np.array(Action)[self.get_possible_actions()[player]]

        return self.rng.choice(actions)
    
    def get_possible_actions(self) -> np.ndarray:
        actions = np.zeros((self.num_players, NUM_ACTIONS), bool)  # for every player which action is possible

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