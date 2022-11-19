from enum import IntEnum


class Action(IntEnum):
    STAY = 0  # NOOP
    MOVETOLEFT = 1
    MOVETORIGHT = 2


NUM_ACTIONS = len(Action)