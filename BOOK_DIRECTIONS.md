# Book directions — Fast Draw

**Catalog #463** · Al Sweigart, *The Big Book of Small Python Projects*, **Project #25** — Fast Draw

- Invent with Python: [project25.html](https://inventwithpython.com/bigbookpython/project25.html)
- Upstream: [fastdraw.py](https://github.com/asweigart/the-big-book-of-small-python-projects/blob/main/fastdraw.py)
- Local reference: [`reference/fastdraw.py`](./reference/fastdraw.py)
- Shared logic: [`fast_draw_core.py`](./fast_draw_core.py)

## What the book asks you to build

A reflex mini-game:

1. Random pause (~2–5 seconds) with “It is high noon...”
2. Print **DRAW!** and start the timer.
3. Player presses Enter; if elapsed **&gt; 0.3s**, too slow; if **&lt; 0.01s**, they acted before DRAW (buffered Enter).
4. Otherwise they win. Loop until QUIT.

## Web version (`web/` — FastAPI, port **3023**)

| Book step | Web equivalent |
|-----------|----------------|
| Random wait | `GET /api/wait` → `random_wait_seconds` |
| DRAW + timer | Client `performance.now()` after DRAW shown |
| Enter / early / slow | Click or Space; `POST /api/evaluate` |
| 0.3s window | `fast_draw_core.DRAW_WINDOW_SEC` |

CLI: [`reference/run_cli.py`](./reference/run_cli.py)
