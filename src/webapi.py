import os

from fastapi import FastAPI
import psycopg2

app = FastAPI()
db_username = os.environ["DB_USERNAME"]
db_password = os.environ["DB_PASSWORD"]

try:
    connection = psycopg2.connect(
        f"dbname='pgdatabase' user='{db_username}' host='localhost' password='{db_password}'"
    )

except:
    print("could not connect to the database")
    exit(1)


@app.get("/iris/{entry_id}")
def read_root(entry_id: int):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM iristable WHERE index = {entry_id};")
        result = cursor.fetchone()
    return result
