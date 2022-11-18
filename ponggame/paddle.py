from ponggame.utils import WHITE, PADDLE_STATE


class Paddle(object):
    """The Paddle object represents the paddle used in pong game.

    :param x: The current x position of the paddle on the game board.
    :param y: The current y position of the paddle on the game board.
    :param width: The width of the paddle.
    :param height: The height of the paddle.
    """
    COLOR = WHITE
    VELOCITY = 4

    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def move(self, right: bool=True) -> None:
        if right:
            self.x -= self.VELOCITY
        else:
            self.x += self.VELOCITY

    def reset(self) ->None:
        self.x = self.original_x
        self.y = self.original_y

    def as_state(self) ->PADDLE_STATE:
        return(
            self.x,
            self.y,
            self.width,
            self.height
        )
