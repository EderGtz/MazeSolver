"""
Hold all the cells in the maze in a 2-dimensional grid as a list of lists
"""
from collections import deque
from graphics import Window
from cell import Cell
import time
import random


class MazeInterrupted(Exception):
    """Raised when the user requests a new maze before this one finishes."""


class Maze:

    def __init__(
            self,
            x1: int,
            y1: int,
            num_rows: int,
            num_cols: int,
            cell_size_x: float,
            cell_size_y: float,
            win: Window | None = None,
            seed: int | float | str | bytes | bytearray | None = None,
            generation_algorithm: str = "dfs",
            ) -> None:

        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells: list[list[Cell]] = []

        generation_algorithm = generation_algorithm.lower()
        if generation_algorithm not in ("dfs", "bfs"):
            raise ValueError("generation_algorithm must be 'dfs' or 'bfs'")

        if seed is not None:
            random.seed(seed)

        self.__create_cells()
        self.__break_entrance_and_exit()
        if generation_algorithm == "bfs":
            self.__break_walls_bfs()
        else:
            self.__break_walls_r(0, 0)
        self.__reset_cells_visited()

    def __create_cells(self) -> None:
        #          cols rows
        #self.__cells[0][0]

        for i in range(self.__num_cols):
            current_col = []
            for j in range(self.__num_rows):
                current_col.append(Cell(self.__win))
            self.__cells.append(current_col)

        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__draw_cell(i, j)



    def __draw_cell(self, i: int, j: int) -> None:
        "i for column, j for row"

        current_cell: Cell = self.__cells[i][j]
        current_cell_x1 = self.__x1 + (i * self.__cell_size_x)
        current_cell_y1 = self.__y1 + (j * self.__cell_size_y)
        current_cell_x2 = current_cell_x1 + self.__cell_size_x
        current_cell_y2 = current_cell_y1 + self.__cell_size_y

        current_cell.draw(
            current_cell_x1, 
            current_cell_y1, 
            current_cell_x2, 
            current_cell_y2
            )
        
        self.__animate()

    def __animate(self) -> None:

        if self.__win is None or self.__win.is_closed():
            return

        self.__win.redraw()

        if self.__win.is_closed():
            return

        if self.__win.new_maze_requested():
            raise MazeInterrupted()

        delay = self.__win.get_speed()
        if delay > 0:
            time.sleep(delay)

    def __break_entrance_and_exit(self) -> None:

        first_cell = self.__cells[0][0]
        first_cell.has_top_wall = False
        self.__draw_cell(0,0)

        last_cell = self.__cells[self.__num_cols - 1][self.__num_rows - 1]
        last_cell.has_bottom_wall = False
        self.__draw_cell(self.__num_cols - 1, self.__num_rows - 1)

    def __unvisited_neighbors(self, i: int, j: int) -> list[tuple[int, int]]:
        neighbors: list[tuple[int, int]] = []

        # left
        if i > 0 and not self.__cells[i - 1][j].visited:
            neighbors.append((i - 1, j))
        # right
        if i < self.__num_cols - 1 and not self.__cells[i + 1][j].visited:
            neighbors.append((i + 1, j))
        # up
        if j > 0 and not self.__cells[i][j - 1].visited:
            neighbors.append((i, j - 1))
        # down
        if j < self.__num_rows - 1 and not self.__cells[i][j + 1].visited:
            neighbors.append((i, j + 1))

        return neighbors

    def __open_neighbors(self, i: int, j: int) -> list[tuple[int, int]]:
        neighbors: list[tuple[int, int]] = []

        # left
        if i > 0 and not self.__cells[i][j].has_left_wall:
            neighbors.append((i - 1, j))
        # right
        if i < self.__num_cols - 1 and not self.__cells[i][j].has_right_wall:
            neighbors.append((i + 1, j))
        # up
        if j > 0 and not self.__cells[i][j].has_top_wall:
            neighbors.append((i, j - 1))
        # down
        if j < self.__num_rows - 1 and not self.__cells[i][j].has_bottom_wall:
            neighbors.append((i, j + 1))

        return neighbors

    def __remove_wall_between(
        self,
        i: int,
        j: int,
        next_i: int,
        next_j: int,
    ) -> None:
        # right
        if next_i == i + 1:
            self.__cells[i][j].has_right_wall = False
            self.__cells[next_i][next_j].has_left_wall = False
        # left
        elif next_i == i - 1:
            self.__cells[i][j].has_left_wall = False
            self.__cells[next_i][next_j].has_right_wall = False
        # down
        elif next_j == j + 1:
            self.__cells[i][j].has_bottom_wall = False
            self.__cells[next_i][next_j].has_top_wall = False
        # up
        elif next_j == j - 1:
            self.__cells[i][j].has_top_wall = False
            self.__cells[next_i][next_j].has_bottom_wall = False

    def __break_walls_r(self, i: int, j: int) -> None:
        self.__cells[i][j].visited = True

        while True:
            next_index_list = self.__unvisited_neighbors(i, j)

            if len(next_index_list) == 0:
                self.__draw_cell(i, j)
                return

            next_i, next_j = random.choice(next_index_list)
            self.__remove_wall_between(i, j, next_i, next_j)
            self.__break_walls_r(next_i, next_j)

    def __break_walls_bfs(self) -> None:
        self.__cells[0][0].visited = True
        queue: deque[tuple[int, int]] = deque([(0, 0)])

        while queue:
            i, j = queue.popleft()
            next_index_list = self.__unvisited_neighbors(i, j)
            random.shuffle(next_index_list)

            for next_i, next_j in next_index_list:
                if self.__cells[next_i][next_j].visited:
                    continue

                self.__cells[next_i][next_j].visited = True
                self.__remove_wall_between(i, j, next_i, next_j)
                queue.append((next_i, next_j))

            self.__draw_cell(i, j)

    def __reset_cells_visited(self) -> None:
        for i in range(self.__num_cols):
            for j in range(self.__num_rows):
                self.__cells[i][j].visited = False

    def solve(self, algorithm: str = "dfs") -> bool:
        algorithm = algorithm.lower()
        if algorithm not in ("dfs", "bfs"):
            raise ValueError("algorithm must be 'dfs' or 'bfs'")

        self.__reset_cells_visited()

        if algorithm == "bfs":
            return self.__solve_bfs()

        return self._solve_r(0, 0)

    def _solve_r(self, i: int, j: int) -> bool:
        self.__animate()

        current_cell = self.__cells[i][j]
        current_cell.visited = True

        if self.__cells[self.__num_cols -1][self.__num_rows -1] == current_cell:
            return True

        # For each direction, if there is no wall and cell hasnt been visited
        # left
        if (
            i > 0 
            and not self.__cells[i][j].has_left_wall 
            and not self.__cells[i - 1][j].visited
        ):
            self.__cells[i][j].draw_move(self.__cells[i - 1][j])
            if self._solve_r(i -1, j):
                return True
            else:
                self.__cells[i][j].draw_move(self.__cells[i - 1][j], undo=True)
            
        # right
        if (
            i < self.__num_cols - 1
            and not self.__cells[i][j].has_right_wall 
            and not self.__cells[i + 1][j].visited
        ):
            self.__cells[i][j].draw_move(self.__cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self.__cells[i][j].draw_move(self.__cells[i + 1][j], undo=True)
            
        # up
        if (
            j > 0 
            and not self.__cells[i][j].has_top_wall
            and not self.__cells[i][j - 1].visited
        ):
            self.__cells[i][j].draw_move(self.__cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self.__cells[i][j].draw_move(self.__cells[i][j - 1], undo=True)
        # down
        if (
            j < self.__num_rows - 1
            and not self.__cells[i][j].has_bottom_wall
            and not self.__cells[i][j + 1].visited
        ):
            self.__cells[i][j].draw_move(self.__cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self.__cells[i][j].draw_move(self.__cells[i][j + 1], True)
        
        return False

    def __solve_bfs(self) -> bool:
        start: tuple[int, int] = (0, 0)
        goal: tuple[int, int] = (
            self.__num_cols - 1,
            self.__num_rows - 1,
        )
        self.__cells[0][0].visited = True
        queue: deque[tuple[int, int]] = deque([start])
        came_from: dict[tuple[int, int], tuple[int, int] | None] = {
            start: None,
        }

        while queue:
            i, j = queue.popleft()

            if (i, j) == goal:
                break

            for next_i, next_j in self.__open_neighbors(i, j):
                if self.__cells[next_i][next_j].visited:
                    continue

                self.__cells[next_i][next_j].visited = True
                came_from[(next_i, next_j)] = (i, j)
                self.__cells[i][j].draw_move(
                    self.__cells[next_i][next_j],
                    undo=True,
                )
                self.__animate()
                queue.append((next_i, next_j))

        if goal not in came_from:
            return False

        path: list[tuple[int, int]] = []
        current: tuple[int, int] | None = goal
        while current is not None:
            path.append(current)
            current = came_from[current]
        path.reverse()

        for (i, j), (next_i, next_j) in zip(path, path[1:]):
            self.__cells[i][j].draw_move(self.__cells[next_i][next_j])
            self.__animate()

        return True
