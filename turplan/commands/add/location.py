from typing import List, Optional

import typer
from pydantic import ValidationError

from turplan.models.models import LocationModel


def add_location(
    name: str = typer.Option(..., help="Navnet på lokationen"),
    address: str = typer.Option(..., help="Adressen på lokationen"),
    capacity: Optional[int] = typer.Option(None, help="Kapaciteten af lokationen"),
    facilities: Optional[List[str]] = typer.Option(
        None, help="Faciliteter på lokationen"
    ),
):
    """
    Tilføj en lokation til turplanen.
    """
    try:
        location = LocationModel(
            name=name,
            address=address,
            capacity=capacity,
            facilities=facilities or [],
        )
        typer.echo(f"Lokation oprettet: {location.json(indent=4)}")
    except ValidationError as e:
        typer.echo(f"Valideringsfejl:\n{e}", err=True)
