"""
Hold all the cells in the maze in a 2-dimensional grid as a list of lists
"""
from graphics import Window
from cell import Cell
import time
import random

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
            ) -> None:

        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells: list[list[Cell]] = []

        if seed:
            self.__seed = random.seed(seed)
        
        self.__create_cells()
        self.__break_entrance_and_exit()
        self.__break_walls_r(0, 0)

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

        if self.__win is None:
            return

        self.__win.redraw()
        time.sleep(0.05)

    def __break_entrance_and_exit(self) -> None:

        first_cell = self.__cells[0][0]
        first_cell.has_top_wall = False
        self.__draw_cell(0,0)

        last_cell = self.__cells[self.__num_cols - 1][self.__num_rows - 1]
        last_cell.has_bottom_wall = False
        self.__draw_cell(self.__num_cols - 1, self.__num_rows - 1)

    def __break_walls_r(self, i: int, j: int) -> None:
        self.__cells[i][j].visited = True

        while True:
            next_index_list = []

            # left
            if i > 0 and not self.__cells[i - 1][j].visited:
                next_index_list.append((i - 1, j))
            # right
            if i < self.__num_cols - 1 and not self.__cells[i + 1][j].visited:
                next_index_list.append((i + 1, j))
            # up
            if j > 0 and not self.__cells[i][j - 1].visited:
                next_index_list.append((i, j - 1))
            # down
            if j < self.__num_rows - 1 and not self.__cells[i][j + 1].visited:
                next_index_list.append((i, j + 1))

            if len(next_index_list) == 0:
                self.__draw_cell(i, j)
                return

            direction_index = random.randrange(len(next_index_list))
            next_index = next_index_list[direction_index]

            # Knocking down the walls between the current cell and the next_index one           
            # right
            if next_index[0] == i + 1:
                self.__cells[i][j].has_right_wall = False
                self.__cells[i + 1][j].has_left_wall = False
            # left
            if next_index[0] == i - 1:
                self.__cells[i][j].has_left_wall = False
                self.__cells[i - 1][j].has_right_wall = False
            # down
            if next_index[1] == j + 1:
                self.__cells[i][j].has_bottom_wall = False
                self.__cells[i][j + 1].has_top_wall = False
            # up
            if next_index[1] == j - 1:
                self.__cells[i][j].has_top_wall = False
                self.__cells[i][j - 1].has_bottom_wall = False

            self.__break_walls_r(next_index[0], next_index[1])