import unittest

from tictactoe import game

EMPTY_RENDER = (
    " 1 | 2 | 3\n"
    "---+---+---\n"
    " 4 | 5 | 6\n"
    "---+---+---\n"
    " 7 | 8 | 9"
)

LINES = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
]


def board_from(cells):
    """Build a board from a 9-char string, '.' for empty."""
    return [" " if c == "." else c for c in cells]


class TestRender(unittest.TestCase):
    def test_ac_1_1_empty_board_shows_cell_numbers(self):
        self.assertEqual(game.render(game.new_board()), EMPTY_RENDER)

    def test_ac_1_1_occupied_cells_show_marks(self):
        board = board_from("X...O...X")
        self.assertEqual(
            game.render(board),
            " X | 2 | 3\n"
            "---+---+---\n"
            " 4 | O | 6\n"
            "---+---+---\n"
            " 7 | 8 | X",
        )


class TestParseCell(unittest.TestCase):
    def test_ac_2_3_valid_digits_map_to_indexes(self):
        for n in range(1, 10):
            with self.subTest(n=n):
                self.assertEqual(game.parse_cell(str(n)), n - 1)

    def test_ac_2_3_whitespace_is_trimmed(self):
        self.assertEqual(game.parse_cell(" 5 "), 4)
        self.assertEqual(game.parse_cell("\t7\n"), 6)

    def test_ac_3_1_invalid_input_rejected(self):
        for text in ["", "   ", "0", "05", "+5", "5.0", "10", "a", "q", "٥", "-1"]:
            with self.subTest(text=text):
                with self.assertRaises(ValueError):
                    game.parse_cell(text)


class TestApplyMove(unittest.TestCase):
    def test_ac_2_1_places_mark(self):
        board = game.apply_move(game.new_board(), 4, "X")
        self.assertEqual(board[4], "X")
        self.assertEqual(board.count(" "), 8)

    def test_ac_3_2_occupied_cell_rejected(self):
        board = board_from("....X....")
        with self.assertRaises(game.CellTaken):
            game.apply_move(board, 4, "O")

    def test_ac_3_2_cell_taken_is_value_error(self):
        self.assertTrue(issubclass(game.CellTaken, ValueError))

    def test_ac_3_3_board_unchanged_on_rejection(self):
        board = board_from("....X....")
        before = list(board)
        with self.assertRaises(game.CellTaken):
            game.apply_move(board, 4, "O")
        self.assertEqual(board, before)

    def test_ac_3_3_valid_move_does_not_mutate_input(self):
        board = game.new_board()
        game.apply_move(board, 0, "X")
        self.assertEqual(board, game.new_board())


class TestOutcome(unittest.TestCase):
    def test_in_progress_is_none(self):
        self.assertIsNone(game.outcome(game.new_board()))
        self.assertIsNone(game.outcome(board_from("XO.......")))

    def test_ac_4_1_every_line_wins(self):
        for mark in ("X", "O"):
            for line in LINES:
                with self.subTest(mark=mark, line=line):
                    board = game.new_board()
                    for i in line:
                        board[i] = mark
                    self.assertEqual(game.outcome(board), mark)

    def test_ac_4_2_full_board_without_line_is_draw(self):
        self.assertEqual(game.outcome(board_from("XOXXOOOXX")), "draw")

    def test_ac_4_3_win_on_ninth_move_beats_draw(self):
        # Full board where X completes the top row.
        self.assertEqual(game.outcome(board_from("XXXOOXXOO")), "X")


class TestOther(unittest.TestCase):
    def test_other_switches_player(self):
        self.assertEqual(game.other("X"), "O")
        self.assertEqual(game.other("O"), "X")


if __name__ == "__main__":
    unittest.main()
