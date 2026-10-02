"""Entry point: python -m tictactoe"""

import sys

from tictactoe.cli import main

try:
    sys.exit(main())
except KeyboardInterrupt:
    # A late Ctrl+C on Windows can arrive after main() has said goodbye (DES-2, AC-5.3).
    sys.exit(0)
