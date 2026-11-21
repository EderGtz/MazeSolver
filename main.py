from graphics import Window
from maze import Maze, MazeInterrupted

def main():
    margin = 50
    screen_x = 800
    screen_y = 600

    win = Window(screen_x, screen_y)

    while not win.is_closed():
        if not win.auto_next() and not win.new_maze_requested():
            win.wait_for_input()
            continue

        win.clear_new_maze_request()
        num_rows, num_cols, seed = win.get_maze_settings()
        generation_algorithm = win.get_generation_algorithm()
        solving_algorithm = win.get_solving_algorithm()
        cell_size_x = (screen_x - 2 * margin) / num_cols
        cell_size_y = (screen_y - 2 * margin) / num_rows

        win.clear()
        try:
            maze = Maze(
                margin,
                margin,
                num_rows,
                num_cols,
                cell_size_x,
                cell_size_y,
                win,
                seed,
                generation_algorithm,
            )
            is_solvable = maze.solve(solving_algorithm)
        except MazeInterrupted:
            continue

        if not is_solvable:
            print("maze can not be solved!")
        else:
            print("maze solved!")

if __name__ == "__main__":
    main()
