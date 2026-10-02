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
