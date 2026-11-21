"""
Hold all the cells in the maze in a 2-dimensional grid as a list of lists
"""
from graphics import Window
from cell import Cell
import time

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
            ) -> None:

        self.__x1 = x1
        self.__y1 = y1
        self.__num_rows = num_rows
        self.__num_cols = num_cols
        self.__cell_size_x = cell_size_x
        self.__cell_size_y = cell_size_y
        self.__win = win
        self.__cells: list[list[Cell]] = []
        
        self.__create_cells()
        self.__break_entrance_and_exit()

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