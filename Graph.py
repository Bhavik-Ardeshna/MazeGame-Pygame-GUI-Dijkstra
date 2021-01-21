import pygame
from utils.P_Queue import PriorityQueue
from queue import LifoQueue
import time
import math
import random
from Vertex import Vertex
from utils.State import State


class Graph:

    def __init__(self, rows: int, vertex_width: int):
        self.rows: int = rows
        self.columns: int = rows
        self.vertex_width: int = vertex_width

        self.start: Vertex = None
        self.end: Vertex = None
        self.paths: dict = {}

        self.grid: list = self.init_grid()

    def init_grid(self) -> list:
        xs: list = []
        ys: list = []

        for row in range(self.rows):
            for col in range(self.columns):
                node = Vertex(row, col, self.vertex_width)
                ys.append(node)
            xs.append(ys)
            ys = []

        return xs

    def __set_all_barriers(self):
        for rows in self.grid:
            for node in rows:
                node.set_barrier()

    def __get_discovered(self):
        nodes: list = []
        for rows in self.grid:
            for node in rows:
                if node.state in [State.OPEN, State.CLOSED, State.PATH]:
                    nodes.append(node)
        return nodes

    def set_start(self, v: Vertex):
        v.set_start()
        self.start = v

    def set_end(self, v: Vertex):
        v.set_end()
        self.end = v

    def mark_path(self, delete: bool):
        current: Vertex = self.paths[self.end]
        while current != self.start:
            if delete:
                current.set_closed()
            else:
                current.set_path()
            current = self.paths[current]

    def reset(self):
        self.start = None
        self.end = None
        self.paths = {}
        self.grid = self.init_grid()

    def reset_discovered(self):
        self.paths = {}
        for node in self.__get_discovered():
            node.reset()

    def dijkstra(self, gui) -> dict:

        # Containing pairs of vertix and distance to the starting vertix where
        # the vertix is the key and the distance the key.
        dist: dict = {}
        # Dictionary with pairs of (vertix: previous_vertix)
        prev: dict = {}
        # Containing all yet to visit nodes.
        queue: PriorityQueue = PriorityQueue()

        # Init dicts and queue
        dist[self.start] = 0
        for row in self.grid:
            for node in row:
                if node != self.start:
                    dist[node] = float('inf')
                    prev[node] = None

        # Add the starting node to the queue with the distance as metric. In case of
        # a tie the current time will be used as a tie breaker so that the least recently
        # added element wins.
        queue.put((dist[self.start], time.time(), self.start))

        while not queue.empty():
            # Get element with minimum distance from the queue.
            crrnt: Vertex = queue.get()[2]

            # Mark as visited
            if crrnt != self.start and crrnt != self.end:
                crrnt.set_closed()

            # If the end is reached the shortest path has been found
            if crrnt == self.end:
                break

            # Discover neighbors:
            for neighbor in crrnt.get_neighbors(self).values():

                # Skip nodes that either cannot be visited or already have been visited
                if neighbor.state == State.BARRIER or neighbor.state == State.CLOSED:
                    continue

                # Mark nodes as open
                if neighbor != self.end and neighbor != self.start:
                    neighbor.set_open()

                # Check whether there's a faster path by comparing known
                # to newly discovered distances
                alt_dist = dist[crrnt] + 1
                if alt_dist < dist[neighbor]:
                    dist[neighbor] = alt_dist
                    prev[neighbor] = crrnt
                    # Add newly discovered neighbor to the queue.
                    queue.put((dist[neighbor], time.time(), neighbor))

            # Redraw the grid
            gui.draw()

        self.paths = prev
