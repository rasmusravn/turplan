from datetime import datetime
from typing import List, Optional

import typer
from pydantic import ValidationError

from turplan.models.models import ActivityModel, LocationModel, ParticipantModel


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
        typer.echo(f"Deltager oprettet: {participant.model_dump_json(indent=4)}")
    except ValidationError as e:
        typer.echo(f"Valideringsfejl:\n{e}", err=True)


def add_activity(
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
        typer.echo(f"Aktivitet oprettet: {activity.model_dump_json(indent=4)}")
    except ValidationError as e:
        typer.echo(f"Valideringsfejl:\n{e}", err=True)


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
        typer.echo(f"Lokation oprettet: {location.model_dump_json(indent=4)}")
    except ValidationError as e:
        typer.echo(f"Valideringsfejl:\n{e}", err=True)
