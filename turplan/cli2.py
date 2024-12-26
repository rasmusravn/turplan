from typing import Annotated, Optional
from pathlib import Path

import typer

app = typer.Typer()

@app.command()
def init(sti: Annotated[Optional[Path], typer.Option()] = None):
