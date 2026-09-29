from fastapi import FastAPI, HTTPException
from psycopg.errors import UniqueViolation, ForeignKeyViolation

from dto import ParkingSpot
from dto.ParkingSession import ParkingSessionResponse, ParkingSessionCreate
from dto.VehicleType import VehicleCreate, VehicleResponse
from repository import parking_repository, vehicle_repository
from repository.vehicle_repository import find_all, find_one, create
from service import session_service

app = FastAPI(title="Parking Among")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/vehicles/{id}", response_model=VehicleResponse)
def get_vehicle(id: int):
    vehicle = find_one(id)

    if vehicle is None:
        raise HTTPException(
            status_code=404,
            detail="Нету такой машины"
        )

    return vehicle


@app.put("/vehicles/{id}", response_model=VehicleResponse)
def update_vehicle(id: int, vehicle: VehicleCreate):
    try:
        updated_vehicle = vehicle_repository.update(
            id=id,
            plate_number=vehicle.plate_number,
            vehicle_type=vehicle.vehicle_type.value
        )
    except UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="Транспорт с таким номером уже существует"
        )

    if updated_vehicle is None:
        raise HTTPException(
            status_code=404,
            detail="Такого транспорта не существует"
        )

    return updated_vehicle


@app.get("/vehicles", response_model=list[VehicleResponse])
def get_all_vehicles():
    return find_all()


@app.post("/vehicles", response_model=VehicleResponse, status_code=201)
def create_vehicle(vehicle: VehicleCreate):
    try:
        return create(
            plate_number=vehicle.plate_number,
            vehicle_type=vehicle.vehicle_type.value
        )
    except UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="Транспорт с таким номером уже существует"
        )


@app.delete("/vehicles/{id}")
def delete_vehicle(id: int):
    try:
        result = vehicle_repository.delete(id=id)
    except ForeignKeyViolation:
        raise HTTPException(
            status_code=409,
            detail="Нельзя удалить машину с историей парковок"
        )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Такого транспорта не существует"
        )

    return result


@app.post(
    "/spots",
    response_model=ParkingSpot.ParkingResponse,
    status_code=201
)
def create_parking(parking_create: ParkingSpot.ParkingCreate):
    try:
        return parking_repository.create_parking(
            spot_number=parking_create.spot_number,
            spot_type=parking_create.spot_type.value
        )
    except UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="Место с таким номером уже существует"
        )


@app.get("/spots", response_model=list[ParkingSpot.ParkingResponse])
def get_all_spots():
    return parking_repository.find_all()


@app.get("/spots/free", response_model=list[ParkingSpot.ParkingResponse])
def get_free_spots():
    return session_service.find_free_spots()


@app.put("/spots/{id}", response_model=ParkingSpot.ParkingResponse)
def update_spot(id: int, spot: ParkingSpot.ParkingCreate):
    try:
        updated_spot = parking_repository.update(
            id=id,
            spot_number=spot.spot_number,
            spot_type=spot.spot_type.value
        )
    except UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="Место с таким номером уже существует"
        )

    if updated_spot is None:
        raise HTTPException(
            status_code=404,
            detail="Такого места не существует"
        )

    return updated_spot


@app.get("/spots/{id}", response_model=ParkingSpot.ParkingResponse)
def get_spot(id: int):
    spot = parking_repository.find_one(id)

    if spot is None:
        raise HTTPException(
            status_code=404,
            detail="Нету такого места парковки"
        )

    return spot


@app.delete("/spots/{id}")
def delete_spot(id: int):
    try:
        result = parking_repository.delete(id=id)
    except ForeignKeyViolation:
        raise HTTPException(
            status_code=409,
            detail="Нельзя удалить место с историей парковок"
        )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Нету такого места парковки"
        )

    return result


@app.post(
    "/sessions/arrivl",
    response_model=ParkingSessionResponse,
    status_code=201
)
def create_session(session: ParkingSessionCreate):
    try:
        result = session_service.create_session(session)
    except UniqueViolation:
        raise HTTPException(
            status_code=409,
            detail="Машина или место уже заняты сессией"
        )

    return result


@app.post(
    "/sessions/leaving/{vehicle_id}",
    response_model=ParkingSessionResponse
)
def leave_session(vehicle_id: int):
    result = session_service.update_session(vehicle_id)
    return result