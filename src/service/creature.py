# import fake.creature as data
import data.creature as data


from model.creature import Creature


def get_all() -> list[Creature]:
    return data.get_all()

def get_one(name: str) -> Creature | None:
    return data.get_one(name)

def create(creature: Creature) -> Creature:
    return data.create(creature)

def replace(name: str, creature: Creature) -> Creature:
    return data.replace(name, creature)

def modify(name: str, creature: Creature) -> Creature:
    return data.modify(name, creature)

def delete(name: str) -> bool:
    return data.delete(name)

"""
stmt = '''
    select * from creature where name=:name or country=:country
'''
params = {"name": "yeti", "country": "CN"}

curs.execute(stmt, params)
"""
