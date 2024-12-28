import json
from pathlib import Path
from typing import Optional

import typer

from turplan.commons.system import get_data_dir


def config_init(
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
