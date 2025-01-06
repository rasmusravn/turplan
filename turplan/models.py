from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class ParticipantModel(BaseModel):
    name: str
    email: EmailStr
    start_time: datetime
    end_time: datetime
    contacts: List[str] = []
    allergies: str
    is_leader: bool = False
    responsibilities: List[str] = []


class ActivityModel(BaseModel):
    name: str
    date: datetime
    description: Optional[str] = None
    participants: Optional[List[str]] = []


class LocationModel(BaseModel):
    name: str
    address: str
    capacity: Optional[int] = None
    facilities: Optional[List[str]] = []


class TripModel(BaseModel):
    name: str
    start_time: datetime
    end_time: datetime
    description: str
    organizer: str
    max_participants: int
    participants: List[str] = []
    activities: List[str] = []
    locations: List[str] = []
