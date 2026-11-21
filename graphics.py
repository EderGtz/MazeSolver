from tkinter import (
    Tk,
    BOTH,
    X,
    LEFT,
    Canvas,
    Frame,
    Label,
    Spinbox,
    Scale,
    Entry,
    Checkbutton,
    Button,
    BooleanVar,
    DoubleVar,
    IntVar,
    StringVar,
    TclError,
)
import time


class Window:
    def __init__(self, width: int, height: int) -> None:
        self.__rootWidget = Tk()
        self.__rootWidget.title("Maze solver")
        self.__running = False
        self.__is_closed = False
        self.__new_maze_requested = False

        self.__rows_var = IntVar(value=12)
        self.__cols_var = IntVar(value=16)
        self.__speed_var = DoubleVar(value=0.03)
        self.__seed_var = StringVar(value="")
        self.__auto_var = BooleanVar(value=True)

        controls = Frame(self.__rootWidget)
        controls.pack(fill=X)

        Label(controls, text="Rows:").pack(side=LEFT, padx=(8, 2))
        Spinbox(
            controls,
            from_=1,
            to=60,
            width=4,
            textvariable=self.__rows_var,
        ).pack(side=LEFT)

        Label(controls, text="Cols:").pack(side=LEFT, padx=(8, 2))
        Spinbox(
            controls,
            from_=1,
            to=60,
            width=4,
            textvariable=self.__cols_var,
        ).pack(side=LEFT)

        Label(controls, text="Speed (s):").pack(side=LEFT, padx=(8, 2))
        Scale(
            controls,
            from_=0.0,
            to=0.2,
            resolution=0.005,
            orient="horizontal",
            length=110,
            variable=self.__speed_var,
        ).pack(side=LEFT)

        Label(controls, text="Seed:").pack(side=LEFT, padx=(8, 2))
        Entry(
            controls,
            width=8,
            textvariable=self.__seed_var,
        ).pack(side=LEFT)

        Checkbutton(
            controls,
            text="Auto next",
            variable=self.__auto_var,
        ).pack(side=LEFT, padx=(8, 2))

        Button(
            controls,
            text="New maze",
            command=self.request_new_maze,
        ).pack(side=LEFT, padx=(8, 4))

        self.canvas = Canvas(self.__rootWidget, width=width, height=height)
        self.canvas.pack(fill=BOTH, expand=True)
        self.__rootWidget.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.__rootWidget.update_idletasks()
        self.__rootWidget.update()

    def wait_for_close(self):
        self.__running = True
        while self.__running and not self.__is_closed:
            self.redraw()
        print("Window is closed")

    def wait_for_input(self):
        while (
            not self.__is_closed
            and not self.__new_maze_requested
            and not self.auto_next()
        ):
            self.redraw()
            time.sleep(0.02)

    def close(self):
        self.__is_closed = True
        self.__running = False

    def is_closed(self) -> bool:
        return self.__is_closed

    def clear(self):
        self.canvas.delete("all")

    def request_new_maze(self) -> None:
        self.__new_maze_requested = True

    def new_maze_requested(self) -> bool:
        return self.__new_maze_requested

    def clear_new_maze_request(self) -> None:
        self.__new_maze_requested = False

    def auto_next(self) -> bool:
        return bool(self.__auto_var.get())

    def get_speed(self) -> float:
        try:
            delay = float(self.__speed_var.get())
        except (ValueError, TclError):
            return 0.03
        return max(0.0, min(delay, 1.0))

    def get_maze_settings(self) -> tuple[int, int, str | None]:
        rows = self.__get_int(self.__rows_var, 12, 1, 60)
        cols = self.__get_int(self.__cols_var, 16, 1, 60)
        seed = self.__seed_var.get().strip() or None
        return rows, cols, seed

    @staticmethod
    def __get_int(var: IntVar, default: int, minimum: int, maximum: int) -> int:
        try:
            value = int(var.get())
        except (ValueError, TclError):
            return default
        return max(minimum, min(value, maximum))

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
            width=2,
        )
