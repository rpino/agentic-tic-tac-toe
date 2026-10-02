# Review Report — Tic tac toe game

Scope: every change on `master` from 5be559e to a54799f. That is T-1 (be051a1), T-2 (8424ec6), T-3 (f27ed66), the QA tests (8a5e7eb) and the AC-5.4 fix (b8a012c). There are no PRs: the repo is local with no remote, so the commits were reviewed directly.

| PR | Task | ACs | Reviewer (AI first pass) | Human approver | Decision |
|---|---|---|---|---|---|
| be051a1 | T-1 | AC-1.1, 2.3, 3.1–3.3, 4.1–4.3 | Claude | Pino | Approve |
| 8424ec6 | T-2 | AC-1.2, 2.1, 2.2, 3.1, 3.2, 4.1, 4.2, 5.1 | Claude | Pino | Approve |
| f27ed66 | T-3 | AC-4.4, 5.1–5.3, 6.1–6.4 | Claude | Pino | Approve |
| b8a012c | Fix (QA-1) | AC-5.4 | Claude | Pino | Approve |

**Overall:** the code matches the design (ADR-001: rules with no I/O, input and output passed in; ADR-002: unittest; DES-1: flat layout; DES-2: guard in `__main__.py`). There are 45 tests, each named after its AC, and they would fail if the behaviour broke: they assert exact strings and states, and nothing they test is mocked. There are no Blocker or Major findings.

## Findings
| File:line | Severity | Finding | Suggested fix | Status |
|---|---|---|---|---|
| docs/03-design/design.md §8 | Minor | Doc drift: the design's coverage table has no row for **AC-5.4**, added in requirements v0.2. The design doesn't mention the blank line before "Goodbye." either. Traceability from AC-5.4 to the design is missing. | Add a row: `AC-5.4 → cli.main (blank line before Goodbye. on EOF/Ctrl+C)`. Because this edits an approved artifact, the Tech Lead decides: a one-line doc fix, or leave it with this note. | **Fixed** (REV-1): row added to §8, and a note added to the §3.3 I/O conventions |
| tictactoe/cli.py:29-37 | Minor | `except ValueError` wraps both `parse_cell` and `apply_move`. Any unexpected `ValueError` from `apply_move` in future would show as "Invalid input" instead of failing loudly. Today `apply_move` only raises `CellTaken`, so the behaviour is correct. | Parse in its own `try`, and wrap only `apply_move` in `except CellTaken`. | **Fixed** (REV-2): parse and apply now in separate `try` blocks |
| tictactoe/cli.py:33 | Nit | `idx` in the `CellTaken` handler depends on `parse_cell` having succeeded in the same `try`. That's correct, but the coupling isn't obvious. | Fixed automatically by the previous suggestion. | **Fixed** (REV-2) |
| tictactoe/cli.py:66-67 | Nit | `while play_game(...) == "over" and ask_play_again(...): pass` is compact but takes a moment to read. | Optionally expand it into an explicit loop with `break`s. | **Fixed** (REV-2): explicit loop with `break`s |
| tests/test_cli.py, tests/test_qa.py | Nit | The fake-input and `run_main` helpers are written twice, once in each file. | Move them to a shared `tests/helpers.py` if more tests are added. | **Fixed** (REV-2): `tests/helpers.py` (`FakeIO`, `run_main`, `run_program`); `tests/__init__.py` added |
| tests/test_cli.py `test_full_game_then_quit` | Nit | A weak assertion: it only checks substrings. QA's TC-24 already covers the same path exactly. | Keep it as a smoke test, or delete it. | Accepted (noted in the QA report) |
| repo | Nit | No `.gitattributes`, so every commit prints LF/CRLF warnings. | Add `* text=auto`. | **Fixed** (REV-2): `.gitattributes` with `* text=auto eol=lf` |

## Security
Threat model: an offline, single-process terminal game. Its only input is the local player's keyboard and its only output is stdout. There is no network, no files, no stored data and no accounts.

| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Access control | N/A | No resources, users or endpoints |
| 2 | Authentication & session | N/A | No authentication |
| 3 | Input validation | Pass | Every input is trimmed and checked against an allowlist: `game.py` `parse_cell` (exactly one char in `"123456789"`); `cli.py:27` and `cli.py:53-56` (exact `q`/`y`/`n` sets). Tested by TC-07 (including Unicode digits and signs). |
| 4 | Injection | Pass | No SQL, shell or eval. User text is never used as a format template; `cli.py:33` only formats an int. |
| 5 | Secrets | Pass | None in the code or config |
| 6 | Sensitive data / PII | N/A | Nothing collected or stored |
| 7 | Dependencies | Pass | Zero third-party dependencies (TC-26) |
| 8 | Error handling | Pass | End of input and Ctrl+C give "Goodbye." and exit 0 with no traceback (`cli.py:68-71`, `__main__.py:7-11`; TC-19, TC-20, M-2 to M-4). Unexpected internal errors would still show a traceback; that's acceptable for a local tool. |
| 9 | Logging & audit | N/A | No security-relevant actions |
| 10 | Abuse cases | Pass / Low | A very long input line is read fully into memory by `input()`. The only person who can do that is the local user, against their own process, so it's accepted as Low. No other abuse paths. |
| 11 | Configuration | N/A | No configuration. TC-27 checks there's no network or file access. |

Security findings: **none Critical, High or Medium.** One Low (#10), accepted as described.

## Sign-off
- [x] No open Blocker/Major findings
- [x] No open Critical/High security findings
- Approved by: Pino on 2026-10-01

## Re-review after fixes (branch `chore/review-fixes`)
- Behaviour-preserving refactor only: all 45 tests pass, both through `discover` and module by module.
- No new findings. Security results are unchanged.
