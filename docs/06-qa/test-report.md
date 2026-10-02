# Test Report — Tic tac toe game

| Field | Value |
|---|---|
| Build | `master` + fix for AC-5.4 (branch `fix/AC-5.4-goodbye-own-line`) |
| Environment | Windows 11, Python 3.14.4, `python -m unittest discover tests` |
| Date | 2026-10-01 |
| QA Lead | Pino |

## Summary
- **Automated:** 45 tests, **45 passed**, 0 failed, 0 flaky.
- **AC coverage:** 22 of 22 ACs (requirements v0.2) have at least one passing automated TC (see test-cases.md).
- **NFRs:** NFR-1 (static checks), NFR-2 (coverage) and NFR-3 (static check) pass.
- **Manual:** 5 of 5 checks (M-1 to M-5) passed; run by Pino in a real Windows terminal, including a real Ctrl+C.
- **Defects:** none. **Gaps:** 1 (GAP-1), resolved: PO added AC-5.4, which is fixed and tested.

## AC coverage matrix
| AC | TCs | Result |
|---|---|---|
| AC-1.1 | TC-01, 02, 03, 24 | Pass |
| AC-1.2 | TC-03, 24 | Pass |
| AC-2.1 | TC-04, 24 | Pass |
| AC-2.2 | TC-05, 24 | Pass |
| AC-2.3 | TC-06 | Pass |
| AC-3.1 | TC-07, 08 | Pass |
| AC-3.2 | TC-09, 10 | Pass |
| AC-3.3 | TC-11, 12 | Pass |
| AC-4.1 | TC-13, 14, 24 | Pass |
| AC-4.2 | TC-15 | Pass |
| AC-4.3 | TC-16 | Pass |
| AC-4.4 | TC-17 | Pass |
| AC-5.1 | TC-18 | Pass |
| AC-5.2 | TC-19, M-4 | Pass |
| AC-5.3 | TC-20 (simulated), M-2, M-3 (real) | Pass |
| AC-5.4 | TC-29 | Pass |
| AC-6.1 | TC-21, 24 | Pass |
| AC-6.2 | TC-22, 25 | Pass |
| AC-6.3 | TC-21, 24 | Pass |
| AC-6.4 | TC-23 | Pass |

## What QA added beyond Build
- **TC-24:** an exact, character-for-character check of the real program's full stdout. The Build smoke tests only checked that key phrases appeared.
- **TC-25:** play again across two complete games, so state from one game can't leak into the next.
- **TC-26 to TC-28:** NFR checks (standard library only; no network, file or OS access; Python 3.10 syntax).
- The manual checklist, and one gap.

## Watch for false greens
- **TC-20 (AC-5.3)** raises `KeyboardInterrupt` from a fake input function. It doesn't test a real Ctrl+C signal, which is why manual checks M-2 and M-3 exist.
- **The Build smoke test `test_full_game_then_quit`** only checks for substrings, so on its own it's a weak test. TC-24 now covers the same path exactly.
- No test mocks the code it tests, and no test was changed to make it pass.

## Risks
| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| A real Windows Ctrl+C behaves differently from the simulation | Low | Low | Guard in `__main__.py`; M-2, M-3 |
| Python 3.10 to 3.13, macOS and Linux never actually run | Low | Low | Static 3.10 parse; only stdlib used |
| GAP-1 looks untidy on screen | — | — | Resolved by AC-5.4 |

## Recommendation
**Ready.** Every AC has a passing test, the manual checks passed and GAP-1 is resolved.
