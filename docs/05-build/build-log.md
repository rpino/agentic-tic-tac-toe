# Build Log — Tic tac toe game

| Date | Task | Branch / PR | ACs covered | Tests added | Reviewed by | Notes |
|---|---|---|---|---|---|---|
| 2026-10-01 | T-1 | `feature/T-1-rules-core` (local, no remote, no PR) | AC-1.1, AC-2.3, AC-3.1, AC-3.2, AC-3.3, AC-4.1, AC-4.2, AC-4.3 | `tests/test_game.py`: 15 tests, all passing | Pino | Tests failed first (no module), then passed after the change. Stdlib only. |
| 2026-10-01 | T-2 | `feature/T-2-single-game-cli` (local, no PR) | AC-1.2, AC-2.1, AC-2.2, AC-3.1, AC-3.2, AC-4.1, AC-4.2, AC-5.1 (q detection) | `tests/test_cli.py`: 12 tests; suite at 27, all passing | Pino | Tests failed first (no module). `play_game` returns `"quit"`; the "Goodbye." message and exit 0 for AC-5.1 are printed by `main` in T-3, the single exit point. |
| 2026-10-01 | T-3 | `feature/T-3-session-loop` (local, no PR) | AC-4.4, AC-5.1 (Goodbye + exit 0), AC-5.2, AC-5.3, AC-6.1, AC-6.2, AC-6.3, AC-6.4 | `tests/test_cli.py`: +10 tests (8 `main`, 2 subprocess smoke tests); suite at 37, all passing | Pino | Tests failed first (16 failures/errors). `__main__.py` has the late-Ctrl+C guard (DES-2). Manual Ctrl+C check on a real Windows terminal left for QA (design §10). |
| 2026-10-01 | Fix (QA-1) | `fix/AC-5.4-goodbye-own-line` (local, no PR) | AC-5.4 (new in requirements v0.2) | `tests/test_qa.py`: +3 tests; suite at 45, all passing | Pino | From QA GAP-1 via REQ-4. Tests failed first (5 failures), then passed. One-line change: blank line before Goodbye. on EOF/Ctrl+C. |
