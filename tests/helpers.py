"""Shared test helpers: scripted fake I/O and running the real program."""

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class FakeIO:
    """Scripted input_fn that records prompts, and an output_fn that collects messages.

    A reply that is an exception instance is raised instead of returned
    (e.g. EOFError() for end of input, KeyboardInterrupt() for Ctrl+C).
    """

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


def run_main(replies):
    """Run cli.main with scripted replies; return (exit code, FakeIO)."""
    from tictactoe import cli

    io = FakeIO(replies)
    return cli.main(io.input_fn, io.output_fn), io


def run_program(stdin_text):
    """Run the real program (python -m tictactoe) with piped stdin."""
    return subprocess.run(
        [sys.executable, "-m", "tictactoe"],
        input=stdin_text, capture_output=True, text=True, cwd=ROOT, timeout=10,
    )
