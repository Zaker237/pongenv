from gym.envs.registration import register

from pongenv.utils import Action, NUM_ACTIONS
from pongenv.pongenv import PongEnv
from pongenv.agents import HumanAgent, RandomAgent

register(
    id='PongEnv-Multi-v0',
    entry_point='pongenv:PongEnv',
    kwargs={'num_players': 2},
)

register(
    id='PongEnv-Solo-v0',
    entry_point='pongenv:PongEnv',
    kwargs={'num_players': 1},
)