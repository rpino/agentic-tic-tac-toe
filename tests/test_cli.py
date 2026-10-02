import unittest

from tictactoe import cli, game


class FakeIO:
    """Scripted input_fn that records prompts, and an output_fn that collects messages."""

    def __init__(self, replies):
        self.replies = list(replies)
        self.prompts = []
        self.output = []

    def input_fn(self, prompt):
        self.prompts.append(prompt)
        reply = self.replies.pop(0)
        if isinstance(reply, BaseException):
            raise reply
        return reply

    def output_fn(self, message):
        self.output.append(message)


def prompt_for(player):
    return f"Player {player}, choose a cell (1-9) or q: "


def play(replies):
    io = FakeIO(replies)
    result = cli.play_game(io.input_fn, io.output_fn)
    return result, io


class TestPlayGame(unittest.TestCase):
    def test_ac_1_1_game_starts_with_empty_board(self):
        _, io = play(["q"])
        self.assertEqual(io.output[0], game.render(game.new_board()))

    def test_ac_1_2_x_is_prompted_first_with_exact_prompt(self):
        _, io = play(["q"])
        self.assertEqual(io.prompts, [prompt_for("X")])

    def test_ac_2_1_valid_move_places_mark_and_redisplays(self):
        _, io = play(["5", "q"])
        expected = game.apply_move(game.new_board(), 4, "X")
        self.assertEqual(io.output[1], game.render(expected))

    def test_ac_2_2_turn_passes_to_other_player(self):
        _, io = play(["5", "1", "q"])
        self.assertEqual(io.prompts, [prompt_for("X"), prompt_for("O"), prompt_for("X")])

    def test_ac_3_1_invalid_input_message_same_player(self):
        _, io = play(["abc", "", "q"])
        self.assertEqual(io.output[1:], [cli.INVALID_INPUT, cli.INVALID_INPUT])
        self.assertEqual(cli.INVALID_INPUT, "Invalid input: enter a number from 1 to 9.")
        self.assertEqual(io.prompts, [prompt_for("X")] * 3)

    def test_ac_3_2_occupied_cell_message_same_player(self):
        _, io = play(["5", "5", "q"])
        self.assertEqual(io.output[2], "Cell 5 is taken. Choose another.")
        self.assertEqual(io.prompts, [prompt_for("X"), prompt_for("O"), prompt_for("O")])

    def test_ac_3_3_rejected_move_prints_only_the_error(self):
        _, io = play(["5", "5", "q"])
        # empty board, board after X@5, error; no redraw after the rejection
        self.assertEqual(len(io.output), 3)

    def test_ac_4_1_win_shows_final_board_and_message(self):
        # X: 1, 2, 3 (top row); O: 4, 5
        result, io = play(["1", "4", "2", "5", "3"])
        self.assertEqual(result, "over")
        final = game.render(["X", "X", "X", "O", "O", " ", " ", " ", " "])
        self.assertEqual(io.output[-2:], [final, "Player X wins!"])
        self.assertEqual(len(io.prompts), 5)

    def test_ac_4_1_o_can_win(self):
        # X: 1, 2, 7; O: 4, 5, 6 (middle row)
        result, io = play(["1", "4", "2", "5", "7", "6"])
        self.assertEqual(result, "over")
        self.assertEqual(io.output[-1], "Player O wins!")

    def test_ac_4_2_draw_shows_final_board_and_message(self):
        # Final board XOX / XOO / OXX
        result, io = play(["1", "2", "3", "5", "4", "6", "8", "7", "9"])
        self.assertEqual(result, "over")
        final = game.render(list("XOXXOOOXX"))
        self.assertEqual(io.output[-2:], [final, "It's a draw!"])

    def test_ac_4_3_win_on_ninth_move_reports_win(self):
        # X: 1, 6, 7, 3, 2; O: 4, 5, 8, 9. Final board XXX / OOX / XOO;
        # no line before move 9, then X completes the top row on the ninth move.
        result, io = play(["1", "4", "6", "5", "7", "8", "3", "9", "2"])
        self.assertEqual(result, "over")
        self.assertEqual(io.output[-1], "Player X wins!")
        self.assertEqual(len(io.prompts), 9)

    def test_ac_5_1_q_quits(self):
        for reply in ["q", "Q", " q "]:
            with self.subTest(reply=reply):
                result, _ = play([reply])
                self.assertEqual(result, "quit")


X_WINS = ["1", "4", "2", "5", "3"]
PLAY_AGAIN = "Play again? (y/n): "


def run_main(replies):
    io = FakeIO(replies)
    code = cli.main(io.input_fn, io.output_fn)
    return code, io


class TestMain(unittest.TestCase):
    def test_ac_4_4_game_end_goes_to_play_again_prompt(self):
        _, io = run_main(X_WINS + ["n"])
        self.assertEqual(io.prompts[-1], PLAY_AGAIN)
        self.assertEqual(len(io.prompts), len(X_WINS) + 1)

    def test_ac_5_1_q_prints_goodbye_and_returns_0(self):
        code, io = run_main(["q"])
        self.assertEqual(code, 0)
        self.assertEqual(io.output[-1], "Goodbye.")

    def test_ac_5_2_eof_at_either_prompt(self):
        for replies in ([EOFError()], X_WINS + [EOFError()]):
            with self.subTest(at=len(replies)):
                code, io = run_main(replies)
                self.assertEqual(code, 0)
                self.assertEqual(io.output[-1], "Goodbye.")

    def test_ac_5_3_ctrl_c_at_either_prompt(self):
        for replies in ([KeyboardInterrupt()], X_WINS + [KeyboardInterrupt()]):
            with self.subTest(at=len(replies)):
                code, io = run_main(replies)
                self.assertEqual(code, 0)
                self.assertEqual(io.output[-1], "Goodbye.")

    def test_ac_6_1_exact_play_again_prompt(self):
        _, io = run_main(X_WINS + ["n"])
        self.assertEqual(io.prompts[-1], "Play again? (y/n): ")

    def test_ac_6_2_yes_starts_new_game_with_empty_board_and_x(self):
        for reply in ["y", "Y", " y "]:
            with self.subTest(reply=reply):
                _, io = run_main(X_WINS + [reply, "q"])
                self.assertEqual(io.prompts[-1], prompt_for("X"))
                self.assertEqual(io.output[-2], game.render(game.new_board()))

    def test_ac_6_3_no_prints_goodbye_and_returns_0(self):
        for reply in ["n", "N", " n "]:
            with self.subTest(reply=reply):
                code, io = run_main(X_WINS + [reply])
                self.assertEqual(code, 0)
                self.assertEqual(io.output[-1], "Goodbye.")

    def test_ac_6_4_other_input_repeats_prompt(self):
        _, io = run_main(X_WINS + ["maybe", "q", "", "n"])
        self.assertEqual(io.output[-4:-1], ["Please enter y or n."] * 3)
        self.assertEqual(io.prompts[-4:], [PLAY_AGAIN] * 4)


class TestEntryPoint(unittest.TestCase):
    """Smoke test: the real program via python -m tictactoe."""

    def run_program(self, stdin_text):
        import os
        import subprocess
        import sys

        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return subprocess.run(
            [sys.executable, "-m", "tictactoe"],
            input=stdin_text, capture_output=True, text=True, cwd=root, timeout=10,
        )

    def test_full_game_then_quit(self):
        proc = self.run_program("1\n4\n2\n5\n3\nn\n")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("Player X wins!", proc.stdout)
        self.assertIn("Goodbye.", proc.stdout)
        self.assertNotIn("Traceback", proc.stderr)

    def test_ac_5_2_eof_exits_cleanly(self):
        proc = self.run_program("")
        self.assertEqual(proc.returncode, 0)
        self.assertIn("Goodbye.", proc.stdout)
        self.assertNotIn("Traceback", proc.stderr)


if __name__ == "__main__":
    unittest.main()
