from django.forms import ModelForm

from .models import Member


class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = ["school", "class_year"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            self.fields[key].required = False
