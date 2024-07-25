from model.explorer import Explorer
import icecream as ic

_explorers: list = [
    Explorer(
        name="Claude Hande",
        country="FR",
        description="It's hard to meet when the full moon rises",
    ),
    Explorer(
        name="Noah Weiser",
        country="DE",
        description="He has poor eyesight and carries a machete.",
    ),
]


def get_all() -> list[Explorer]:
    return _explorers


def get_one(name: str) -> Explorer:
    for _explorer in _explorers:
        if _explorer.name == name:
            return _explorer
    return None


def create(explorer: Explorer) -> Explorer:
    return explorer


def modify(name: str, explorer: Explorer) -> Explorer:
    return explorer


def replace(name: str, explorer: Explorer) -> Explorer:
    return explorer


def delete(name: str) -> bool:
    for _explorer in _explorers:
        if _explorer.name == name:
            return True
    return False
