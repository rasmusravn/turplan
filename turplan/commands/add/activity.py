from datetime import datetime
from typing import List, Optional

import typer
from pydantic import ValidationError

from turplan.models.models import ActivityModel


def tilfoej_aktivitet(
    name: str = typer.Option(..., help="Navnet på aktiviteten"),
    date: str = typer.Option(..., help="Dato for aktiviteten (YYYY-MM-DD)"),
    description: Optional[str] = typer.Option(None, help="Beskrivelse af aktiviteten"),
    participants: Optional[List[str]] = typer.Option(
        None, help="Deltagere i aktiviteten"
    ),
):
    """
    Tilføj en aktivitet til turplanen.
    """
    try:
        activity = ActivityModel(
            name=name,
            date=datetime.strptime(date, "%Y-%m-%d"),
            description=description,
            participants=participants or [],
        )
        typer.echo(f"Aktivitet oprettet: {activity.json(indent=4)}")
    except ValidationError as e:
        typer.echo(f"Valideringsfejl:\n{e}", err=True)
