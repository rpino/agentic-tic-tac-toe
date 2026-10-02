# Release Notes — Tic tac toe game v1.0.0 (2026-10-01)

## For players
Classic tic-tac-toe for two people sharing one keyboard, played in your terminal.

- **Start:** open a terminal in the project folder and run `python -m tictactoe`.
- **Play:** the board shows cells 1–9. On your turn, type a cell number and press Enter. X always goes first.
- **Mistakes are safe:** typos and taken cells are rejected with a message, and you keep your turn.
- **Results:** the game announces "Player X wins!", "Player O wins!" or "It's a draw!".
- **Play again:** answer `y` to start a fresh game, or `n` to leave.
- **Quit any time:** type `q`, or press Ctrl+C.

## For support (Pino)
- **Requirements:** Python 3.10 or newer. Nothing to install. Run it from the folder that contains `tictactoe/`.
- **Common questions:**
  - *"Python was not found"*: Python isn't on PATH. See the setup done at install time (the `python3` alias).
  - *"No module named tictactoe"*: you're in the wrong folder. `cd` to the project root first.
  - *"Can I play the computer?"*: no. That's out of scope for v1.
  - *"Is the score kept?"*: no. Each game is independent.
- **Known limitations:** terminal only; 3×3 only; tested on Windows with Python 3.14 (3.10 compatibility was checked statically; macOS and Linux weren't run).
- **Escalation:** open an issue in the project, or reopen a phase with `/sdlc-core:reopen`.

## For engineers
- **Layout:** `tictactoe/game.py` (pure rules, ADR-001), `tictactoe/cli.py` (prompts and messages, with input and output passed in), `tictactoe/__main__.py` (entry point with the late Ctrl+C guard, DES-2).
- **Tests:** `python -m unittest discover tests`. 45 tests: unit, functional (fake I/O in `tests/helpers.py`), end-to-end (subprocess) and static NFR checks (ADR-002).
- **Changes since planning:** AC-5.4 (blank line before "Goodbye." on end of input or Ctrl+C) was added through QA GAP-1 → REQ-4. The review cleanups REV-1 and REV-2 changed no behaviour.
- **No** migrations, flags, config, secrets or third-party dependencies.
- **Commits:** be051a1 (T-1), 8424ec6 (T-2), f27ed66 (T-3), b8a012c (AC-5.4), fb9f054 (review fixes). Local repo; no PRs.
- **Docs:** docs/01-discovery to docs/07-review; ADRs in docs/03-design/adr/.
