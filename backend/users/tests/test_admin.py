from unittest.mock import patch

from django.contrib.admin import AdminSite
from django.test import TestCase
from faker import Faker

from shows.models import Member
from slack.service import SlackBoss
from slack.tests.utils import slack_id_faker
from users.admin import UserAdmin
from users.models import User
from users.tests.utils import fake_user_data


class TestUserAdmin(TestCase):
    def setUp(self):
        faker = Faker()
        Faker.seed(0)

        patcher = patch.object(
            SlackBoss, "fetch_user", side_effect=slack_id_faker(faker)
        )
        self.mock_fetch_user = patcher.start()
        self.addCleanup(patcher.stop)

        self.user_data = fake_user_data(faker)
        self.user = User.objects.create(
            email=self.user_data["email"],
            password=self.user_data["password"],
            first_name=self.user_data["first_name"],
            last_name=self.user_data["last_name"],
        )

        self.site = AdminSite()

    def test_admin_is_executive_board(self):
        for position, _ in Member.POSITIONS:
            self.user.member.position = position
            is_board = UserAdmin(User, self.site).board(self.user)
            if position == Member.POSITIONS.general_member:
                self.assertFalse(is_board)
            else:
                self.assertTrue(is_board)
