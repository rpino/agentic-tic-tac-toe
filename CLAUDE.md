# Tic tac toe game — Agentic SDLC rules

This project follows the **Agentic SDLC** process (sdlc-core plugin).

## Always
- Before doing any work, read `.sdlc/state.json` (or run `/sdlc-core:status`) to know the current phase.
- Work only on the current phase. Never skip ahead.
- Every phase produces its artifact in `docs/NN-<phase>/`. The artifact of one phase is the input of the next.
- Every requirement, design element, task, test and PR must trace back to an acceptance criterion ID (e.g. `AC-1.2`).
- When you finish a phase artifact, set it to `in_review` and STOP. A human approves with `/sdlc-core:approve`.
- If you find a gap in an earlier phase (missing AC, wrong design), reopen that phase — don't silently patch around it.

## Never
- Never edit `.sdlc/state.json` directly. Use the sdlc-core skills.
- Never approve a phase on a human's behalf.
- Never write code under `src/`, `app/`, `lib/`, `tests/` … before Planning is approved (a hook enforces this).
- Never commit code without a test change (a hook enforces this).

## Standing rules learned on this project
<!-- sdlc-knowledge:knowledge-updater appends lessons here after each retro -->
- Every AC that specifies exact terminal output also states line boundaries: what happens to the prompt line when a message follows it. (Retro SR-1; QA GAP-1 → AC-5.4)
- Every CLI user flow has at least one end-to-end test that asserts the exact full stdout of the real program, not substrings. (Retro SR-2; QA TC-24)
- Run `python -m unittest discover tests` and get a pass before every commit. (Retro SR-3)
- Commit `.sdlc/state.json` after each approval, before any `git checkout` or merge. (Retro SR-4; QA approval branch slip)
