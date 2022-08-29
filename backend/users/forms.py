from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, UsernameField


class CustomUsernameField(UsernameField):
    required = False


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["email", "password1", "password2", "first_name", "last_name", "phone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"].required = False


class UpdateUserForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ["email", "password", "first_name", "last_name", "phone"]
        field_classes = {"username": CustomUsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            self.fields[key].required = False
