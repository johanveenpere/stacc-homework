import os

from fastapi import FastAPI, HTTPException
import psycopg2
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()
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
def get_item(entry_id: int):
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM iristable WHERE index = {entry_id};")
        result = cursor.fetchone()
    return result


def parse_condition(condition: str):
    operator = condition[:2]
    value = condition[2:]

    condition_string = ""
    match operator:
        case "lt":
            condition_string += "<"
        case "le":
            condition_string += "<="
        case "eq":
            condition_string += "="
        case "gt":
            condition_string += ">"
        case "ge":
            condition_string += ">="
        case "ne":
            condition_string += "!="
        case _:
            raise ValueError

    condition_string += str(float(value))
    return condition_string


type optional_condition = str | None


@app.get("/irises")
def get_all_with_condition(
    sepal_length: optional_condition = None,
    sepal_width: optional_condition = None,
    petal_length: optional_condition = None,
    petal_width: optional_condition = None,
    species: optional_condition = None,
    sepal_ratio: optional_condition = None,
    petal_ratio: optional_condition = None,
):
    sql_conditions = []

    query = "SELECT * FROM iristable"
    if (
        sepal_length
        or sepal_width
        or petal_length
        or petal_width
        or species
        or sepal_ratio
        or petal_ratio
    ):
        query += " WHERE "
        try:
            if sepal_length:
                sql_conditions.append(f"sepal_length {parse_condition(sepal_length)}")
            if sepal_width:
                sql_conditions.append(f"sepal_width {parse_condition(sepal_width)}")
            if petal_length:
                sql_conditions.append(f"petal_length {parse_condition(petal_length)}")
            if petal_width:
                sql_conditions.append(f"petal_width {parse_condition(petal_width)}")
            if species:
                sql_conditions.append(f"species = '{species}'")
            if sepal_ratio:
                sql_conditions.append(f"sepal_ratio {parse_condition(sepal_ratio)}")
            if petal_ratio:
                sql_conditions.append(f"petal_ratio {parse_condition(petal_ratio)}")
        except:
            raise HTTPException(status_code=400)
        query += " " + " AND ".join(sql_conditions)
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result
