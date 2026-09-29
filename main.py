
from fastapi import FastAPI, HTTPException
from psycopg.errors import UniqueViolation

from dto import ParkingSpot
from dto.VehicleType import VehicleCreate, VehicleResponse
from repository import parking_repository, vehicle_repository
from repository.vehicle_repository import find_all, find_one, create

app = FastAPI(title="Parking Among")


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/vehicles/{id}", response_model=VehicleResponse)
def get_vehicle(id: int):
    vehicle = find_one(id)
    print(vehicle)
    if vehicle is None:
        raise HTTPException(status_code=404,
                            detail="Нету такой машины",)

    return vehicle
@app.put("/vehicles/{id}")
def update_vehicle(id: int, vehicle: VehicleCreate):
    try:
        updated_vehicle = vehicle_repository.update(id=id, plate_number=vehicle.plate_number, vehicle_type=vehicle.vehicle_type.value)
    except UniqueViolation:
        raise HTTPException(status_code=409, detail="Транспорт с таким номером уже существует",)
    if updated_vehicle is None:
        raise HTTPException(status_code=404, detail="Такого транспорта не существует")
    return updated_vehicle
@app.get("/vehicles", response_model=list[VehicleResponse])
def get_all_vehicles():
    return find_all()

@app.post("/vehicles", response_model=VehicleResponse, status_code=201)
def create_vehicle(vehicle: VehicleCreate):
    return create(plate_number=vehicle.plate_number, vehicle_type=vehicle.vehicle_type)

@app.delete("/vehicles/{id}")
def delete_vehicle(id: int):
    return vehicle_repository.delete(id=id)

@app.post("/spots", response_model=ParkingSpot.ParkingResponse, status_code=201)
def create_parking(parking_create: ParkingSpot.ParkingCreate):
    print(parking_create)
    return parking_repository.create_parking(spot_number=parking_create.spot_number, spot_type=parking_create.spot_type)

@app.get("/spots", response_model=list[ParkingSpot.ParkingResponse])
def get_all_spots():
    return parking_repository.find_all()


@app.put("/spots/{id}")
def update_spot(id: int, spot: ParkingSpot.ParkingCreate):
    try:
        updated_spot = parking_repository.update(id=id, spot_number=spot.spot_number, spot_type=spot.spot_type.value)
    except UniqueViolation:
        raise HTTPException(status_code=409, detail="Место с таким номером уже существует",)
    if updated_spot is None:
        raise HTTPException(status_code=404, detail="Такого места не существует")
    return updated_spot

@app.get("/spots/{id}", response_model=ParkingSpot.ParkingResponse)
def get_spot(id: int):
    spot = parking_repository.find_one(id)
    print(spot)
    if spot is None:
        raise HTTPException(status_code=404,
                            detail="Нету такого места парковки",)

    return spot

@app.delete("/spots/{id}")
def delete_spot(id: int):
    return parking_repository.delete(id=id)