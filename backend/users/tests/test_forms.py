from django.contrib.auth import get_user_model
from django.test import TestCase
from faker import Faker

from slack.tests.utils import PatchSlackBossMixin
from users.forms import RegisterForm, UpdateUserForm, GroupAdminForm
from users.tests.utils import fake_user_data

User = get_user_model()


class TestRegisterForm(PatchSlackBossMixin, TestCase):
    form = RegisterForm

    def setUp(self):
        super().setUp()

        faker = Faker()
        Faker.seed(0)

        self.user_data = fake_user_data(faker)

    def test_register_success(self):
        f = self.form(
            data={
                "email": self.user_data["email"],
                "password1": self.user_data["password"],
                "password2": self.user_data["password"],
                "first_name": self.user_data["first_name"],
                "last_name": self.user_data["last_name"],
            }
        )
        self.assertTrue(f.is_valid())
        user = f.save()

        self.assertEqual(user.email, self.user_data["email"])
        self.assertEqual(user.first_name, self.user_data["first_name"])
        self.assertEqual(user.last_name, self.user_data["last_name"])

        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)


class TestUpdateUserForm(PatchSlackBossMixin, TestCase):
    form = UpdateUserForm

    def setUp(self):
        super().setUp()

        faker = Faker()
        Faker.seed(0)

        self.user_data = fake_user_data(faker)
        self.user = User.objects.create(
            email=self.user_data["email"],
            password=self.user_data["password"],
            first_name=self.user_data["first_name"],
            last_name=self.user_data["last_name"],
        )

        self.email = faker.email()

    def test_update_user_success(self):
        f = self.form(data={"email": self.email}, instance=self.user)
        self.assertTrue(f.is_valid())
        user = f.save()
        self.assertEqual(user.email, self.email)


class TestGroupAdminForm(PatchSlackBossMixin, TestCase):
    form = GroupAdminForm

    def setUp(self):
        super().setUp()

        faker = Faker()
        Faker.seed(0)

        self.group_name = faker.words(nb=1)[0]
        self.user_data = fake_user_data(faker, count=3)
        self.users = [
            User.objects.create(
                email=user["email"],
                password=user["password"],
                first_name=user["first_name"],
                last_name=user["last_name"],
                is_staff=(i != 0),
            )
            for i, user in enumerate(self.user_data)
        ]

    def test_create_group(self):
        f = self.form(
            data={
                "name": self.group_name,
                "permissions": (1, 2, 3),
                "users": self.users[1:],
            }
        )
        self.assertTrue(f.is_valid())
        group = f.save()
        self.assertEqual(group.name, self.group_name)
        self.assertEqual(group.permissions.count(), 3)
        self.assertEqual(group.user_set.count(), 2)
        self.assertTrue(group.user_set.first() == self.users[1])

    def test_create_group_with_non_staff(self):
        f = self.form(
            data={
                "name": self.group_name,
                "permissions": (1, 2, 3),
                "users": (self.users[0],),
            }
        )
        self.assertFalse(f.is_valid())
