"""Terminal shell around the rules core (design §3.3, ADR-001).

Prompts go through input_fn so they appear without a newline; every other
message goes through output_fn, one call per message.
"""

from tictactoe import game

MOVE_PROMPT = "Player {player}, choose a cell (1-9) or q: "
INVALID_INPUT = "Invalid input: enter a number from 1 to 9."
CELL_TAKEN = "Cell {n} is taken. Choose another."
WIN = "Player {player} wins!"
DRAW = "It's a draw!"
QUIT_KEYS = ("q", "Q")
PLAY_AGAIN_PROMPT = "Play again? (y/n): "
PLAY_AGAIN_INVALID = "Please enter y or n."
GOODBYE = "Goodbye."


def play_game(input_fn, output_fn):
    """Play one game. Return "over" on a win or draw, "quit" if a player enters q."""
    board = game.new_board()
    player = "X"
    output_fn(game.render(board))
    while True:
        text = input_fn(MOVE_PROMPT.format(player=player)).strip()
        if text in QUIT_KEYS:
            return "quit"
        try:
            idx = game.parse_cell(text)
            board = game.apply_move(board, idx, player)
        except game.CellTaken:
            output_fn(CELL_TAKEN.format(n=idx + 1))
            continue
        except ValueError:
            output_fn(INVALID_INPUT)
            continue
        output_fn(game.render(board))
        result = game.outcome(board)
        if result == "draw":
            output_fn(DRAW)
            return "over"
        if result is not None:
            output_fn(WIN.format(player=result))
            return "over"
        player = game.other(player)


def ask_play_again(input_fn, output_fn):
    """Return True for y/Y, False for n/N; re-prompt on anything else (AC-6.1 to AC-6.4)."""
    while True:
        text = input_fn(PLAY_AGAIN_PROMPT).strip()
        if text in ("y", "Y"):
            return True
        if text in ("n", "N"):
            return False
        output_fn(PLAY_AGAIN_INVALID)


def main(input_fn=input, output_fn=print):
    """Run games until a player quits or declines to play again. Always returns 0.

    End of input and Ctrl+C at any prompt also end the session (AC-5.2, AC-5.3).
    """
    try:
        while play_game(input_fn, output_fn) == "over" and ask_play_again(input_fn, output_fn):
            pass
    except (EOFError, KeyboardInterrupt):
        pass
    output_fn(GOODBYE)
    return 0
