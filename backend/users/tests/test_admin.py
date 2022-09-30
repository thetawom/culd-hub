import logging

from django.contrib.admin import AdminSite
from django.test import TestCase
from faker import Faker

from shows.models import Member
from slack.tests.utils import PatchSlackBossMixin
from users.admin import UserAdmin
from users.models import User
from users.tests.utils import fake_user_data

logging.disable(logging.WARNING)


class TestUserAdmin(PatchSlackBossMixin, TestCase):
    def setUp(self):
        super().setUp()

        faker = Faker()
        Faker.seed(1234)

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
