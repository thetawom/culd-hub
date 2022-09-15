import logging

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from faker import Faker

from slack.tests.utils import PatchSlackBossMixin
from users.tests.utils import fake_user_data

logging.disable(logging.WARNING)

User = get_user_model()


class TestUserModel(PatchSlackBossMixin, TestCase):
    def setUp(self):
        super().setUp()

        faker = Faker()
        Faker.seed(0)

        self.user_data = fake_user_data(faker)

    def test_create_user(self):
        user = User.objects.create(
            email=self.user_data["email"],
            password=self.user_data["password"],
            first_name=self.user_data["first_name"],
            last_name=self.user_data["last_name"],
        )
        self.assertEqual(
            str(user),
            f"{self.user_data['first_name']} " f"{self.user_data['last_name']}",
        )

    def test_create_user_invalid_email_error(self):
        with self.assertRaises(ValueError):
            User.objects.create(email=None, password=self.user_data["password"])
        with self.assertRaises(ValidationError):
            User.objects.create(email="abc", password=self.user_data["password"])

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(
            email=self.user_data["email"],
            password=self.user_data["password"],
            first_name=self.user_data["first_name"],
            last_name=self.user_data["last_name"],
        )
        self.assertEqual(
            str(superuser),
            f"{self.user_data['first_name']} " f"{self.user_data['last_name']}",
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)

    def test_create_superuser_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email=self.user_data["email"],
                password=self.user_data["password"],
                is_superuser=False,
            )
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email=self.user_data["email"],
                password=self.user_data["password"],
                is_staff=False,
            )
