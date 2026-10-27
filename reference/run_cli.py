"""Terminal Fast Draw — uses shared fast_draw_core timing rules."""

from __future__ import annotations

import sys
import time
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from fast_draw_core import evaluate_reaction, random_wait_seconds  # noqa: E402

print(
    """Fast Draw

When you see DRAW, you have 0.3 seconds to press Enter.
You lose if you press Enter before DRAW appears.
"""
)
input("Press Enter to begin...")

while True:
    print()
    print("It is high noon...")
    time.sleep(random_wait_seconds())
    print("DRAW!")
    draw_time = time.time()
    input()
    result = evaluate_reaction(time.time() - draw_time)
    print(result["message"])

    print("Enter QUIT to stop, or press Enter to play again.")
    if input("> ").strip().upper() == "QUIT":
        print("Thanks for playing!")
        break
