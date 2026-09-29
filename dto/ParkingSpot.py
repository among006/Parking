from enum import Enum

from pydantic import BaseModel, Field, ConfigDict


class ParkingType(str, Enum):
    CAR = "CAR"
    MOTORCYCLE = "MOTORCYCLE"
    TRUCK = "TRUCK"


class ParkingCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    spot_number: str = Field(min_length=1, max_length=20)
    spot_type: ParkingType

class ParkingResponse(ParkingCreate):
    id: int
