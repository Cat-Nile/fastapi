import pytest

from model.creature import Creature
from error import Missing, Duplicate


from src.data import creature


@pytest.fixture
def sample() -> Creature:
    return Creature(
        name="yeti",
        country="CN",
        area="Himalayas",
        description="Harmless Himalayan",
        aka="Abominable Snowman",
    )


def test_create(sample):
    response = creature.create(sample)
    assert response == sample


def test_create_duplicate(sample):
    with pytest.raises(Duplicate):
        _ = creature.create(sample)


def test_get_one(sample):
    response = creature.get_one(sample.name)
    assert response == sample


def test_get_one_missing():
    with pytest.raises(Missing):
        _ = creature.get_one("boxturtle")
