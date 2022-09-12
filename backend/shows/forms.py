import logging

from django.forms import ModelForm

from shows.models import Member, Show


class MemberForm(ModelForm):
    class Meta:
        model = Member
        fields = ["school", "class_year"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, field in self.fields.items():
            self.fields[key].required = False


class ShowAdminForm(ModelForm):
    class Meta:
        model = Show
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.name != "":
            logging.error("INSTANCE!")
            logging.error(self.instance.name)
            self.fields["point"].queryset = Member.objects.filter(
                performed_shows=self.instance
            )
        else:
            self.fields["point"].queryset = Member.objects.none()
