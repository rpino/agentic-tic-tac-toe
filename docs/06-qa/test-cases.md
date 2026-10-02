# Test Cases — Tic tac toe game

Levels: **U** = unit (`tests/test_game.py`), **F** = functional, through `cli` with scripted fake I/O (`tests/test_cli.py`), **E** = end-to-end, running the real `python -m tictactoe` in a subprocess with piped stdin, **S** = static check of the source (`tests/test_qa.py`), **M** = manual, in a real terminal.

## Automated
| TC | AC / NFR | Level | Steps / data | Expected | Automated test | Result |
|---|---|---|---|---|---|---|
| TC-01 | AC-1.1 | U | `render(new_board())` | Exact 5-line grid with cells 1–9 | `test_ac_1_1_empty_board_shows_cell_numbers` | Pass |
| TC-02 | AC-1.1 | U | Render a board with X and O | Marks replace the numbers | `test_ac_1_1_occupied_cells_show_marks` | Pass |
| TC-03 | AC-1.1, AC-1.2 | F | Start a game | Empty board first; prompt is exactly `Player X, choose a cell (1-9) or q: ` | `test_ac_1_1_game_starts_…`, `test_ac_1_2_…` | Pass |
| TC-04 | AC-2.1 | U, F | X plays 5 | Mark placed; board redrawn | `test_ac_2_1_places_mark`, `test_ac_2_1_valid_move_…` | Pass |
| TC-05 | AC-2.2 | F | 5, 1, q | Prompts go X, O, X | `test_ac_2_2_turn_passes_…` | Pass |
| TC-06 | AC-2.3 | U | `" 5 "`, `"\t7\n"`, digits 1–9 | Indexes 4, 6, 0–8 | `test_ac_2_3_*` | Pass |
| TC-07 | AC-3.1 | U | `""`, `"   "`, `0`, `05`, `+5`, `5.0`, `10`, `a`, `q`, `٥`, `-1` | `ValueError` for each | `test_ac_3_1_invalid_input_rejected` | Pass |
| TC-08 | AC-3.1 | F | `abc`, then empty input | Exact invalid-input message, twice; same player | `test_ac_3_1_invalid_input_message_same_player` | Pass |
| TC-09 | AC-3.2 | U | Move to an occupied cell | `CellTaken` (a subclass of `ValueError`) | `test_ac_3_2_occupied_cell_rejected`, `…_is_value_error` | Pass |
| TC-10 | AC-3.2 | F | 5, 5 | `Cell 5 is taken. Choose another.`; O prompted again | `test_ac_3_2_occupied_cell_message_same_player` | Pass |
| TC-11 | AC-3.3 | U | Rejected and accepted moves | Input board never mutated | `test_ac_3_3_board_unchanged_…`, `…_does_not_mutate_input` | Pass |
| TC-12 | AC-3.3 | F | 5, 5 | Only the error is printed; no redraw | `test_ac_3_3_rejected_move_prints_only_the_error` | Pass |
| TC-13 | AC-4.1 | U | All 8 lines, for both X and O | The winner is returned | `test_ac_4_1_every_line_wins` (16 subtests) | Pass |
| TC-14 | AC-4.1 | F | Full games: X wins, O wins | Final board, then `Player X wins!` / `Player O wins!` | `test_ac_4_1_win_…`, `test_ac_4_1_o_can_win` | Pass |
| TC-15 | AC-4.2 | U, F | Board XOX/XOO/OXX | `"draw"`; final board, then `It's a draw!` | `test_ac_4_2_*` | Pass |
| TC-16 | AC-4.3 | U, F | X completes a line on the 9th move | Win reported, not a draw | `test_ac_4_3_*` | Pass |
| TC-17 | AC-4.4 | F | X wins | Next prompt is the play-again prompt; no further move prompt | `test_ac_4_4_game_end_goes_to_play_again_prompt` | Pass |
| TC-18 | AC-5.1 | F | `q`, `Q`, `" q "` | Game ends; `Goodbye.`; returns 0 | `test_ac_5_1_q_quits`, `test_ac_5_1_q_prints_goodbye_…` | Pass |
| TC-19 | AC-5.2 | F, E | End of input at the move prompt and at the play-again prompt; empty stdin to the real program | `Goodbye.`; exit 0; no traceback | `test_ac_5_2_eof_at_either_prompt`, `test_ac_5_2_eof_exits_cleanly` | Pass |
| TC-20 | AC-5.3 | F | `KeyboardInterrupt` raised at either prompt (simulated) | `Goodbye.`; returns 0 | `test_ac_5_3_ctrl_c_at_either_prompt` | Pass (simulated only; see M-2, M-3) |
| TC-21 | AC-6.1, AC-6.3 | F | Win, then `n`, `N`, `" n "` | Exact prompt `Play again? (y/n): `; `Goodbye.`; 0 | `test_ac_6_1_…`, `test_ac_6_3_…` | Pass |
| TC-22 | AC-6.2 | F | Win, then `y`, `Y`, `" y "` | Empty board; X prompted | `test_ac_6_2_…` | Pass |
| TC-23 | AC-6.4 | F | `maybe`, `q`, `""` | `Please enter y or n.` ×3; prompt repeated | `test_ac_6_4_other_input_repeats_prompt` | Pass |
| TC-24 | AC-1.1, 1.2, 2.1, 2.2, 4.1, 6.1, 6.3 | E | Real program; stdin `1 4 2 5 3 n` | **Exact** full stdout match; empty stderr; exit 0 | `test_tc_e2e_exact_stdout_for_x_win_then_no` | Pass |
| TC-25 | AC-6.2, BR-1 | F | X wins → `y` → O wins → `n` | Second game starts fresh and reaches its own result | `test_tc_second_game_starts_clean_and_can_finish` | Pass |
| TC-26 | NFR-1 | S | Collect the package's imports | Standard library only | `test_tc_nfr_1_stdlib_only` | Pass |
| TC-27 | NFR-3 | S | Imports and calls | No socket, os, subprocess or urllib imports; no `open()` | `test_tc_nfr_3_no_network_file_or_os_access` | Pass |
| TC-28 | NFR-1 | S | Parse the source with Python 3.10 grammar | Parses | `test_tc_nfr_1_parses_as_python_3_10` | Pass (static check; only 3.14 installed) |
| — | NFR-2 | — | This table | Every AC has at least one automated TC | — | Pass (21/21) |

## Manual (real terminal; for Pino to run, about 5 minutes)
Run `python -m tictactoe` from `C:\Users\deadc\Projects\tic-tac-toe`.

| TC | AC | Steps | Expected | Result |
|---|---|---|---|---|
| M-1 | AC-1.1 to 4.2 | Play a full game to a win, typing moves | Board lines up; prompts sit on the same line as your cursor; win message shown | Pending |
| M-2 | AC-5.3 | Press Ctrl+C at a move prompt | `Goodbye.`, no traceback; `echo $LASTEXITCODE` → 0 | Pending |
| M-3 | AC-5.3 | Finish a game, then press Ctrl+C at `Play again?` | Same as M-2 | Pending |
| M-4 | AC-5.2 | Press Ctrl+Z then Enter at a move prompt | `Goodbye.`, exit 0 | Pending |
| M-5 | AC-6.2 | Finish a game, answer `y`, play a few moves | Fresh board; X moves first | Pending |

## Gaps found (not covered by any AC)
| Gap | Scenario | Raised to PO as |
|---|---|---|
| GAP-1 | After Ctrl+D/Ctrl+Z or Ctrl+C at a prompt, `Goodbye.` prints on the **same line** as the prompt (`Player X, choose a cell (1-9) or q: Goodbye.`). AC-5.2 and AC-5.3 only say "print Goodbye." | QA-1 |

## Defects
None found against the approved ACs.
