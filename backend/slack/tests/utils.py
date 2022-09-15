from unittest.mock import patch

from django.test import TestCase
from faker import Faker

from slack.service import SlackBoss


def slack_id_faker(faker=None):
    if faker is None:
        faker = Faker()
        Faker.seed(1234)

    def func(*args, **kwargs):
        return faker.password(length=10, special_chars=False, lower_case=False)

    return func


class PatchSlackBossMixin(TestCase):
    def setUp(self):
        super().setUp()
        self._patch_fetch_user()

    def _patch_fetch_user(self):
        patcher = patch.object(SlackBoss, "fetch_user", side_effect=slack_id_faker())
        self.mock_fetch_user = patcher.start()
        self.addCleanup(patcher.stop)
