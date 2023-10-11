import csv
import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

""" Создает таблицу с ингредиентами. """


conn = psycopg2.connect(
    user=os.getenv("POSTGRES_USER"),
    password=os.getenv("POSTGRES_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("POSTGRES_DB"),
)
cursor = conn.cursor()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS recipes_ingredient
      (id SERIAL PRIMARY KEY, name TEXT, measurement_unit TEXT)"""
)


with open(
    "/app/data/ingredients.csv",
    newline="",
    encoding="utf-8",
) as csvfile:
    # ...
    reader = csv.reader(csvfile, delimiter=",")
    next(reader)
    for row in reader:
        name = row[0]
        measurement_unit = row[1]
        cursor.execute(
            "INSERT INTO recipes_ingredient (name, measurement_unit) "
            "VALUES (%s, %s)",
            (name, measurement_unit),
        )

conn.commit()
conn.close()
