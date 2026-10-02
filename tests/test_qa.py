"""QA-phase tests (docs/06-qa/test-cases.md): exact end-to-end output, NFR checks, multi-game state."""

import ast
import os
import subprocess
import sys
import unittest

from tictactoe import cli, game

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PKG = os.path.join(ROOT, "tictactoe")
SOURCES = [os.path.join(PKG, f) for f in sorted(os.listdir(PKG)) if f.endswith(".py")]


def run_program(stdin_text):
    return subprocess.run(
        [sys.executable, "-m", "tictactoe"],
        input=stdin_text, capture_output=True, text=True, cwd=ROOT, timeout=10,
    )


class TestExactTranscript(unittest.TestCase):
    def test_tc_e2e_exact_stdout_for_x_win_then_no(self):
        """TC-24: the whole stdout of a real run, character for character."""
        moves = [(0, "X"), (3, "O"), (1, "X"), (4, "O"), (2, "X")]
        board = game.new_board()
        expected = game.render(board) + "\n"
        for idx, player in moves:
            expected += cli.MOVE_PROMPT.format(player=player)
            board = game.apply_move(board, idx, player)
            expected += game.render(board) + "\n"
        expected += "Player X wins!\n" + "Play again? (y/n): " + "Goodbye.\n"

        proc = run_program("1\n4\n2\n5\n3\nn\n")
        self.assertEqual(proc.stdout, expected)
        self.assertEqual(proc.stderr, "")
        self.assertEqual(proc.returncode, 0)


class TestMultiGame(unittest.TestCase):
    def test_tc_second_game_starts_clean_and_can_finish(self):
        """TC-25: after 'y', the second game has fresh state and can reach its own result."""
        replies = ["1", "4", "2", "5", "3", "y",   # game 1: X wins
                   "4", "1", "5", "2", "9", "3",   # game 2: O wins top row
                   "n"]
        prompts = []
        output = []

        def fake_input(prompt):
            prompts.append(prompt)
            return replies.pop(0)

        code = cli.main(fake_input, output.append)
        self.assertEqual(code, 0)
        self.assertEqual([m for m in output if m.endswith("wins!")], ["Player X wins!", "Player O wins!"])
        self.assertEqual(output[-1], "Goodbye.")


class TestGoodbyeOwnLine(unittest.TestCase):
    """AC-5.4 (from QA GAP-1): after EOF/Ctrl+C, Goodbye. is on its own line."""

    def run_main(self, replies):
        replies = list(replies)
        output = []

        def fake_input(prompt):
            reply = replies.pop(0)
            if isinstance(reply, BaseException):
                raise reply
            return reply

        code = cli.main(fake_input, output.append)
        return code, output

    def test_ac_5_4_newline_before_goodbye_on_eof_or_ctrl_c(self):
        x_wins = ["1", "4", "2", "5", "3"]
        for replies in ([EOFError()], [KeyboardInterrupt()],
                        x_wins + [EOFError()], x_wins + [KeyboardInterrupt()]):
            with self.subTest(replies=replies):
                code, output = self.run_main(replies)
                self.assertEqual(code, 0)
                self.assertEqual(output[-2:], ["", "Goodbye."])

    def test_ac_5_4_no_extra_blank_line_after_q_or_n(self):
        # The player pressed Enter, so the cursor is already on a new line.
        for replies in (["q"], ["1", "4", "2", "5", "3", "n"]):
            with self.subTest(replies=replies):
                _, output = self.run_main(replies)
                self.assertEqual(output[-1], "Goodbye.")
                self.assertNotEqual(output[-2], "")

    def test_ac_5_4_real_program_eof(self):
        proc = run_program("")
        self.assertTrue(proc.stdout.endswith(cli.MOVE_PROMPT.format(player="X") + "\nGoodbye.\n"),
                        repr(proc.stdout[-60:]))


class TestNonFunctional(unittest.TestCase):
    def imported_modules(self):
        names = set()
        for path in SOURCES:
            with open(path, encoding="utf-8") as f:
                tree = ast.parse(f.read())
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    names.update(a.name.split(".")[0] for a in node.names)
                elif isinstance(node, ast.ImportFrom):
                    names.add(node.module.split(".")[0])
        return names

    def test_tc_nfr_1_stdlib_only(self):
        """TC-26: only stdlib or own-package imports (NFR-1)."""
        third_party = {m for m in self.imported_modules()
                       if m != "tictactoe" and m not in sys.stdlib_module_names}
        self.assertEqual(third_party, set())

    def test_tc_nfr_3_no_network_file_or_os_access(self):
        """TC-27: no network/file/OS modules imported and no open() calls (NFR-3)."""
        forbidden = {"socket", "urllib", "http", "os", "subprocess", "shutil", "pathlib", "requests"}
        self.assertEqual(self.imported_modules() & forbidden, set())
        for path in SOURCES:
            with open(path, encoding="utf-8") as f:
                tree = ast.parse(f.read())
            calls = [n.func.id for n in ast.walk(tree)
                     if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)]
            self.assertNotIn("open", calls, path)

    def test_tc_nfr_1_parses_as_python_3_10(self):
        """TC-28: source uses no syntax newer than Python 3.10 (static check; only 3.14 installed)."""
        for path in SOURCES:
            with open(path, encoding="utf-8") as f:
                ast.parse(f.read(), filename=path, feature_version=(3, 10))


if __name__ == "__main__":
    unittest.main()
