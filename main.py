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

    def draw_line(self, line: Line, fill_color: str):
        line.draw(self.canvas, fill_color=fill_color)

class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

class Line:
    def __init__(self, a_point: Point, b_point: Point) -> None:
        self.a_point = a_point
        self.b_point = b_point

    def draw(self, canvas: Canvas, fill_color: str):
        canvas.create_line(
            self.a_point.x, 
            self.a_point.y, 
            self.b_point.x, 
            self.b_point.y, 
            fill=fill_color, 
            width=2
            )

def main():
    win = Window(800, 600)

    lines = [
        Line(Point(50, 100), Point(50, 200)),
        Line(Point(50, 100), Point(100, 100)),
        Line(Point(50, 150), Point(90, 150)),
        Line(Point(50, 200), Point(100, 200)),

        Line(Point(130, 100), Point(130, 200)),
        Line(Point(130, 100), Point(180, 130)),
        Line(Point(180, 130), Point(180, 170)),
        Line(Point(180, 170), Point(130, 200)),

        Line(Point(210, 100), Point(210, 200)),
        Line(Point(210, 100), Point(260, 100)),
        Line(Point(210, 150), Point(250, 150)),
        Line(Point(210, 200), Point(260, 200)),

        Line(Point(290, 100), Point(290, 200)),
        Line(Point(290, 100), Point(340, 100)),
        Line(Point(340, 100), Point(340, 150)),
        Line(Point(340, 150), Point(290, 150)),
        Line(Point(290, 150), Point(340, 200)),
    ]

    for line in lines:
        win.draw_line(line, "black")

    win.wait_for_close()

if __name__  == "__main__":
    main()