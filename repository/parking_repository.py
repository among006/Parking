from db.database import get_connection


def create_parking(spot_number: str,spot_type: str):
    with get_connection() as db:
        result = db.execute(
            """
            insert into parking_spot(spot_number, spot_type) 
            values(%s, %s)
            returning id, spot_number, spot_type
            """,
            (spot_number, spot_type),
        )
        db.commit()
        db.close()
        return result.fetchone()

def find_all():
    with get_connection() as db:
        result = db.execute("select *  from parking_spot")
        db.close()
        return result.fetchall()

def update(id: int, spot_number: str, spot_type: str):
    with get_connection() as db:
        result = db.execute(
            """
            update parking_spot
            set spot_number = %s,
                spot_type = %s
            where id = %s
            returning id, spot_number, spot_type
            """,
            (spot_number, spot_type, id),
        )
        return result.fetchone()

def find_one(id:int):
    with get_connection() as db:
        result = db.execute("select *  from parking_spot where id = %s",(id,))
        db.close()
        return result.fetchone()


def delete(id: str):
    with get_connection() as db:
        result = db.execute(
            """
            delete from parking_spot
                where id = %s
                returning id
            """,
            (id,)
        )
        db.commit()
        db.close()
        return result.fetchone()