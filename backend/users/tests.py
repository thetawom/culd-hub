from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import User


class TestUserModel(TestCase):
    def setUp(self):
        self.email = "frankiev@gmail.com"
        self.first_name = "Frankie"
        self.last_name = "Valli"
        self.password = "OhWhatANight"

    def test_create_user(self):
        user = User.objects.create(email=self.email, password=self.password,
                                   first_name=self.first_name,
                                   last_name=self.last_name)
        self.assertEqual(str(user), "Frankie Valli")

    def test_create_user_invalid_email_error(self):
        with self.assertRaises(ValueError):
            User.objects.create(email=None, password=self.password)
        with self.assertRaises(ValidationError):
            User.objects.create(email="abc", password=self.password)

    def test_create_superuser(self):
        superuser = User.objects.create_superuser(email=self.email,
                                                  password=self.password,
                                                  first_name=self.first_name,
                                                  last_name=self.last_name)
        self.assertEqual(str(superuser), "Frankie Valli")
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_active)

    def test_create_superuser_error(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email=self.email,
                                          password=self.password,
                                          is_superuser=False)
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email=self.email,
                                          password=self.password,
                                          is_staff=False)
