from db.database import get_connection


def create_parking(spot_number: str,spot_type: str):
    db = get_connection()
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
    db = get_connection()
    result = db.execute("select *  from parking_spot")
    db.close()
    return result.fetchall()


def find_one(id:int):
    db = get_connection()
    result = db.execute(f"select *  from parking_spot where id = {id}")
    db.close()
    return result.fetchone()