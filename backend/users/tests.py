from django.test import TestCase

from .models import User


class TestUserModel(TestCase):
    def setUp(self):
        self.email = "frankiev@gmail.com"
        self.first_name = "Frankie"
        self.last_name = "Valli"

    def test_create_user(self):
        user = User.objects.create(email=self.email, first_name=self.first_name,
                                   last_name=self.last_name)
        self.assertEqual(str(user), "Frankie Valli")
