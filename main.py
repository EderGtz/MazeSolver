from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width: int, height: int) -> None:
        self.__rootWidget = Tk()
        self.__rootWidget.title("Maze solver")
        self.canvas = Canvas(self.__rootWidget,width=width, height=height)
        self.canvas.pack(fill=BOTH, expand=True)
        self.__running = False
        self.__rootWidget.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__rootWidget.update_idletasks()
        self.__rootWidget.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running:
            self.redraw()
        print("Window is closed")

    def close(self):
        self.__running = False

    def draw_line(self, line: Line, fill_color: str = "black"):
        line.draw(self.canvas, fill_color=fill_color)

class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

class Line:
    def __init__(self, a_point: Point, b_point: Point) -> None:
        self.a_point = a_point
        self.b_point = b_point

    def draw(self, canvas: Canvas, fill_color: str = "black"):
        canvas.create_line(
            self.a_point.x, 
            self.a_point.y, 
            self.b_point.x, 
            self.b_point.y, 
            fill=fill_color, 
            width=2
            )

class Cell:
    def __init__(self, window: Window):
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

def main() -> None:
    win = Window(800, 600)

    c1 = Cell(win)
    c1.has_right_wall = False
    c1.draw(50, 50, 100, 100)

    c2 = Cell(win)
    c2.has_left_wall = False
    c2.has_bottom_wall = False
    c2.draw(100, 50, 150, 100)

    c1.draw_move(c2)

    c3 = Cell(win)
    c3.has_top_wall = False
    c3.has_right_wall = False
    c3.draw(100, 100, 150, 150)

    c2.draw_move(c3)

    c4 = Cell(win)
    c4.has_left_wall = False
    c4.draw(150, 100, 200, 150)

    c3.draw_move(c4, True)

    win.wait_for_close()

if __name__  == "__main__":
    main()