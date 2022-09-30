from typing import Union, Dict, List

from faker import Faker

from common.exceptions import WrongUsage


def fake_user_data(faker: Faker, count: int = 1) -> Union[Dict, List[Dict]]:
    """Generate fake user data used to populate User model"""

    if count < 1:
        raise WrongUsage("Count must be at least 1")

    data = [
        {
            "email": faker.email(),
            "password": faker.password(length=12),
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
        }
        for _ in range(count)
    ]
    return data[0] if count == 1 else data
