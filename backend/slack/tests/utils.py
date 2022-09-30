from typing import Optional, Union, List
from unittest.mock import patch

from django.test import TestCase
from faker import Faker

from common.exceptions import WrongUsage
from slack.service import SlackBoss


def fake_slack_id(
    faker: Optional[Faker] = None, count: int = 1, **kwargs
) -> Union[str, List[str]]:
    """Generate fake Slack IDs"""

    if count < 1:
        raise WrongUsage("Count must be at least 1")

    if faker is None:
        faker = Faker()
        Faker.seed(1234)

    ids = [
        faker.password(length=10, special_chars=False, lower_case=False)
        for _ in range(count)
    ]
    return ids[0] if count == 1 else ids


def fake_slack_token(faker: Optional[Faker] = None, **kwargs):
    if faker is None:
        faker = Faker()
        Faker.seed(1234)

    return faker.password(length=20, special_chars=False, lower_case=False)


def fake_slack_timestamp(faker: Optional[Faker] = None, **kwargs):
    if faker is None:
        faker = Faker()
        Faker.seed(1234)

    return f"{faker.unix_time()}.{faker.random_int()}"


class PatchSlackBossMixin(TestCase):
    def setUp(self):
        super().setUp()
        self._patch_fetch_user()

    def _patch_fetch_user(self):
        fetch_user_patcher = patch.object(
            SlackBoss, "fetch_user", side_effect=fake_slack_id
        )
        self.mock_fetch_user = fetch_user_patcher.start()
        self.addCleanup(fetch_user_patcher.stop)

        create_channel_patcher = patch.object(
            SlackBoss, "create_channel", side_effect=fake_slack_id
        )
        self.mock_create_channel = create_channel_patcher.start()
        self.addCleanup(create_channel_patcher.stop)
