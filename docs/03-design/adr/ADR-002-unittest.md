# ADR-002: Use stdlib `unittest` for tests

- **Status:** Proposed
- **Date:** 2026-10-01
- **Deciders:** Pino (Tech Lead)
- **Related:** NFR-1, NFR-2

## Context
The brief allows only the Python standard library and asks for minimal setup. Tests must run on Windows, macOS and Linux.

## Options considered
### Option A — `pytest`
- Pros: shorter test syntax and better failure output.
- Cons: a third-party dependency, so it needs a pip install and a virtual environment.

### Option B — `unittest`
- Pros: ships with Python; run with `python -m unittest discover tests` from the repo root (flat layout, DES-1); zero setup.
- Cons: more boilerplate per test.

## Decision
Option B, to keep zero dependencies and zero setup. pytest can still run unittest tests later if the team wants it.

## Consequences
- Tests live in `tests/test_*.py` as `unittest.TestCase` classes.
- Each test names the AC it covers (e.g. `test_ac_3_2_occupied_cell_rejected`).
