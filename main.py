
from fastapi import FastAPI, HTTPException
from sqlalchemy import select

from db.check_db import result
from db.database import get_connection
from dto import ParkingSpot
from dto.VehicleType import VehicleCreate, VehicleResponse
from repository import parking_repository
from repository.vehicle_repository import find_all, find_one, create

app = FastAPI(title="Parking Among")


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/vehicle/{id}", response_model=VehicleResponse)
def get_vehicle(id: int):
    vehicle = find_one(id)
    print(vehicle)
    if vehicle is None:
        raise HTTPException(status_code=404,
                            detail="Нету такой машины",)

    return find_one(id)

@app.get("/vehicles", response_model=list[VehicleResponse])
def get_all_vehicles():
    return find_all()

@app.post("/vehicles", response_model=VehicleResponse, status_code=201)
def create_vehicle(vehicle: VehicleCreate):
    return create(plate_number=vehicle.plate_number, vehicle_type=vehicle.vehicle_type)


@app.post("/spots", response_model=ParkingSpot.ParkingResponse, status_code=201)
def create_parking(parking_create: ParkingSpot.ParkingCreate):
    print(parking_create)
    return parking_repository.create_parking(spot_number=parking_create.spot_number, spot_type=parking_create.spot_type)

@app.get("/spots", response_model=list[ParkingSpot.ParkingResponse])
def get_all_spots():
    return parking_repository.find_all()


@app.get("/spot/{id}", response_model=ParkingSpot.ParkingResponse)
def get_spot(id: int):
    spot = parking_repository.find_one(id)
    print(spot)
    if spot is None:
        raise HTTPException(status_code=404,
                            detail="Нету такого места парковки",)

    return spot
