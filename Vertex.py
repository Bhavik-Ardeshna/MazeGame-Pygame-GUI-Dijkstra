from utils.Colour import Colour
from utils.State import State


class Vertex:
    def __init__(self, row: int, column: int, width: int):
        self.row: int = row
        self.column: int = column
        self.x: int = column * width
        self.y: int = row * width
        self.width: int = width

        self.colour: Colour = Colour.WHITE
        self.state: State = State.EMPTY

    def set_start(self):
        self.colour = Colour.ORANGE
        self.state = State.START

    def set_end(self):
        self.colour = Colour.BLUE
        self.state = State.END

    def set_barrier(self):
        self.colour = Colour.BLACK
        self.state = State.BARRIER

    def set_path(self):
        self.colour = Colour.PURPLE
        self.state = State.PATH

    def set_open(self):
        self.colour = Colour.RED
        self.state = State.OPEN

    def set_closed(self):
        self.colour = Colour.YELLOW
        self.state = State.CLOSED

    def reset(self):
        self.colour = Colour.WHITE
        self.state = State.EMPTY

    def get_neighbors(self, graph, dist: int = 1) -> dict:

        neighbors: dict = {}
        if self.row - dist >= 0:
            neighbors["upper"] = graph.grid[self.row - dist][self.column]
        if self.row + dist < graph.rows:
            neighbors["lower"] = graph.grid[self.row + dist][self.column]
        if self.column - dist >= 0:
            neighbors["left"] = graph.grid[self.row][self.column - dist]
        if self.column + dist < graph.columns:
            neighbors["right"] = graph.grid[self.row][self.column + dist]

        return neighbors

    def get_position(self) -> tuple:
        """Returns the row and column the vertex is in"""
        return (self.row, self.column)

    def __str__(self):
        return str(self.get_position())
