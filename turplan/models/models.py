from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr


class ParticipantModel(BaseModel):
    name: str
    email: EmailStr
    contacts: Optional[List[str]] = []
    allergies: Optional[str] = None
    days: List[datetime]
    is_leader: bool = False
    leader_role: Optional[str] = None
    responsibilities: Optional[List[str]] = []


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
