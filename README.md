# Fast Draw (catalog #463)

Al Sweigart — *The Big Book of Small Python Projects*, Project #25.

| Artifact | Path |
|----------|------|
| Book steps | [`BOOK_DIRECTIONS.md`](./BOOK_DIRECTIONS.md) |
| Upstream script | [`reference/fastdraw.py`](./reference/fastdraw.py) |
| CLI | [`reference/run_cli.py`](./reference/run_cli.py) |
| Shared logic | [`fast_draw_core.py`](./fast_draw_core.py) |
| Web (FastAPI) | [`web/`](./web/) — port **3023** |

## Run the web demo

```powershell
Set-Location "c:\Users\emmak\Desktop\Content\CodingProjects\PortProjects\demos\fast-draw\web"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 3023
```

Open [http://127.0.0.1:3023/](http://127.0.0.1:3023/).

## Run the CLI

```powershell
Set-Location "c:\Users\emmak\Desktop\Content\CodingProjects\PortProjects\demos\fast-draw"
python reference\run_cli.py
```

Portfolio: [`PORTFOLIO_INTEGRATION.md`](./PORTFOLIO_INTEGRATION.md).
