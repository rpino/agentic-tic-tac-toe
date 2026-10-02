# Build Log — Tic tac toe game

| Date | Task | Branch / PR | ACs covered | Tests added | Reviewed by | Notes |
|---|---|---|---|---|---|---|
| 2026-10-01 | T-1 | `feature/T-1-rules-core` (local, no remote, no PR) | AC-1.1, AC-2.3, AC-3.1, AC-3.2, AC-3.3, AC-4.1, AC-4.2, AC-4.3 | `tests/test_game.py`: 15 tests, all passing | Pino | Tests failed first (no module), then passed after the change. Stdlib only. |
| 2026-10-01 | T-2 | `feature/T-2-single-game-cli` (local, no PR) | AC-1.2, AC-2.1, AC-2.2, AC-3.1, AC-3.2, AC-4.1, AC-4.2, AC-5.1 (q detection) | `tests/test_cli.py`: 12 tests; suite at 27, all passing | pending (Pino) | Tests failed first (no module). `play_game` returns `"quit"`; the "Goodbye." message and exit 0 for AC-5.1 are printed by `main` in T-3, the single exit point. |
