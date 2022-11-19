
from gameenv.utils import Action

import numpy as np
from typing import Tuple
from gym.utils import seeding


class HumanAgent:
    def predict(self, *args) -> int:
        raise RuntimeError("Expected a human to make the decision")


class RandomAgent:
    def __init__(self, env, player: int, seed: int = None):
        self.env = env
        self.player = player

        if seed is not None:
            self.seed(seed)

    def predict(self, *args, **kwargs) -> Tuple[int, None]:
        actions = np.array(Action)[self.env.game.get_possible_actions()[self.player]]

        return (self.env.game.rng.choice(actions), None)

    @property
    def np_random(self):
        if not hasattr(self, "_np_random"):
            self.seed()

        return self._np_random

    def seed(self, seed=None):
        self._np_random, seed = seeding.np_random(seed)
        return [seed]