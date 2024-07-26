from data import cursor, IntegrityError

from model.explorer import Explorer
from error import Missing, Duplicate


cursor.execute(
    "create table if not exists explorer(name text primary key, country text, description text)"
)


def row_to_model(row: tuple) -> Explorer:
    name, country, description = row[0], row[1], row[2]
    return Explorer(name=name, country=country, description=description)


def model_to_dict(explorer: Explorer) -> dict | None:
    if explorer:
        return explorer.model_dump()
    else:
        return None


def get_one(name: str) -> Explorer:
    query = "select * from explorer where name=:name"
    params = {"name": name}
    cursor.execute(query, params)
    row = cursor.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(msg=f"Explorer {name} not found.")


def get_all() -> list[Explorer]:
    query = "select * from explorer"
    cursor.execute(query)
    rows = cursor.fetchall()
    return [row_to_model(row) for row in rows]


def create(explorer: Explorer) -> Explorer:
    query = "insert into explorer (name, country, description) values (:name, :country, :description)"
    params = model_to_dict(explorer)
    try:
        cursor.execute(query, params)
        # cursor.connection.commit()
    except IntegrityError:
        raise Duplicate(msg=f"Explorer {explorer.name} already exists.")

    return get_one(explorer.name)


def modify(name: str, explorer: Explorer) -> Explorer:
    if not (name and explorer):
        return None
    query = "update explorer set country=:country, name=:name, description=:description where name=:name_orig"
    params = model_to_dict(explorer)
    params["name_orig"] = explorer.name
    cursor.execute(query, params)
    if cursor.rowcount == 1:
        modified = get_one(explorer.name)
        return modified
    else:
        raise Missing(msg=f"Explorer {name} not found.")


def delete(name: str):
    if not name:
        return False
    query = "delete from explorer where name=:name"
    params = {"name": name}
    cursor.executue(query, params)
    if cursor.rowcount != 1:
        raise Missing(msg=f"Explorer {name} not found.")
