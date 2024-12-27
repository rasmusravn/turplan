import json
import os
from pathlib import Path
from typing import Annotated, Optional

import typer

from turplan.commands import aktivitet, deltager, lokation

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


@app.command("init")
def init(
    project_name: Optional[str] = typer.Argument(
        None, help="Navn på projektet/ turen."
    ),
):
    """
    Opretter en ny projektmappe (toplevel: 'turplan') til din tur.
    """
    if project_name is None:
        project_name = typer.prompt("Hvad skal projektet/turen hedde?")

    # Opret en mappe "turplan" i nuværende directory
    # Under "turplan" opret en ny mappe for hvert projekt
    top_level_dir = get_data_dir()
    project_dir = top_level_dir / Path(str(project_name))

    # Opret mapperne, hvis de ikke allerede findes
    project_dir.mkdir(parents=True, exist_ok=True)

    typer.echo(f"Dit projekt/tur '{project_name}' er nu oprettet i: {project_dir}")

    # Her kunne du gemme projekt-specifik data i en JSON-fil inde i project_dir
    # fx:
    project_config_path = project_dir / "project.json"
    project_data = {
        "name": project_name
        # Tilføj hvad du vil af data...
    }
    with open(project_config_path, "w", encoding="utf-8") as f:
        json.dump(project_data, f, indent=4, ensure_ascii=False)
    typer.echo(f"Projektdata gemt i {project_config_path}")


app = typer.Typer()

# Registrér underkommandoer
app.command("tilføj deltager")(deltager.tilfoej_deltager)
app.command("tilføj aktivitet")(aktivitet.tilfoej_aktivitet)
app.command("tilføj lokation")(lokation.tilfoej_lokation)

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
