# Problem Brief — Tic tac toe game

| Field | Value |
|---|---|
| Requested by | Pino |
| Product Owner | Pino |
| Date | 2026-10-01 |
| Status | In review |

## 1. Problem statement
Pino wants to learn the Agentic SDLC process by running it end to end on a real (if small) project. There is no business problem; the "pain" is not yet having hands-on experience of every phase, gate and artifact. A tic-tac-toe game is small enough that the process, not the product, is the focus.

## 2. Affected users & stakeholders
- Primary users: Pino (learner and process operator); players of the game (two people sharing one device).
- Secondary / impacted teams: none.

## 3. Why now
No external pressure. Cost of doing nothing: the process stays untested and unlearned.

## 4. Hypothesis
We believe that **building a minimal tic-tac-toe game through all 10 SDLC phases** for **Pino** will result in **practical understanding of the process**. We will know we are right when **every phase is approved and a working, tested game exists**.

## 5. Success metrics
| Metric | Baseline | Target | Measured how / when |
|---|---|---|---|
| SDLC phases approved | 0 / 10 | 10 / 10 | `/sdlc-core:status` at end of project |
| Game playable with correct win/draw detection | No | Yes | QA test report |
| Acceptance criteria covered by tests | 0% | 100% | QA test report |

## 6. Constraints
- Business / contractual: none.
- Regulatory / compliance: none.
- Technical / legacy systems: single language (Python), standard library only; simplest viable interface.
- Timeline / capacity: minimise token usage and effort — prefer the simplest option at every decision.

## 7. Scope
**In scope (first release):**
- Classic 3×3 tic-tac-toe, X and O alternating turns.
- Input validation (invalid / occupied cells).
- Win and draw detection.

**Out of scope:**
- AI / computer opponent
- GUI or web interface
- Online / networked multiplayer
- Score persistence or history
- Board sizes other than 3×3

## 8. Assumptions & risks
| # | Assumption or risk | Impact if wrong | How we'll validate |
|---|---|---|---|
| A1 | Pino can approve every gate (PO, Tech Lead, QA Lead) | Gates stall | Confirmed at init |
| R1 | Process overhead outweighs the size of the product | Excess token/time cost | Keep artifacts short; review in retro |

## 9. Open questions (need a human decision)
- [x] Q1 (DIS-1): Interface — terminal hot-seat (two humans, one keyboard). Confirmed by Pino, 2026-10-01.
