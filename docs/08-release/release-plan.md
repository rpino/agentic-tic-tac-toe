# Release Plan — Tic tac toe game v1.0.0

| Field | Value |
|---|---|
| Target date | 2026-10-01 (on go) |
| Feature flag | None. Design §7: a local single-user program, with nothing to switch on gradually. |
| Release owner | Pino |
| Go/no-go approver | Pino (Product Owner) |
| Release artifact | Git tag `v1.0.0` on `master` (currently at 751e898) |

## Scope
| Included | Deferred / out of scope |
|---|---|
| US-1 Start a game and see the board (AC-1.1, 1.2) | AI opponent |
| US-2 Take turns (AC-2.1 to 2.3) | GUI or web interface |
| US-3 Reject invalid moves (AC-3.1 to 3.3) | Online multiplayer |
| US-4 Win and draw detection (AC-4.1 to 4.4) | Score tracking or persistence |
| US-5 Quit at any time (AC-5.1 to 5.4) | Board sizes other than 3×3 |
| US-6 Play again (AC-6.1 to 6.4) | Packaging (pip / exe) |

All 22 ACs (requirements v0.2) pass. Details are in docs/06-qa/test-report.md.

## Rollout stages
There's one stage: tag the release and run it locally. With a single player-operator and no deployed service, staged rollout doesn't apply.

| Stage | Audience | Advance when | Owner |
|---|---|---|---|
| 1 | Pino (all users) | Go given; tag created; smoke check passes | Pino |

## Pre-flight checklist
- [x] Migrations: none (no data store)
- [x] Config / secrets: none
- [x] Dependencies: Python 3.10+ only; no third-party packages (TC-26)
- [x] QA approved: 45/45 automated tests and M-1 to M-5 manual checks pass
- [x] Review approved: no open findings; security checklist has no Critical, High or Medium findings
- [x] Release notes written (release-notes.md)
- [x] On go: `python -m unittest discover tests` passes on `master` and is run once more just before tagging
- [x] On go: `git tag -a v1.0.0 -m "Tic tac toe v1.0.0"`

## Monitoring
- **Health:** none at runtime (design §6: no logs or metrics for a local toy). The post-release check is a smoke run: `python -m tictactoe`, play one game, quit.
- **Success metrics (brief §5):** SDLC phases approved: 7 of 10 so far, and this release makes 8. Game playable with correct win/draw detection: yes (QA). AC test coverage: 100% (22/22).

## Rollback
1. Any problem: go back to the previous commit (`git checkout <previous-commit>`, or `git revert`), then delete the tag with `git tag -d v1.0.0`.
2. There's no data, so a rollback can't lose anything. Pino can trigger it.

## Go / No-go
- Decision: **GO** by Pino on 2026-10-01
