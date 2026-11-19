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

def main():
    win = Window(800, 600)

    c = Cell(win)
    c.has_left_wall = False
    c.draw(50, 50, 100, 100)

    c = Cell(win)
    c.has_right_wall = False
    c.draw(125, 125, 200, 200)

    c = Cell(win)
    c.has_bottom_wall = False
    c.draw(225, 225, 250, 250)

    c = Cell(win)
    c.has_top_wall = False
    c.draw(300, 300, 500, 500)

    win.wait_for_close()

if __name__  == "__main__":
    main()