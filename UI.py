import pygame
from utils.Colour import Colour
from utils.State import State
from Graph import Graph


class UI:

    def __init__(self, rows: int, width: int):
        self.rows: int = rows
        self.columns: int = rows
        self.width: int = width
        self.vertex_width: int = round(width / rows)
        self.graph: Graph = Graph(self.rows, self.vertex_width)
        self.win = pygame.display.set_mode((width, width))
        pygame.display.set_caption("Arvik's Maze Game (Dijkstra)")

    def draw(self):
        self.win.fill(Colour.WHITE)
        # Draw cells
        for row in self.graph.grid:
            for cell in row:
                pygame.draw.rect(
                    self.win,
                    cell.colour,
                    (cell.x, cell.y, self.vertex_width, self.vertex_width)
                )
        # self.draw_grid()

        pygame.display.update()

    def handle_events(self) -> bool:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = self.get_click_pos(pos)
                node = self.graph.grid[row][col]

                if not self.graph.start and node != self.graph.end:
                    self.graph.set_start(node)

                elif node != self.graph.end and node != self.graph.start and not self.graph.paths:
                    node.set_barrier()

            elif pygame.mouse.get_pressed()[1]:
                pos = pygame.mouse.get_pos()
                row, col = self.get_click_pos(pos)
                node = self.graph.grid[row][col]

                if node != self.graph.end and node != self.graph.start and node.state != State.BARRIER:
                    self.graph.set_end(node)
                    if self.graph.paths:
                        self.graph.mark_path(False)

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = self.get_click_pos(pos)
                node = self.graph.grid[row][col]
                if (
                    node.state == State.END or
                    (not self.graph.paths and node.state == State.BARRIER) or
                    (not self.graph.paths and node.state == State.START)
                ):
                    node.reset()
                    if node == self.graph.start:
                        self.graph.start = None
                    elif node == self.graph.end:
                        if self.graph.paths:
                            self.graph.mark_path(True)
                            node.set_closed()
                        self.graph.end = None

            elif event.type == pygame.KEYDOWN:
                # Reset with ESC
                if event.key == pygame.K_ESCAPE:
                    self.graph.reset()
                # Partly reset
                elif event.key == pygame.K_c:
                    self.graph.reset_discovered()

                # Start Dijkstra algorithm
                elif self.graph.start and event.key == pygame.K_d:
                    self.graph.dijkstra(self)
                    if self.graph.end:
                        self.graph.mark_path(False)

        return True

    def loop(self):
        while self.handle_events():
            self.draw()
        pygame.quit()

    def get_click_pos(self, pos: tuple) -> tuple:

        x, y = pos
        row = y // self.vertex_width
        col = x // self.vertex_width
        return (row, col)
