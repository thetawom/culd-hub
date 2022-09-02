from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core import signing

from users.exceptions import TokenScopeError


class TokenAction(object):
    PASSWORD_RESET = "password_reset"


class ActionTokenGenerator:
    def __init__(self):
        self.token_generator = PasswordResetTokenGenerator()

    def make_token(self, user, action):
        token = self.token_generator.make_token(user)
        payload = {"token": token, "action": action}
        return signing.dumps(payload, compress=True)

    def check_token(self, user, token, action, exp=None):
        payload = signing.loads(token, max_age=exp)
        if action != payload.pop("action"):
            raise TokenScopeError
        return self.token_generator.check_token(user, payload.pop("token"))


action_token = ActionTokenGenerator()
