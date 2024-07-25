from model.creature import Creature

_creatures = [
    Creature(
        name="Yeti",
        aka="Abominable Snowman",
        country="CN",
        area="Himalayas",
        description="Hirsute Himalayan",
    ),
    Creature(
        name="Big foot",
        country="US",
        area="*",
        aka="Sasquatch",
        description="Yeti's cousin Eddie",
    ),
]


def get_all() -> list[Creature]:
    return _creatures


def get_one(name: str) -> Creature | None:
    for _creature in _creatures:
        if _creature.name == name:
            return _creature
    return None


def create(creature: Creature) -> Creature:
    return creature


def modify(name: str, creature: Creature) -> Creature:
    return creature


def replace(name: str, creature: Creature) -> Creature:
    return creature


def delete(name: str) -> bool:
    for _creature in _creatures:
        if _creature.name == name:
            return True
    return None
