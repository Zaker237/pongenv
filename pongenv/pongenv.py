
import numpy as np
from gym import Env, spaces
from gym.envs.classic_control import rendering
from gym.utils import seeding
import click
import time

import ponggame
from pongenv.utils import (
    Action,
    NUM_ACTIONS,
    PongEnvException,
    PongNumPlayersException
)


class PongEnv(Env):
    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self, num_players: int, make_agents_cb=None, reward_fn='max') -> None:
        if num_players < 1 or num_players > 2:
            raise PongNumPlayersException('num_players should be 1 or 2')

        self.num_players = num_players

        if make_agents_cb is not None:
            agents = make_agents_cb(self)
            if len(agents) != num_players:
                raise ValueError('Must have same number of agents as players.')
            self.agents = agents

        if reward_fn == 'max':
            self.reward_fn = lambda sr, done: (sr - 184) / 184 if done else 0
        elif reward_fn == 'step':
            self.reward_fn = lambda sr, done: sr
        elif reward_fn == 'win':
            self.reward_fn = lambda sr, done: (1 if sr == self.get_scores().max() else -1) if done else 0
        elif reward_fn == 'winmax':
            def winmax_rew(sr, done):
                if done:
                    scores = self.get_scores()
                    if sr == scores.max():
                        best_two = scores[(-scores).argsort()[:2]]
                        return best_two[0] - best_two[1]
                    else:
                        return scores[0] - scores.max()
                return 0
            self.reward_fn = winmax_rew
        else:
            self.reward_fn = reward_fn

        self.seed()
        self.viewer = None
        self.last_reward = 0
        self.action_space = spaces.Discrete(NUM_ACTIONS)  # see utils for list of all actions