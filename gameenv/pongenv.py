import time
import numpy as np
from numpy.random import MT19937
from numpy.random import RandomState, SeedSequence
from gym import Env, spaces
from gym.envs.classic_control import rendering
from gym.utils import seeding

import ponggame
from gameenv.utils import Action, NUM_ACTIONS
from gameenv.exceptions import PongEnvException, PongNumPlayersException

# The agent interacting with the environment is player 0
AGENT_PLAYER = 0

class PongEnv(Env):
    metadata = {'render.modes': ['human', 'rgb_array']}

    def __init__(self, num_players: int, make_agents_cb=None, **kwargs) -> None:
        if num_players < 1 or num_players > 2:
            raise PongNumPlayersException('num_players should be 1 or 2')

        self.num_players = num_players

        if make_agents_cb is not None:
            agents = make_agents_cb(self)
            if len(agents) != num_players:
                raise ValueError('Must have same number of agents as players.')
            self.agents = agents

        self.seed()
        self.viewer = None
        self.last_reward = 0
        self.action_space = spaces.Discrete(NUM_ACTIONS)  # see utils for list of all actions
        self.tuple_spaces = spaces.Tuple((
            spaces.Discrete(num_players), # The active player
            spaces.Box(low=False, high=True, shape=(num_players,), dtype=bool),
            spaces.Box(low=0, high=ponggame.WIDTH, shape=(1,), dtype=np.uint8), # game width
            spaces.Box(low=0, high=ponggame.HEIGHT, shape=(1,), dtype=np.uint8), # game heigth
            # Ball
            spaces.Box(low=0, high=50, shape=(1,), dtype=np.uint8), # raduis
            spaces.Box(low=0, high=ponggame.WIDTH, shape=(1,), dtype=np.uint8), # x position
            spaces.Box(low=0, high=ponggame.HEIGHT, shape=(1,), dtype=np.uint8), # y position
            spaces.Box(low=0, high=10, shape=(1,), dtype=np.uint8), # x velocity
            spaces.Box(low=0, high=10, shape=(1,), dtype=np.uint8), # y velocity
            # Top Paddle
            spaces.Box(low=0, high=ponggame.WIDTH, shape=(1,), dtype=np.uint8), # with
            spaces.Box(low=0, high=ponggame.WIDTH, shape=(1,), dtype=np.uint8), # height
            spaces.Box(low=0, high=ponggame.HEIGHT, shape=(1,), dtype=np.uint8), # x pos
            spaces.Box(low=0, high=ponggame.WIDTH, shape=(1,), dtype=np.uint8), # x height
            # Bottom Paddle
            spaces.Box(low=0, high=ponggame.WIDTH, shape=(1,), dtype=np.uint8), # with
            spaces.Box(low=0, high=ponggame.WIDTH, shape=(1,), dtype=np.uint8), # height
            spaces.Box(low=0, high=ponggame.HEIGHT, shape=(1,), dtype=np.uint8), # x pos
            spaces.Box(low=0, high=ponggame.WIDTH, shape=(1,), dtype=np.uint8), # x height
            # Score
            spaces.Box(low=False, high=True, shape=(2,), dtype=np.int8),
        ))
        self.observation_space = spaces.flatten_space(self.tuple_spaces)

    def init_game(self, **kwargs) ->None:
        self.rng = RandomState(MT19937(SeedSequence(987654321)))
        self.bottom_paddle = ponggame.Paddle(
            ponggame.WIDTH//2 - ponggame.PADDLE_WIDTH//2,
            10,
            ponggame.PADDLE_WIDTH,
            ponggame.PADDLE_HEIGHT
        )
        self.top_paddle = ponggame.Paddle(
            ponggame.WIDTH//2 - ponggame.PADDLE_WIDTH//2,
            ponggame.HEIGHT - 10 - ponggame.PADDLE_HEIGHT,
            ponggame.PADDLE_WIDTH,
            ponggame.PADDLE_HEIGHT
        )

        self.ball = ponggame.Ball(
            ponggame.WIDTH//2,
            ponggame.HEIGHT//2,
            ponggame.BALL_RADUIS
        )

        self.game = ponggame.PongGame(
            self.ball,
            self.top_paddle,
            self.bottom_paddle,
            self.rng,
            win_score=10,
            game_height=ponggame.HEIGHT,
            game_width=ponggame.WIDTH
        )

    def set_agents(self, agents):
        if len(agents) != self.num_players:
            raise ValueError("Must have same number of agents as players")
        self.agents = agents

    def seed(self, seed=None):
        self.rng, seed = seeding.np_random(seed)
        self.game = ponggame.PongGame(self.num_players, self.rng)
        return [seed]

    def get_observation_space(self, agent=0):
        return spaces.flatten(
            self.tuple_spaces,
            (
                self.game.active_player,
                (self.game.active_player + agent) % self.num_players,
                self.game.game_width, # game width
                self.game.game_height, # game heigth
                # Ball
                self.game.ball.raduis, # raduis
                self.game.ball.x, # x position
                self.game.ball.y, # y position
                self.game.ball.x_velocity, # x velocity
                self.game.ball.y_velocity, # y velocity
                # Top Paddle
                self.game.top_paddle.width, # with
                self.game.top_paddle.height, # height
                self.game.top_paddle.x, # x pos
                self.game.top_paddle.y, # x height
                # Bottom Paddle
                self.game.bottom_paddle.width, # with
                self.game.bottom_paddle.height, # height
                self.game.bottom_paddle.x, # x pos
                self.game.bottom_paddle.y, # x height
                # Score
                self.game.scores
            )
        )

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
            step_reward = self.game.take_actions(actions)[AGENT_PLAYER]
            # self.last_reward = step_reward
            done = self.game.finished
            reward = self.reward_fn(step_reward, done)
        except PongEnvException:
            reward = -100
            valid = False
            done = True
            # done = self.game.finished

        translated_actions = [Action(action).name for action in chosen_actions]
        info = {'valid': valid, 'actions': translated_actions, 'scores': self.game.get_scores()}
        return self.get_observation_space(), reward, done, info

    def reset(self):
        self.game = ponggame.PongGame(self.num_players, self.rng)
        self.last_reward = 0
        return self.get_observation_space()

    def finished(self):
        return self.game.finished