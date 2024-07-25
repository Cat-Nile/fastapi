import sqlite3

from model.creature import Creature

DB_NAME = "cryptid.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

def __init__():
    cursor.execute("create table creature(name, description, country, area, aka")

def row_to_model(row: tuple) -> Creature:
    name, description, country, area, aka = row
    return Creature(
        name=name,
        description=description,
        country=country,
        area=area,
        aka=aka,
    )

def model_to_dict(creature: Creature) -> dict:
    return creature.model_dumpt()


def get_one(name: str) -> Creature:
    query = "select * from creature where name=:name"
    params = {"name": name}
    cursor.execute(query, params)
    row = cursor.fetchone()
    return row_to_model(row)


def get_all() -> list[Creature]:
    query = "select * from creature"
    cursor.execute(query)
    rows = list(cursor.fetchall())
    return [row_to_model(row) for row in rows]

def create(creature: Creature):
    query = "insert into creature values (:name, :description, :country, :area, :aka)"
    params = model_to_dict(creature)
    cursor.execute(query, params)

def modify(creature: Creature):
    return creature

def replace(creature: Creature):
    return creature

def delete(creature: Creature):
    query = "delete from creature where name=:name"
    params = {"name": creature.name}
    cursor.execute(query, params)
