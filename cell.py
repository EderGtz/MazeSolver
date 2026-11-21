from graphics import Window, Line, Point

class Cell:
    def __init__(self, window: Window | None = None):
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True
        self.__x1 = -1.0
        self.__x2 = -1.0
        self.__y1 = -1.0
        self.__y2 = -1.0
        self.__win = window

    def draw(self, x1: float, y1: float, x2: float, y2: float) -> None:
        self.__x1 = x1
        self.__x2 = x2
        self.__y1 = y1
        self.__y2 = y2

        if self.__win is None:
            return

        if self.has_left_wall:
            line = Line(Point(x1, y1), Point(x1, y2))
            self.__win.draw_line(line=line)

        if self.has_right_wall:
            line = Line(Point(x2, y1), Point(x2, y2))
            self.__win.draw_line(line=line)
        
        if self.has_top_wall:
            line = Line(Point(x1, y1), Point(x2, y1))
            self.__win.draw_line(line=line)

        if self.has_bottom_wall:
            line = Line(Point(x1, y2), Point(x2, y2))
            self.__win.draw_line(line=line)

    def draw_move(self, to_cell: Cell, undo: bool = False) -> None:
        """
        The path through the maze will be red, 
        if backtrack is needed it will be gray
        """
        line_color = "gray"

        if not undo:
            line_color = "red"

        if self.__win is None:
            return

        self_center = Point(
            (self.__x1 + self.__x2) / 2,
            (self.__y1 + self.__y2) / 2,
        )

        to_cell_center = Point(
            (to_cell.__x1 + to_cell.__x2) / 2,
            (to_cell.__y1 + to_cell.__y2) / 2,
        )

        line = Line(self_center, to_cell_center)
        self.__win.draw_line(line, line_color)   