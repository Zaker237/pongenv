import numpy as np
# from typing import Dict, List, Tuple
from pongenv.utils import Action, NUM_ACTIONS
from pongenv.exceptions import PongNumPlayersException, PongEnvException



class PongGame(object):
    def __init__(
        self,
        num_players: int,
        max_score: int = 10
    ) -> None:
        if num_players < 1 or num_players > 2:
            raise PongNumPlayersException('num_players should be 1 or 2')

        self.finished = False

    def sample_action(self, player: int) -> Action:
        actions = np.array(Action)[self.get_possible_actions()[player]]

        return self.rng.choice(actions)

    def get_scores(self) -> np.ndarray:
        scores = np.zeros((self.num_players, 6), dtype=np.int16)

    def play(self):
        pass