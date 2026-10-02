# ADR-001: Pure rules core with an injectable-I/O CLI shell

- **Status:** Proposed
- **Date:** 2026-10-01
- **Deciders:** Pino (Tech Lead)
- **Related:** NFR-2, AC-1 to AC-6

## Context
NFR-2 requires 100% of ACs to be covered by automated tests that don't need a terminal. Many ACs specify exact prompts and messages, and the brief asks to keep effort low.

## Options considered
### Option A — Single script calling `input()` and `print()` directly
- Pros: fewest lines.
- Cons: tests must patch builtins or spawn subprocesses for every AC, which is brittle and slow, and the rules can't be tested alone.

### Option B — Pure `game.py` plus a `cli.py` that receives `input_fn` and `output_fn`
- Pros: rules are tested as plain functions; CLI ACs are tested by passing a scripted input list and capturing output; no mocking library needed.
- Cons: two modules instead of one (about 20 extra lines).

## Decision
Option B. The small extra structure is what makes NFR-2 cheap to meet.

## Consequences
- `cli.main` takes `input_fn` and `output_fn`, defaulting to `input` and `print`.
- `EOFError` and `KeyboardInterrupt` are raised by `input_fn`, so tests simulate them by raising from a fake.
