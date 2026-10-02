"""Pure tic-tac-toe rules: no I/O (design §3.3, ADR-001).

A board is a list of 9 strings, each " ", "X" or "O"; index 0-8 is cell 1-9.
"""

EMPTY = " "
VALID_CELLS = "123456789"
LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),             # diagonals
)


class CellTaken(ValueError):
    """Raised when a move targets an occupied cell (AC-3.2)."""


def new_board():
    return [EMPTY] * 9


def parse_cell(text):
    """Return the 0-based index for input that is exactly one digit 1-9 after trimming (AC-2.3, AC-3.1)."""
    text = text.strip()
    if len(text) != 1 or text not in VALID_CELLS:
        raise ValueError(f"invalid cell: {text!r}")
    return int(text) - 1


def apply_move(board, idx, player):
    """Return a new board with player's mark at idx; never mutates board (AC-3.3)."""
    if board[idx] != EMPTY:
        raise CellTaken(idx)
    new = list(board)
    new[idx] = player
    return new


def outcome(board):
    """Return "X" or "O" for a win, "draw" for a full board, else None. Wins take priority (AC-4.3)."""
    for a, b, c in LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    if EMPTY not in board:
        return "draw"
    return None


def other(player):
    return "O" if player == "X" else "X"


def render(board):
    """Board in the exact AC-1.1 format; empty cells show their number."""
    cells = [mark if mark != EMPTY else str(i + 1) for i, mark in enumerate(board)]
    rows = [" " + " | ".join(cells[r:r + 3]) for r in (0, 3, 6)]
    return "\n---+---+---\n".join(rows)
