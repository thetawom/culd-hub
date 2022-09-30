from django.contrib.auth.backends import ModelBackend

from common.exceptions import CustomException


class CustomAuthBackend(ModelBackend):
    def user_can_authenticate(self, user):
        if not super().user_can_authenticate(user):
            raise CustomException("User is not active")
        return True
