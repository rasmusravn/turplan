import os
from pathlib import Path
from typing import Annotated, Optional

import typer

from turplan.commands.add import activity, location, participant
from turplan.commands.config import init

APP_NAME = "turplan"
app_dir = typer.get_app_dir(APP_NAME)
config_path: Path = Path(app_dir) / "config.json"

app = typer.Typer(
    no_args_is_help=True,
    help="""
    Et CLI-værktøj til at planlæggeture, \n
    """,
)


@app.command("indlæs")
def load_trip(trip: Annotated[str, typer.Argument(help="Tur som skal indlæses")] = ""):
    "Indlæser tur til som værktøjet skal arbejde med"
    if trip == "":
        data_path = get_data_dir()
        for item in os.listdir(data_path):
            full_path = os.path.join(data_path, item)
            if os.path.isdir(full_path):
                print(item)
    else:
        typer.echo(f"Indlæser ̈́{trip}")


app.command("config init")(init.config_init)
# Registrér underkommandoer
app.command("tilføj deltager")(participant.add_participant)
app.command("tilføj aktivitet")(activity.add_activity)
app.command("tilføj lokation")(location.add_location)

if __name__ == "__main__":
    app()


@app.command()
def fjern(emne: Annotated[Optional[Path], typer.Option()] = None):
    typer.echo("Init called")


@app.command()
def config():
    if not config_path.is_file():
        config_file_obj = Path(config_path)
        config_file_obj.touch(exist_ok=True)
        typer.echo(f"Konifgurereringsfil oprettet her:\n {config_file_obj}")


@app.command()
def pakkeliste():
    typer.echo("Her er en pakkeliste")
