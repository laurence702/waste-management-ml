from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from enum import Enum

class WasteType(str, Enum):
    RECYCLABLE = "recyclable"
    ORGANIC = "organic"
    GENERAL = "general"
    HAZARDOUS = "hazardous"

class Area(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    code: str = Field(index=True, unique=True)
    description: Optional[str] = None
    population_density: Optional[float] = None

class WasteLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    area_id: int = Field(foreign_key="area.id")
    collection_date: datetime = Field(default_factory=datetime.utcnow)
    waste_type: WasteType
    weight_kg: float
    truck_id: Optional[str] = None
