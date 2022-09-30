from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UsernameField, UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from django.forms import ModelMultipleChoiceField, ModelForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class CustomUsernameField(UsernameField):
    required = False


class RegisterForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["email", "password1", "password2", "first_name", "last_name", "phone"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["phone"].required = False

    def save(self, *args, **kwargs):
        self.instance.is_active = False
        return super().save(*args, **kwargs)


class UpdateUserForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ["email", "password", "first_name", "last_name", "phone"]
        field_classes = {"username": CustomUsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            self.fields[key].required = False


class GroupAdminForm(ModelForm):
    class Meta:
        model = Group
        exclude = []

    users = ModelMultipleChoiceField(
        queryset=User.objects.filter(is_staff=True),
        required=False,
        widget=FilteredSelectMultiple("users", False),
        label=_("Users"),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["users"].initial = self.instance.user_set.all()

    def save_m2m(self):
        self.instance.user_set.set(self.cleaned_data["users"])

    def save(self, *args, **kwargs):
        instance = super().save()
        self.save_m2m()
        return instance
