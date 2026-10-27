"""
Fast Draw — reflex timing rules (book: react within 0.3s after DRAW).

Wait is random 2.0–5.0 seconds before the draw signal.
"""

from __future__ import annotations

import random
from typing import Any, Literal

WAIT_MIN_TENTHS = 20
WAIT_MAX_TENTHS = 50
DRAW_WINDOW_SEC = 0.3
EARLY_THRESHOLD_SEC = 0.01

Outcome = Literal["win", "slow", "early"]


def random_wait_seconds() -> float:
    return random.randint(WAIT_MIN_TENTHS, WAIT_MAX_TENTHS) / 10.0


def evaluate_reaction(elapsed_sec: float, *, early: bool = False) -> dict[str, Any]:
    if early or elapsed_sec < EARLY_THRESHOLD_SEC:
        return {
            "outcome": "early",
            "elapsed_sec": round(max(elapsed_sec, 0.0), 4),
            "message": 'You drew before "DRAW" appeared! You lose.',
        }
    if elapsed_sec > DRAW_WINDOW_SEC:
        return {
            "outcome": "slow",
            "elapsed_sec": round(elapsed_sec, 4),
            "message": f"You took {round(elapsed_sec, 4)} seconds to draw. Too slow!",
        }
    elapsed = round(elapsed_sec, 4)
    return {
        "outcome": "win",
        "elapsed_sec": elapsed,
        "message": (
            f"You took {elapsed} seconds to draw. "
            "You are the fastest draw in the west! You win!"
        ),
    }


def config_for_client() -> dict[str, float]:
    return {
        "draw_window_sec": DRAW_WINDOW_SEC,
        "early_threshold_sec": EARLY_THRESHOLD_SEC,
        "wait_min_sec": WAIT_MIN_TENTHS / 10.0,
        "wait_max_sec": WAIT_MAX_TENTHS / 10.0,
    }
