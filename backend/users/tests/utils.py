from typing import Union, Dict, List

from faker import Faker


def fake_user_data(faker: Faker, count: int = 1) -> Union[Dict, List[Dict]]:
    """Generate fake user data used to populate User model"""
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
