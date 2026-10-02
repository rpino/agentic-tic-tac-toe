# Retrospective — Tic tac toe game v1.0.0 (full SDLC run)

| Field | Value |
|---|---|
| Period | 2026-10-01, 18:59 to about 22:00 (UTC-7), one session |
| Participants | Pino (PO, Tech Lead, QA Lead); Claude (conductor and phase agents); requirements-reviewer and design-reviewer agents |

## Metrics
Sources: `.sdlc/state.json` history (62 events) and git (14 commits).

| Metric | Value | Notes |
|---|---|---|
| Total cycle time | About 3 hours | Idea to tagged release to health check, in one sitting |
| Phases approved | 9 of 10, plus Requirements re-approved once | Knowledge is pending this retro |
| Review submissions | 14 for 9 phases | 5 resubmissions: Requirements ×2, Design, QA, Review. Each came from a human decision on an open issue |
| Human decisions recorded | 10 issues (DIS-1, REQ-1 to 4, DES-1, 2, QA-1, 2, REV-1, 2) | All resolved; none guessed by the agent |
| Reopen events | 1 | Requirements, from QA GAP-1 → AC-5.4 |
| Gaps caught before production | 1 gap and 7 review findings | GAP-1 in QA; 2 Minor and 5 Nit findings in Review, all fixed |
| Escaped defects | 0 | Operate health check is clean |
| AI reviewer catches | 10 (5 requirements, 5 design) | Folded in before the gates; all 3 were still valid when checked later |

## What went well
- **The gates did their job.** Every scope or rule choice went to Pino: who moves first, play again, layout, the Ctrl+C guard, GAP-1. None were invented.
- **Traceability held end to end:** US → AC → design table → T-n → test names → TC-n → review → release notes.
- **Writing tests first caught real issues:** an exact-prompt mismatch was prevented in design, and the ninth-move-win case was pinned down.
- **The feedback loop worked as designed.** QA found GAP-1, Requirements was reopened, the PO decided, the AC was added, the fix came with tests first, and everything was re-approved, without disturbing the other phases.
- **The reviewer agents added real value** before the human gates: input ambiguity, untestable ACs, how prompts are printed, and the Windows Ctrl+C edge case.

## What didn't
- **Setup friction on Windows.** `python3` pointed to the Microsoft Store stub, so the hooks would have failed until it was fixed by hand.
- **The code gate can't be configured through the tool.** `tictactoe/` couldn't be added to the gated paths (DES-1), so the rule was followed by convention only.
- **Git and state friction.** `approve` changes `.sdlc/state.json`, which once blocked a `git checkout` and put a commit on the wrong branch (it was fast-forwarded afterwards).
- **Overhead compared with the product size.** 10 phases and 10 decisions for about 120 lines of code. That was fine for learning the process, but too heavy for routine small changes (brief R1).
- Small slips: a garbled test line (fixed before it ran), a broken table row from a sed command, the `main` vs `master` branch name, and LF/CRLF warnings until `.gitattributes` was added.

## Where AI helped / missed
| Phase | Helped | Missed |
|---|---|---|
| Discovery | Turned a vague idea into a measurable brief in about 3 questions | — |
| Requirements | The reviewer made the input rules exact and split EOF from Ctrl+C | Didn't specify **line breaks** for messages printed after a prompt (became GAP-1) |
| Design | The reviewer caught that prompts must go through `input_fn`, the trim-before-`q` order and the late Windows Ctrl+C | Didn't trace AC-5.4 later (REV-1 caught it) |
| Planning | Full AC coverage across 3 small tasks | — |
| Build | Test-first with AC-named tests; 37 tests | Its smoke tests only checked substrings (flagged by QA) |
| QA | Exact full-output test; found GAP-1 from a manual run; NFR checks | Ctrl+C only simulated; a human check was needed |
| Review | Doc drift, an error-handling smell, test duplication | — |
| Release / Operate | Concise plan, notes, smoke check | — |

## Proposed standing rules
| # | Rule | Source | Decision |
|---|---|---|---|
| SR-1 | Every AC that specifies exact terminal output also states line boundaries (what happens to the prompt line when a message follows it). | GAP-1 / REQ-4 | **Adopted** (Pino, 2026-10-01) |
| SR-2 | Every CLI user flow has at least one end-to-end test that asserts the **exact full stdout** of the real program, not substrings. | QA TC-24, review finding | **Adopted** (Pino, 2026-10-01) |
| SR-3 | Run `python -m unittest discover tests` and get a pass before every commit. | Build/QA practice | **Adopted** (Pino, 2026-10-01) |
| SR-4 | Commit `.sdlc/state.json` after each approval, before any `git checkout` or merge. | QA approval branch slip | **Adopted** (Pino, 2026-10-01) |

## Marketplace improvements (proposed, for every project)
These are not edits to the installed plugin. They'd be made in the marketplace repo if Pino wants them.
- **M-1:** `sdlc_state.py` needs a `settings` command (e.g. `settings add-code-path tictactoe/`), so the code gate covers non-standard layouts (DES-1).
- **M-2:** the hooks call `python3`, which is missing on many Windows machines. Fall back to `py -3` or `python`, or document the alias step in the README.
- **M-3:** the `acceptance-criteria` skill's checklist should ask, for CLI or terminal output, about newline and line-boundary behaviour (SR-1 in general form).
- **M-4:** consider a "lite" phase set for very small changes. The README roadmap already lists one.

## Action items
| Action | Owner | Due |
|---|---|---|
| All four adopted and written into `CLAUDE.md` | Pino → Claude | Done 2026-10-01 |
| M-1 and M-2: implement now in the marketplace repo. M-3 and M-4: not now | Pino → Claude | 2026-10-01 |

## Follow-up done (2026-10-01)
- **SR-1 to SR-4** written into `CLAUDE.md` → "Standing rules learned on this project".
- **M-1 done:** `sdlc_state.py settings show | add-code-path | remove-code-path | require-tests` (marketplace repo). Used on this project with `settings add-code-path tictactoe/`, so the code gate now covers `tictactoe/`. That closes the known gap from design DES-1.
- **M-2 done:** `scripts/run_py.sh` launcher (tries python3, then python, then py, skipping the Store stub). The hooks now call it. Verified in a shell where `python3` and `python` were both stubs: it picked the real Python, and the gate still denied a direct edit to the state file.
- The marketplace changes are uncommitted in the marketplace repo. The installed plugin picks them up only after the marketplace is updated or reinstalled.
- **M-3, M-4:** not now (Pino).
