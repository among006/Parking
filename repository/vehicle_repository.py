from db.check_db import result
from db.database import get_connection

def find_one(id:int):
    db = get_connection()
    result = db.execute(f"select *  from vehicles where id = {id}")
    db.close()
    return result.fetchone()

def find_all():
    db = get_connection()
    result = db.execute("select *  from vehicles")
    db.close()
    return result.fetchall()

def create(plate_number: str, vehicle_type: str):
    db = get_connection()
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
