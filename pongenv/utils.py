# from typing import Dict, List, Tuple
from enum import IntEnum


class PongEnvException(Exception):
    pass


class PongNumPlayersException(Exception):
    pass


class Action(IntEnum):
    STAY = 0  # NOOP
    MOVETOLEFT = 1
    MOVETORIGHT = 2


NUM_ACTIONS = len(Action)