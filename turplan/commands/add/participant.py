from datetime import datetime
from typing import List, Optional

import typer
from pydantic import ValidationError

from turplan.models.models import ParticipantModel


def add_participant(
    name: str = typer.Option(..., help="Navnet på deltageren"),
    email: str = typer.Option(..., help="Email-adressen på deltageren"),
    contacts: Optional[List[str]] = typer.Option(None, help="Kontaktpersoner"),
    allergies: Optional[str] = typer.Option(None, help="Allergier"),
    days: List[str] = typer.Option(..., help="Dage for deltagelse (YYYY-MM-DD)"),
    is_leader: bool = typer.Option(False, help="Er deltageren en leder?"),
    leader_role: Optional[str] = typer.Option(None, help="Lederens rolle"),
    responsibilities: Optional[List[str]] = typer.Option(None, help="Lederens ansvar"),
):
    """
    Tilføj en deltager til turplanen.
    """
    try:
        participant = ParticipantModel(
            name=name,
            email=email,
            contacts=contacts or [],
            allergies=allergies,
            days=[datetime.strptime(day, "%Y-%m-%d") for day in days],
            is_leader=is_leader,
            leader_role=leader_role,
            responsibilities=responsibilities or [],
        )
        typer.echo(f"Deltager oprettet: {participant.json(indent=4)}")
    except ValidationError as e:
        typer.echo(f"Valideringsfejl:\n{e}", err=True)
