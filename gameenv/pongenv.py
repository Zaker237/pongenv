
import numpy as np
from gym import Env, spaces
from gym.envs.classic_control import rendering
from gym.utils import seeding
import click
import time

from ponggame import PongGame
from gameenv.utils import Action, NUM_ACTIONS
from gameenv.exceptions import PongEnvException, PongNumPlayersException

# The agent interacting with the environment is player 0
AGENT_PLAYER = 0


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

    def set_agents(self, agents):
        if len(agents) != self.num_players:
            raise ValueError("Must have same number of agents as players")
        self.agents = agents

    def seed(self, seed=None):
        self.rng, seed = seeding.np_random(seed)
        self.game = PongGame(self.num_players, self.rng)
        return [seed]

    def get_observation_space(self, agent=0):
        pass

    def get_score(self):
        """ Return the score of the the active Player. """
        return self.game.get_scores()[AGENT_PLAYER]

    def get_scores(self):
        """ Return le Scores of all Players """
        return self.game.get_scores()

    def sample_action(self):
        """ Return a random action """
        return self.game.sample_action(AGENT_PLAYER)

    def valid_actions(self, player=AGENT_PLAYER):
        """ Return all possibles actions based on the current state """
        return self.game.get_possible_actions()[player]

    def step(self, action: int):
        game = self.game
        valid = True
        chosen_actions = [action]
        for agent_id, agent in enumerate(self.agents[1:], 1):
            mask = None
            # respect masking
            if getattr(agent, "action_mask_fn", None) is not None:
                mask = self.valid_actions(agent_id)
            action, _ = agent.predict(self.get_observation_space(agent_id), action_masks=mask)
            chosen_actions.append(action)

        try:
            actions = np.zeros((self.num_players, NUM_ACTIONS), bool)
            actions.put(np.array(chosen_actions) + np.arange(self.num_players * NUM_ACTIONS, step=NUM_ACTIONS), True)
            step_reward = game.take_actions(actions)[AGENT_PLAYER]
            # self.last_reward = step_reward
            done = self.game.finished
            reward = self.reward_fn(step_reward, done)
        except PongEnvException:
            reward = -100
            valid = False
            done = True
            # done = self.game.finished

        translated_actions = [Action(action).name for action in chosen_actions]
        info = {'valid': valid, 'actions': translated_actions, 'scores': game.get_scores()}
        return self.get_observation_space(), reward, done, info

    def reset(self):
        self.game = PongGame(self.num_players, self.rng)
        self.last_reward = 0
        return self.get_observation_space()

    def finished(self):
        return self.game.finished