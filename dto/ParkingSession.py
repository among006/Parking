from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class ParkingSessionCreate(BaseModel):
    vehicle_id: int = Field(gt=0)
    spot_id: int = Field(gt=0)

class ParkingSessionResponse(BaseModel):
    id: int
    vehicle_id: int
    spot_id: int
    entered_at: datetime
    exited_at: datetime | None
    hourly_rate: Decimal
    total_price: Decimal | None

