import io
import os

from urllib import request
import pandas as pd
from sqlalchemy import create_engine

db_username = os.environ['DB_USERNAME']
db_password = os.environ['DB_PASSWORD']

def main(url):
    df = None
    with request.urlopen(url) as response, io.StringIO() as buffer:
        buffer.write(response.read().decode("utf-8"))
        buffer.seek(0)
        df = pd.read_csv(buffer, sep=",")
        df["sepal_ratio"] = df["sepal_length"] / df["sepal_width"]
        df["petal_ratio"] = df["petal_length"] / df["petal_width"]
    print(df)
    engine = create_engine(
        f"postgresql://{db_username}:{db_password}@localhost/pgdatabase"
    )
    df.to_sql("iristable", engine)


main(
    "https://gist.githubusercontent.com/curran/a08a1080b88344b0c8a7/raw/0e7a9b0a5d22642a06d3d5b9bcbad9890c8ee534/iris.csv"
)
