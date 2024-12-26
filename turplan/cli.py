from pathlib import Path
from typing import Annotated, Optional

import typer

app = typer.Typer()


@app.command()
def init(sti: Annotated[Optional[Path], typer.Option()] = "./"):
    typer.echo("Init called")


@app.command()
def tilføj(emne: Annotated[Optional[Path], typer.Option()] = None):
    typer.echo("Init called ")


@app.command()
def fjern(emne: Annotated[Optional[Path], typer.Option()] = None):
    typer.echo("Init called")
