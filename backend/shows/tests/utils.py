from typing import Union, Dict, List

from faker import Faker

from common.exceptions import WrongUsage


def fake_show_name(faker: Faker) -> str:
    """Generate fake show name"""
    return " ".join(faker.words(nb=3))


def fake_show_data(faker: Faker, count: int = 1) -> Union[Dict, List[Dict]]:
    """Generate fake show data used to populate Show model"""

    if count < 1:
        raise WrongUsage("Count must be at least 1")

    data = [
        {
            "name": fake_show_name(faker),
            "date": faker.date_object(),
            "address": faker.address(),
            "lions": faker.random_int(min=0, max=5),
        }
        for _ in range(count)
    ]
    return data[0] if count == 1 else data


def fake_round_data(faker: Faker, count: int = 1) -> Union[Dict, List[Dict]]:
    """Generate fake show round data used to populate Round model"""

    if count < 1:
        raise WrongUsage("Count must be at least 1")

    data = [{"time": faker.time_object()} for _ in range(count)]
    return data[0] if count == 1 else data
