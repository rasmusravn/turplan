from datetime import datetime
from typing import List
import json

import typer
from pydantic import ValidationError, BaseModel, EmailStr

from turplan.models import ActivityModel, ParticipantModel, TripModel

app = typer.Typer()


@app.command()
def add_trip():
    """
    Tilføj en ny tur med grundlæggende information.
    """
    name = typer.prompt("Indtast turens navn")
    
    # Start dato og tid - separeret input
    start_date = typer.prompt("Indtast turens startdato (YYYY-MM-DD)")
    start_time = typer.prompt("Indtast turens starttidspunkt (HH:MM)", default="00:00")
    start_datetime = f"{start_date} {start_time}"
    
    # Slut dato og tid - separeret input
    end_date = typer.prompt("Indtast turens slutdato (YYYY-MM-DD)")
    end_time = typer.prompt("Indtast turens sluttidspunkt (HH:MM)", default="00:00")
    end_datetime = f"{end_date} {end_time}"
    
    description = typer.prompt("Indtast beskrivelse af turen")
    organizer = typer.prompt("Indtast arrangørens navn")
    max_participants = typer.prompt("Indtast maksimalt antal deltagere", type=int)
    
    try:
        trip = TripModel(
            name=name,
            start_time=datetime.strptime(start_datetime, "%Y-%m-%d %H:%M"),
            end_time=datetime.strptime(end_datetime, "%Y-%m-%d %H:%M"),
            description=description,
            organizer=organizer,
            max_participants=max_participants,
            participants=[],
            activities=[],
            locations=[]
        )
        
        # Gem turen i JSON-fil
        trips = load_trips()
        trips.append(trip.model_dump())
        save_trips(trips)
        
        typer.echo(f"Tur oprettet successfully:")
        typer.echo(f"Navn: {trip.name}")
        typer.echo(f"Start: {trip.start_time}")
        typer.echo(f"Slut: {trip.end_time}")
        typer.echo(f"Arrangør: {trip.organizer}")
        typer.echo(f"Max deltagere: {trip.max_participants}")
        
    except ValidationError as e:
        typer.echo(f"Valideringsfejl:\n{e}", err=True)

def load_trips() -> List[dict]:
    """
    Indlæs eksisterende ture fra JSON-fil.
    """
    def fix_time_format(time_str: str) -> str:
        """Hjælpefunktion til at formatere tidspunkter korrekt"""
        # Fjern sekunder hvis de findes
        if ':00' in time_str:
            time_str = time_str.rsplit(':00', 1)[0]
        
        # Split dato og tid
        date_part, time_part = time_str.split(' ')
        
        # Hvis tiden kun er timer (f.eks. "16"), tilføj ":00"
        if ':' not in time_part:
            time_part = f"{time_part}:00"
            
        return f"{date_part} {time_part}"

    try:
        with open("trips.json", "r") as f:
            trips = json.load(f)
            for trip in trips:
                # Håndter tur datoer
                trip['start_time'] = datetime.strptime(
                    fix_time_format(trip['start_time']), 
                    "%Y-%m-%d %H:%M"
                )
                trip['end_time'] = datetime.strptime(
                    fix_time_format(trip['end_time']), 
                    "%Y-%m-%d %H:%M"
                )
                
                # Håndter deltager datoer
                if 'participants' in trip:
                    for participant in trip['participants']:
                        participant['start_time'] = datetime.strptime(
                            fix_time_format(participant['start_time']), 
                            "%Y-%m-%d %H:%M"
                        )
                        participant['end_time'] = datetime.strptime(
                            fix_time_format(participant['end_time']), 
                            "%Y-%m-%d %H:%M"
                        )
            return trips
    except FileNotFoundError:
        return []

def save_trips(trips: List[dict]):
    """
    Gem ture til JSON-fil med korrekt datohåndtering.
    """
    def datetime_handler(obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M")  # Gem uden sekunder
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    with open("trips.json", "w") as f:
        json.dump(trips, f, indent=4, default=datetime_handler)


class ParticipantInput(BaseModel):
    """Model til validering af deltager input"""
    name: str
    email: str  # Vi bruger str her og validerer email-formatet selv
    start_time: datetime
    end_time: datetime
    contacts: List[str]
    allergies: str
    is_leader: bool
    responsibilities: List[str]

    @property
    def email_address(self) -> EmailStr:
        """Validerer email-formatet"""
        return EmailStr(self.email)

@app.command()
def add_participant():
    """
    Tilføj en deltager til en specifik tur.
    """
    # Vis og vælg tur
    trips = load_trips()
    if not trips:
        typer.echo("Ingen ture findes. Opret venligst en tur først.")
        return
    
    typer.echo("\nEksisterende ture:")
    for idx, trip in enumerate(trips):
        typer.echo(f"{idx + 1}. {trip['name']} ({trip['start_time']} - {trip['end_time']})")
    
    trip_idx = typer.prompt("Vælg tur nummer", type=int) - 1
    if trip_idx < 0 or trip_idx >= len(trips):
        typer.echo("Ugyldigt tur nummer")
        return
    
    selected_trip = trips[trip_idx]
    
    # Indsaml deltager information
    while True:
        try:
            # Basis information
            name = typer.prompt("Indtast deltagerens navn")
            
            # Email med validering
            while True:
                try:
                    email = typer.prompt(f"Indtast {name}'s email")
                    # Test email validering med en midlertidig model
                    ParticipantModel(
                        name=name,
                        email=email,
                        start_time=datetime.now(),  # Midlertidig værdi
                        end_time=datetime.now(),    # Midlertidig værdi
                        allergies="temp"
                    )
                    break
                except ValidationError as e:
                    typer.echo("Ugyldig email-adresse")
                    if not typer.confirm("Vil du prøve igen?"):
                        return
            
            # Datoer
            start_date = typer.prompt(f"Indtast {name}'s startdato (YYYY-MM-DD)")
            start_time = typer.prompt(f"Indtast {name}'s starttidspunkt (HH:MM)", default="00:00")
            start_datetime = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
            
            end_date = typer.prompt(f"Indtast {name}'s slutdato (YYYY-MM-DD)")
            end_time = typer.prompt(f"Indtast {name}'s sluttidspunkt (HH:MM)", default="00:00")
            end_datetime = datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M")
            
            # Øvrig information
            contacts = typer.prompt(f"Indtast {name}'s nære kontakter")
            allergies = typer.prompt("Indtast evt. allergier, ellers bare skriv 'ingen'")
            is_leader = typer.prompt(f"Er {name} leder? (ja/nej)").lower() == 'ja'
            responsibilities = typer.prompt("Indtast særlige ansvarsområder")

            # Opret og validér den komplette deltager
            participant = ParticipantModel(
                name=name,
                email=email,
                start_time=start_datetime,
                end_time=end_datetime,
                contacts=contacts.split(',') if ',' in contacts else [contacts] if contacts else [],
                allergies=allergies,
                is_leader=is_leader,
                responsibilities=responsibilities.split(',') if ',' in responsibilities else [responsibilities] if responsibilities else []
            )
            
            # Gem deltageren
            if 'participants' not in selected_trip:
                selected_trip['participants'] = []
            
            selected_trip['participants'].append(participant.model_dump())
            save_trips(trips)
            
            typer.echo(f"\nDeltager {name} er blevet tilføjet til turen '{selected_trip['name']}'")
            break
            
        except ValidationError as e:
            typer.echo(f"Valideringsfejl:\n{e}")
            if not typer.confirm("Vil du prøve igen?"):
                return
        except ValueError as e:
            typer.echo(f"Ugyldig værdi: {e}")
            if not typer.confirm("Vil du prøve igen?"):
                return

@app.command()
def add_activity():
    """
    Tilføj en aktivitet til turplanen.
    """
    name = typer.prompt("Indtast aktivitetens navn")
    date = typer.prompt("Indtast dato og tidspunkt (YYYY-MM-DD HH:MM)")
    description = typer.prompt("Indtast beskrivelse af aktiviteten")
    participants = typer.prompt("Indtast deltagere (adskilt med komma)")
    
    try:
        activity = ActivityModel(
            name=name,
            date=datetime.strptime(date, "%Y-%m-%d %H:%M"),
            description=description,
            participants=[p.strip() for p in participants.split(",")] if participants else []
        )
        typer.echo(f"Aktivitet oprettet: {activity.model_dump_json(indent=4)}")
    except ValidationError as e:
        typer.echo(f"Valideringsfejl:\n{e}", err=True)


@app.command()
def add_location():
    """
    Tilføj en lokation til turplanen.
    """
    name = typer.prompt("Indtast lokations navn")
    address = typer.prompt("Indtast lokations adresse")
    capacity = typer.prompt("Indtast lokations kapacitet")
    facilities = typer.prompt("Indtast lokations faciliteter")

    try:
        location = LocationModel(
            name=name,
            address=address,
            capacity=capacity,
            facilities=facilities
        )
        typer.echo(f"Lokation oprettet: {location.model_dump_json(indent=4)}")
    except ValidationError as e:
        typer.echo(f"Valideringsfejl:\n{e}", err=True)