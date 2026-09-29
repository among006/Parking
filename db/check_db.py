from db.database import get_connection

with get_connection() as connection:
    proverka = connection.execute("select * from vehicles")
    result = proverka.fetchall()
    for i in result:
        print(i)