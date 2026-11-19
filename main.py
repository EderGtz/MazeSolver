from tkinter import Tk, BOTH, Canvas

class Window:
    def __init__(self, width, height) -> None:
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

def main():
    window = Window(800, 600)
    window.wait_for_close()

if __name__  == "__main__":
    main()