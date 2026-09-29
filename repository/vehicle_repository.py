from db.check_db import result
from db.database import get_connection

def find_one(id:int):
    with get_connection() as db:
        result = db.execute("select *  from vehicles where id = %s", (id,))
        db.close()
        return result.fetchone()

def find_all():
    with get_connection() as db:
        result = db.execute("select *  from vehicles")
        db.close()
        return result.fetchall()

def create(plate_number: str, vehicle_type: str):
    with get_connection() as db:
        result = db.execute(
            """
            insert into vehicles (plate_number, vehicle_type)
            values (%s, %s)
            RETURNING id, plate_number, vehicle_type
            """,
            (plate_number, vehicle_type),
        )
        db.commit()
        db.close()
        return result.fetchone()


def update(id: int, plate_number: str, vehicle_type: str):
    with get_connection() as db:
        result = db.execute(
            """
            update parking_spot
            set plate_number = %s,
                vehicle_type = %s
            where id = %s
            returning id, plate_number, vehicle_type
            """,
            (plate_number, vehicle_type, id),
        )
        return result.fetchone()

def delete(id: str):
    with get_connection() as db:
        result = db.execute(
            """
            delete from vehicles
                where id = %s
                returning id
            """,
            (id,)
        )
        db.commit()
        db.close()
        return result.fetchone()