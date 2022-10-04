from django.test import SimpleTestCase

from common.exceptions import CustomException


class TestCustomException(SimpleTestCase):
    def test_custom_exception_default_message(self):
        with self.assertRaisesMessage(CustomException, CustomException.default_message):
            raise CustomException

    def test_custom_exception_override_message(self):
        message = "Custom error message"
        with self.assertRaisesMessage(CustomException, message):
            raise CustomException(message)
