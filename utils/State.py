import enum


class State(enum.Enum):
    """
    START: Cell is the starting cell.
    END: Cell is the destination cell.
    BARRIER: Cell is a barrier.
    PATH: Cell is one of the cells of the shortest path.
    OPEN:Cell has been discovered but not yet visited.
    CLOSED: Cell has been visited.
    """

    START = 1
    END = 2
    BARRIER = 3
    PATH = 4
    OPEN = 5
    CLOSED = 6
    EMPTY = 7
