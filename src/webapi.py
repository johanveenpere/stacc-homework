import os

from fastapi import FastAPI, HTTPException
import psycopg2
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()
pg_username = os.environ["PG_USERNAME"]
pg_password = os.environ["PG_PASSWORD"]
pg_hostname = os.environ["PG_HOSTNAME"]
pg_database_name = os.environ["PG_DATABASE_NAME"]

try:
    connection = psycopg2.connect(
        f"dbname='{pg_database_name}' user='{pg_username}' host='{pg_hostname}' password='{pg_password}'"
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


@app.get(
    "/irises",
    summary="Get all entries in the database.",
    description="""Get all entries in the database matching all supplied conditions. The condition for species is the species name. For other parameters the condition is in the form (operator)(float) where the operators are: lt - less than, le - less than or equal, eq - equal, gt - greater than, ge - greater than or equal, ne - not equal. For example, the condition "le6.0" means <=6.0""",
)
def get_all_with_condition(
    sepal_length: str = None,
    sepal_width: str = None,
    petal_length: str = None,
    petal_width: str = None,
    species: str = None,
    sepal_ratio: str = None,
    petal_ratio: str = None,
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
