from django.core import signing

from .exceptions import TokenScopeError


def get_token(user, action, **kwargs):
    payload = {"email": user.email, "action": action}
    if kwargs:
        payload.update(**kwargs)
    token = signing.dumps(payload, compress=True)
    return token


def get_token_payload(token, action, exp=None):
    payload = signing.loads(token, max_age=exp)
    _action = payload.pop("action")
    if _action != action:
        raise TokenScopeError
    return payload
