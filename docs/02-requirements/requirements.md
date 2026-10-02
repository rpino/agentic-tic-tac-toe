# Requirements — Tic tac toe game

| Field | Value |
|---|---|
| Source brief | docs/01-discovery/problem-brief.md |
| Product Owner | Pino |
| Version / date | v0.2 — 2026-10-01 (REQ-4: AC-5.4 added) |
| Status | In review |

## 1. Summary
A two-player, hot-seat tic-tac-toe game played in a terminal on one keyboard. It exists to exercise the full Agentic SDLC end to end (brief §1, §4), so scope is the classic 3×3 game only.

## 2. User stories & acceptance criteria

### US-1: Start a game and see the board · Priority: Must · Traces to: Brief §4, §5 metric 2
As a **player**, I want **to start a game and see an empty board with cell numbers** so that **I know where I can move**.

**Acceptance criteria**
- **AC-1.1** WHEN the game starts THE SYSTEM SHALL display an empty 3×3 board whose cells are labelled 1–9, left to right, top to bottom, in exactly this format (an occupied cell shows X or O in place of its number):
  ```
   1 | 2 | 3
  ---+---+---
   4 | 5 | 6
  ---+---+---
   7 | 8 | 9
  ```
- **AC-1.2** WHEN the game starts THE SYSTEM SHALL prompt player X to move first (BR-1) with the exact prompt `Player X, choose a cell (1-9) or q: `.

### US-2: Take turns placing marks · Priority: Must · Traces to: Brief §7, §5 metric 2
As a **player**, I want **to place my mark by typing a cell number** so that **we can play alternately on one keyboard**.

**Acceptance criteria**
- **AC-2.1** WHEN the current player enters a number 1–9 for an empty cell THE SYSTEM SHALL place that player's mark in the cell and redisplay the board.
- **AC-2.2** WHEN a valid move does not end the game THE SYSTEM SHALL pass the turn to the other player and prompt with `Player <X|O>, choose a cell (1-9) or q: `.
- **AC-2.3** THE SYSTEM SHALL trim leading and trailing whitespace from input before validating it (e.g. " 5 " is treated as "5").

### US-3: Reject invalid moves · Priority: Must · Traces to: Brief §7
As a **player**, I want **bad input to be rejected with a clear message** so that **a typo doesn't lose my turn or break the game**.

**Acceptance criteria**
- **AC-3.1** IF the trimmed input is anything other than exactly one ASCII digit 1–9 (including empty input, "0", "05", "+5", "5.0", "10", letters other than q/Q, and non-ASCII digits) THEN THE SYSTEM SHALL show "Invalid input: enter a number from 1 to 9." and prompt the same player again.
- **AC-3.2** IF the chosen cell is already occupied THEN THE SYSTEM SHALL show "Cell <n> is taken. Choose another." and prompt the same player again.
- **AC-3.3** IF a move is rejected THEN THE SYSTEM SHALL leave the board unchanged.

### US-4: Detect win and draw · Priority: Must · Traces to: Brief §5 metric 2
As a **player**, I want **the game to announce a win or draw** so that **we know who won without checking ourselves**.

**Acceptance criteria**
- **AC-4.1** WHEN a move completes three of the same mark in any row, column or diagonal THE SYSTEM SHALL display the final board and "Player <X|O> wins!" and end the game.
- **AC-4.2** WHEN the ninth cell is filled without a win THE SYSTEM SHALL display the final board and "It's a draw!" and end the game.
- **AC-4.3** IF the ninth move also completes a line THEN THE SYSTEM SHALL report the win, not a draw.
- **AC-4.4** WHEN the game has ended (win or draw) THE SYSTEM SHALL accept no further moves on that board and go to the play-again prompt (US-6).

### US-5: Quit at any time · Priority: Should · Traces to: Brief §6 (simplest viable interface)
As a **player**, I want **to quit mid-game** so that **I don't have to finish or kill the terminal**.

**Acceptance criteria**
- **AC-5.1** WHEN a player enters "q" or "Q" at the move prompt THE SYSTEM SHALL print "Goodbye." and exit with status 0.
- *AC-5.2, AC-5.3 and AC-5.4 apply at both the move prompt and the play-again prompt.*
- **AC-5.2** IF the input stream ends (end-of-file: Ctrl+D on macOS/Linux, Ctrl+Z then Enter on Windows) THEN THE SYSTEM SHALL print "Goodbye." and exit with status 0 without a traceback.
- **AC-5.3** IF the player interrupts with Ctrl+C THEN THE SYSTEM SHALL print "Goodbye." and exit with status 0 without a traceback.
- **AC-5.4** WHEN "Goodbye." is printed because of AC-5.2 or AC-5.3 THE SYSTEM SHALL print it on its own line, never on the same line as the prompt.

### US-6: Play again · Priority: Should · Traces to: PO decision REQ-2 (2026-10-01)
As a **player**, I want **to start a new game after one ends** so that **we can keep playing without restarting the program**.

**Acceptance criteria**
- **AC-6.1** WHEN a game ends (win or draw) THE SYSTEM SHALL show the exact prompt `Play again? (y/n): `.
- **AC-6.2** WHEN the player enters "y" or "Y" (after trimming whitespace) THE SYSTEM SHALL start a new game with an empty board (AC-1.1) and X to move (BR-1).
- **AC-6.3** WHEN the player enters "n" or "N" (after trimming whitespace) THE SYSTEM SHALL print "Goodbye." and exit with status 0.
- **AC-6.4** IF the input is anything else THEN THE SYSTEM SHALL show "Please enter y or n." and repeat the play-again prompt.

## 3. Business rules
| ID | Rule | Source |
|---|---|---|
| BR-1 | X always moves first, in every game. | PO decision REQ-1, 2026-10-01 |
| BR-2 | Players alternate; a rejected move does not consume a turn. | Classic rules |
| BR-3 | After each game the players may start another in the same run (US-6). | PO decision REQ-2, 2026-10-01 |

## 4. Non-functional requirements
| ID | Category | Requirement (measurable) |
|---|---|---|
| NFR-1 | Portability | Runs with Python 3.10+ standard library only, on Windows, macOS and Linux terminals. |
| NFR-2 | Testability | Game rules (move validation, win/draw detection) are testable without a terminal; 100% of ACs covered by automated tests (brief §5 metric 3). |
| NFR-3 | Security | No network, file or OS access beyond stdin/stdout. |

## 5. Out of scope
- AI / computer opponent
- GUI or web interface
- Online / networked multiplayer
- Score persistence or history
- Board sizes other than 3×3
- Score tracking across replayed games

## 6. Open questions (need a PO decision)
- [x] Q1 (REQ-1): X always moves first — confirmed by Pino.
- [x] Q2 (REQ-2): Add a "play again?" prompt — decided by Pino; added as US-6.
- [x] Q3 (REQ-3): Keep US-5 (quit) as Should — confirmed by Pino.
- [x] Q4 (REQ-4, from QA GAP-1): "Goodbye." must appear on its own line after end-of-input or Ctrl+C. Decided by Pino; added AC-5.4.

## 7. Traceability
| AC | Story | Brief metric / section |
|---|---|---|
| AC-1.1, AC-1.2 | US-1 | §5 metric 2 |
| AC-2.1 – AC-2.3 | US-2 | §5 metric 2, §7 |
| AC-3.1 – AC-3.3 | US-3 | §7 (input validation) |
| AC-4.1 – AC-4.4 | US-4 | §5 metric 2, §7 (win/draw) |
| AC-5.1 – AC-5.4 | US-5 | §6 (AC-5.4 from QA GAP-1) |
| AC-6.1 – AC-6.4 | US-6 | PO decision REQ-2 |
| All | — | §5 metric 3 (100% AC test coverage, NFR-2) |
