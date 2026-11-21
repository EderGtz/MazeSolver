import unittest
from maze import Maze, MazeInterrupted

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
        )

    def test_maze_create_cells_different_dimensions(self):
        num_cols = 5
        num_rows = 8
        m1 = Maze(0, 0, num_rows, num_cols, 20, 15)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
        )

    def test_maze_create_cells_single_cell(self):
        num_cols = 1
        num_rows = 1
        m1 = Maze(0, 0, num_rows, num_cols, 50, 50)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
        )

    def test_maze_create_cells_wide(self):
        num_cols = 20
        num_rows = 3
        m1 = Maze(0, 0, num_rows, num_cols, 10, 30)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
        )

    def test_maze_break_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            getattr(m1, "_Maze__cells")[0][0].has_top_wall,
            False,
        )
        self.assertEqual(
            getattr(m1, "_Maze__cells")[num_cols - 1][num_rows - 1].has_bottom_wall,
            False,
    )

    def test_maze_reset_cells_visited(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)

        # The maze generator visits every cell, so they should all be reset.
        for i in range(num_cols):
            for j in range(num_rows):
                self.assertEqual(
                    m1._Maze__cells[i][j].visited,
                    False,
                )

    def test_maze_bfs_generation(self):
        num_cols = 6
        num_rows = 5
        m1 = Maze(
            0,
            0,
            num_rows,
            num_cols,
            10,
            10,
            generation_algorithm="bfs",
        )

        for i in range(num_cols):
            for j in range(num_rows):
                self.assertEqual(
                    m1._Maze__cells[i][j].visited,
                    False,
                )

        reachable = self._reachable_cells(m1, num_cols, num_rows)
        self.assertEqual(
            len(reachable),
            num_cols * num_rows,
        )

    def test_maze_solve_with_all_algorithm_combinations(self):
        num_cols = 8
        num_rows = 6

        for generation_algorithm in ("dfs", "bfs"):
            for solving_algorithm in ("dfs", "bfs"):
                with self.subTest(
                    generation=generation_algorithm,
                    solving=solving_algorithm,
                ):
                    m1 = Maze(
                        0,
                        0,
                        num_rows,
                        num_cols,
                        10,
                        10,
                        seed=123,
                        generation_algorithm=generation_algorithm,
                    )
                    self.assertTrue(m1.solve(solving_algorithm))

    def test_new_maze_request_interrupts_current_maze(self):
        class FakeWindow:
            def __init__(self):
                self.calls = 0
                self.requested = False
                self.closed = False

            def draw_line(self, line, fill_color="black"):
                pass

            def redraw(self):
                self.calls += 1
                if self.calls >= 5:
                    self.requested = True

            def is_closed(self):
                return self.closed

            def new_maze_requested(self):
                return self.requested

            def get_speed(self):
                return 0

        win = FakeWindow()

        with self.assertRaises(MazeInterrupted):
            Maze(0, 0, 10, 12, 10, 10, win)

    def _reachable_cells(self, maze, num_cols, num_rows):
        start = (0, 0)
        seen = {start}
        stack = [start]

        while stack:
            i, j = stack.pop()
            cell = maze._Maze__cells[i][j]
            neighbors = []

            if i > 0 and not cell.has_left_wall:
                neighbors.append((i - 1, j))
            if i < num_cols - 1 and not cell.has_right_wall:
                neighbors.append((i + 1, j))
            if j > 0 and not cell.has_top_wall:
                neighbors.append((i, j - 1))
            if j < num_rows - 1 and not cell.has_bottom_wall:
                neighbors.append((i, j + 1))

            for neighbor in neighbors:
                if neighbor not in seen:
                    seen.add(neighbor)
                    stack.append(neighbor)

        return seen

if __name__ == "__main__":
    unittest.main()