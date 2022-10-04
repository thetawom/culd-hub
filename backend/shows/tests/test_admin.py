from django.contrib.admin import AdminSite
from django.test import TestCase
from faker import Faker

from shows.admin import ShowAdmin
from shows.models import Show
from shows.tests.utils import fake_show_data


# logging.disable(logging.WARNING)


class TestShowAdmin(TestCase):
    def setUp(self):
        faker = Faker()
        Faker.seed(0)

        self.show_data = fake_show_data(faker, count=1)
        self.show = Show.objects.create(
            name=self.show_data["name"],
            date=self.show_data["date"],
            address=self.show_data["address"],
            lions=self.show_data["lions"],
        )

        self.site = AdminSite()

    def test_admin_board(self):
        show_admin = ShowAdmin(Show, self.site)
        self.assertIsNone(show_admin.rounds(self.show))
