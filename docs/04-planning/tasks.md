# Implementation Plan — Tic tac toe game

| Field | Value |
|---|---|
| Design | docs/03-design/design.md (approved 2026-10-01) |
| Status | In review |

## Milestones
1. M1: rules core done and fully unit-tested, with no I/O (T-1).
2. M2: one full game playable in the terminal (T-2).
3. M3: play again, quit and clean exit everywhere; release candidate (T-3).

## Tasks
Estimates are the agent's guess (S = under 1 hour with an agent). Owner: Pino, pairing with Claude.

| ID | Title | ACs | Depends on | Est. | Owner | Status |
|---|---|---|---|---|---|---|
| T-1 | Rules core (`game.py`) | AC-1.1, AC-2.3, AC-3.1, AC-3.2, AC-3.3, AC-4.1, AC-4.2, AC-4.3 | — | S | Pino | done (in review) |
| T-2 | Single game CLI (`cli.play_game`) | AC-1.2, AC-2.1, AC-2.2, AC-3.1, AC-3.2, AC-4.1, AC-4.2, AC-5.1 | T-1 | S | Pino | done (in review) |
| T-3 | Session loop, play again and exit handling (`cli.main`, `ask_play_again`, `__main__.py`) | AC-4.4, AC-5.2, AC-5.3, AC-6.1, AC-6.2, AC-6.3, AC-6.4 | T-2 | S | Pino | todo |

### T-1: Rules core
- **What:** `tictactoe/__init__.py` and `tictactoe/game.py`, with `new_board`, `parse_cell`, `apply_move`, `CellTaken`, `outcome`, `other` and `render`, exactly as in design §3.3. No I/O.
- **Satisfies:** AC-1.1 (exact render), AC-2.3 and AC-3.1 (parsing, including every case in design §4), AC-3.2 and AC-3.3 (occupied cell; board not mutated), AC-4.1 to AC-4.3 (all 8 lines; draw; a win on the ninth move beats a draw).
- **Tests that prove it:** `tests/test_game.py`, one `unittest` test (or a `subTest` table) per AC, named `test_ac_<n>_<m>_…`.
- **Definition of done:** `python -m unittest discover tests` passes; every AC above has a named test; only stdlib imports.

### T-2: Single game CLI
- **What:** `tictactoe/cli.py`, with message and prompt constants copied verbatim from the ACs, and `play_game(input_fn, output_fn)`. Prompts go through `input_fn`. The order is: trim, check q/Q, parse, apply. After a rejected move, print only the error. Return `"over"` or `"quit"`.
- **Satisfies:** AC-1.2, AC-2.1, AC-2.2, AC-3.1 and AC-3.2 (messages), AC-4.1 and AC-4.2 (result messages), AC-5.1 (including `" q "`).
- **Tests that prove it:** `tests/test_cli.py`, with a scripted fake `input_fn` that records prompts and a list-collecting `output_fn`. It asserts exact prompts and messages, including a full X-wins game, a draw game, an invalid-then-valid move, and quitting.
- **Definition of done:** tests pass; for each AC, the asserted strings match the requirements character for character.

### T-3: Session loop, play again and exit handling
- **What:** `ask_play_again` and `main(input_fn=input, output_fn=print) -> int` in `cli.py`; `tictactoe/__main__.py`, which runs `sys.exit(main())` with the late `KeyboardInterrupt` guard (DES-2).
- **Satisfies:** AC-4.4, AC-5.2, AC-5.3 (at both prompts), AC-6.1 to AC-6.4.
- **Tests that prove it:** `tests/test_cli.py`. The `y`/`Y` answers start a new game with an empty board and X to move; `n`/`N` prints "Goodbye." and returns 0; any other answer re-prompts; the fake raises `EOFError` or `KeyboardInterrupt` at each prompt and the test checks for "Goodbye." and a return value of 0. One subprocess smoke test runs `python -m tictactoe` with piped input and checks exit code 0.
- **Definition of done:** all tests pass; a manual Windows Ctrl+C check is noted for QA (design §10).

## Coverage check
| AC | Tasks |
|---|---|
| AC-1.1 | T-1 |
| AC-1.2 | T-2 |
| AC-2.1, AC-2.2 | T-2 |
| AC-2.3 | T-1 |
| AC-3.1, AC-3.2 | T-1 (logic), T-2 (messages) |
| AC-3.3 | T-1 |
| AC-4.1, AC-4.2 | T-1 (logic), T-2 (messages) |
| AC-4.3 | T-1 |
| AC-4.4 | T-3 |
| AC-5.1 | T-2 |
| AC-5.2, AC-5.3 | T-3 |
| AC-6.1 – AC-6.4 | T-3 |
| NFR-1, NFR-3 | All (stdlib only; stdin/stdout only) |
| NFR-2 | All (every AC has a named test) |

All 21 ACs are covered.

## Risks / spikes
- No spikes needed.
- Process note: the code-gate hook doesn't watch `tictactoe/` (design DES-1), so the rule is followed by convention. Each task is committed with its tests, which satisfies the "no commit without a test change" hook.
- Ticket sync: none. No Jira or Linear connector is set up, and this is a solo project.
