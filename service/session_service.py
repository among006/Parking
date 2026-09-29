from datetime import datetime, timezone
from math import ceil

from fastapi import HTTPException

from db.database import get_connection
from dto import ParkingSession
from dto.VehicleType import VehicleType
from repository import session_repository


def find_empty_spot(vehicle_type: VehicleType):
    with get_connection() as db:
        spots = db.execute(
            """
            select id from parking_spot
            where spot_type = %s
            order by id
            """,
            (vehicle_type.value,)
        ).fetchall()

        for spot in spots:
            result = session_repository.find_active_spot(db, spot["id"])
            if result is None:
                return spot["id"]

        return None


def find_free_spots():
    with get_connection() as db:
        return session_repository.find_free_spots(db)


def create_session(session: ParkingSession.ParkingSessionCreate):
    with get_connection() as db:
        vehicle = session_repository.find_vehicle(db, session.vehicle_id)

        if vehicle is None:
            raise HTTPException(
                status_code=404,
                detail="Нету такой машины"
            )

        spot = session_repository.find_spot(db, session.spot_id)

        if spot is None:
            raise HTTPException(
                status_code=404,
                detail="Нету такого места парковки"
            )

        if vehicle["vehicle_type"] != spot["spot_type"]:
            raise HTTPException(
                status_code=409,
                detail="Тип машины не подходит для этого места"
            )

        active_vehicle = session_repository.find_active_vehicle(
            db, session.vehicle_id
        )

        if active_vehicle is not None:
            raise HTTPException(
                status_code=409,
                detail="Машина уже находится на парковке"
            )

        active_spot = session_repository.find_active_spot(
            db, session.spot_id
        )

        if active_spot is not None:
            raise HTTPException(
                status_code=409,
                detail="Это место уже занято"
            )

        if vehicle["vehicle_type"] == VehicleType.CAR:
            hourly_rate = 100
        elif vehicle["vehicle_type"] == VehicleType.MOTORCYCLE:
            hourly_rate = 50
        elif vehicle["vehicle_type"] == VehicleType.TRUCK:
            hourly_rate = 150
        else:
            raise HTTPException(
                status_code=409,
                detail="Неизвестный тип машины"
            )

        result = session_repository.create_session(
            db,
            session.vehicle_id,
            session.spot_id,
            hourly_rate
        )

        return result


def update_session(vehicle_id: int):
    with get_connection() as db:
        vehicle = session_repository.find_vehicle(db, vehicle_id)

        if vehicle is None:
            raise HTTPException(
                status_code=404,
                detail="Нету такой машины"
            )

        session = session_repository.find_active_vehicle(db, vehicle_id)

        if session is None:
            raise HTTPException(
                status_code=409,
                detail="Эта машина сейчас не находится на парковке"
            )

        exited_at = datetime.now(timezone.utc)
        entered_at = session["entered_at"].astimezone(timezone.utc)

        seconds = (exited_at - entered_at).total_seconds()

        if seconds < 0:
            raise HTTPException(
                status_code=409,
                detail="Время выезда раньше времени въезда"
            )

        hours = ceil(seconds / 3600)

        if hours < 1:
            hours = 1

        total_price = hours * session["hourly_rate"]

        result = session_repository.update_session(
            db,
            session["id"],
            exited_at,
            total_price
        )

        if result is None:
            raise HTTPException(
                status_code=409,
                detail="Сессия уже закрыта"
            )

        return result