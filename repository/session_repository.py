def find_vehicle(db, vehicle_id: int):
    result = db.execute(
        """
        select * from vehicles where id = %s for update
        """,
        (vehicle_id,)
    )
    return result.fetchone()


def find_spot(db, spot_id: int):
    result = db.execute(
        """
        select * from parking_spot where id = %s for update
        """,
        (spot_id,)
    )
    return result.fetchone()


def find_active_vehicle(db, vehicle_id: int):
    result = db.execute(
        """
        select * from parking_session
        where vehicle_id = %s and exited_at is null
        for update
        """,
        (vehicle_id,)
    )
    return result.fetchone()


def find_active_spot(db, spot_id: int):
    result = db.execute(
        """
        select id from parking_session
        where spot_id = %s and exited_at is null
        """,
        (spot_id,)
    )
    return result.fetchone()


def create_session(db, vehicle_id: int, spot_id: int, hourly_rate):
    result = db.execute(
        """
        insert into parking_session (vehicle_id, spot_id, hourly_rate)
        values (%s, %s, %s)
        returning id, vehicle_id, spot_id, entered_at,
                  exited_at, hourly_rate, total_price
        """,
        (vehicle_id, spot_id, hourly_rate)
    )
    return result.fetchone()


def update_session(db, id: int, exited_at, total_price):
    result = db.execute(
        """
        update parking_session
        set exited_at = %s,
            total_price = %s
        where id = %s and exited_at is null
        returning id, vehicle_id, spot_id, entered_at,
                  exited_at, hourly_rate, total_price
        """,
        (exited_at, total_price, id)
    )
    return result.fetchone()


def find_free_spots(db):
    result = db.execute(
        """
        select id, spot_number, spot_type
        from parking_spot
        where not exists (
            select 1 from parking_session
            where parking_session.spot_id = parking_spot.id
              and exited_at is null
        )
        """
    )
    return result.fetchall()