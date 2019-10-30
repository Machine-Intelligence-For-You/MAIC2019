import pickle, signal, copy
from functools import wraps
import errno
import os


class Trace:

    def __init__(self, board):
        self.initial_board = copy.deepcopy(board)
        self.winner = -1
        self.actions = []
        self.score = [0,0]

    def add_action(self, player, action, game_step, board, score,pieces_in_hands):
        self.actions.append((player, action, game_step, board, score,pieces_in_hands))

    def write(self, f):
        pickle.dump(self, open(f + ".trace", 'wb'))

    def load_trace(self, f):
        return pickle.load(open(f, 'rb'))

    def get_actions(self):
        return self.actions

    def get_last_board(self):
        if not self.actions:
            return self.initial_board
        else:
            return self.actions[-1]


class Timeout():
    """Timeout class using ALARM signal."""
    class Timeout(Exception):
        pass

    def __init__(self, sec):
        self.sec = sec

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.raise_timeout)
        signal.setitimer(signal.ITIMER_REAL, self.sec)

    def __exit__(self, *args):
        signal.alarm(0)    # disable alarm

    def raise_timeout(self, *args):
        raise Timeout.Timeout()


class TimeoutError(Exception):
    pass


def timeout(seconds=1, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.setitimer(signal.ITIMER_REAL,seconds) #used timer instead of alarm
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wraps(func)(wrapper)
    return decorator
