from enum import Enum

from pydantic import BaseModel, Field, ConfigDict


class VehicleType(str, Enum):
    CAR = "CAR"
    MOTORCYCLE = "MOTORCYCLE"
    TRUCK = "TRUCK"

class VehicleCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace = True)

    plate_number: str = Field(min_length=1, max_length=20)
    vehicle_type: VehicleType

class VehicleResponse(VehicleCreate):
    id: int