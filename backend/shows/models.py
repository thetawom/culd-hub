from django.contrib import admin
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext as _
from model_utils import Choices
from phonenumber_field.modelfields import PhoneNumberField

from slack.models import SlackUser

User = get_user_model()


class Member(models.Model):
    """Model for a club member.

    Each Member has a one-to-zero-or-one relationship with User. Additional
    profile information such as the member's school, class year, and club
    position are also stored.
    """

    POSITIONS = Choices(
        (0, "general_member", _("General Member")),
        (1, "secretary", _("Secretary")),
        (2, "treasurer", _("Treasurer")),
        (3, "president", _("President")),
        (4, "senior_advisor", _("Senior Advisor")),
    )
    SCHOOLS = Choices(
        (0, "college", _("Columbia College")),
        (1, "engineering", _("School of Engineering and Applied Science")),
        (2, "barnard", _("Barnard College")),
        (3, "general_studies", _("School of General Studies")),
        (4, "other", _("Other")),
    )
    CLASS_YEARS = Choices(
        (0, "freshman", _("Freshman")),
        (1, "sophomore", _("Sophomore")),
        (2, "junior", _("Junior")),
        (3, "senior", _("Senior")),
        (4, "masters", _("Masters")),
        (4, "doctorate", _("Doctorate")),
        (5, "alumni", _("Alumni")),
        (6, "other", _("Other")),
    )

    user = models.OneToOneField(
        User, related_name="member", on_delete=models.CASCADE, null=True
    )
    position = models.PositiveSmallIntegerField(
        choices=POSITIONS, default=POSITIONS.general_member, verbose_name="position"
    )
    school = models.PositiveSmallIntegerField(
        choices=SCHOOLS, null=True, blank=True, default=None, verbose_name="school"
    )
    class_year = models.PositiveSmallIntegerField(
        choices=CLASS_YEARS,
        null=True,
        blank=True,
        default=None,
        verbose_name="class year",
    )

    def __str__(self):
        return f"{self.user.get_full_name()}"  # noqa

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.fetch_slack_user()

    def fetch_slack_user(self):
        """Fetch Slack user for member, creating one if necessary"""
        return SlackUser.objects.get_or_create(member=self)


class Show(models.Model):
    """Model for a show.

    Each Show stores information pertaining to the show, such as the date,
    time, venue address, number of lions, point person, performers, etc.
    """

    PRIORITIES = Choices(
        (0, "full", _("Full")),
        (1, "normal", _("Normal")),
        (2, "urgent", _("Urgent")),
    )
    STATUSES = Choices(
        (0, "draft", _("Draft")),
        (1, "published", _("Published")),
        (2, "closed", _("Closed")),
    )

    name = models.CharField(max_length=60, null=False, blank=False)
    date = models.DateField(null=True, blank=True, verbose_name="show date")
    time = models.TimeField(
        null=True,
        blank=True,
        editable=False,
        verbose_name="show time",
        help_text="time of the first round of the show, updated automatically",
    )
    address = models.CharField(
        max_length=80,
        blank=True,
        verbose_name="venue address",
        help_text=_("Venue name or room number if on campus"),
    )
    is_campus = models.BooleanField(default=False, verbose_name="On Campus")
    lions = models.PositiveSmallIntegerField(
        null=True, blank=True, verbose_name="Number of lions"
    )
    point = models.ForeignKey(
        "Member",
        related_name="pointed_shows",
        related_query_name="pointed_show",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="point person",
    )
    performers = models.ManyToManyField(
        "Member",
        related_name="performed_shows",
        related_query_name="performed_show",
        through="Role",
    )
    contact = models.ForeignKey(
        "Contact",
        related_name="shows",
        related_query_name="show",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    status = models.PositiveSmallIntegerField(choices=STATUSES, default=STATUSES.draft)
    priority = models.PositiveSmallIntegerField(
        choices=PRIORITIES, default=PRIORITIES.normal
    )

    class Meta:
        ordering = ["date", "time"]

    def __str__(self):
        return self.name

    def __iter__(self):
        for field in self._meta.fields:
            field_name = str(field).split(".")[-1]
            yield field_name, getattr(self, field_name, None)

    def clean(self):
        if self.status > Show.STATUSES.draft and self.date is None:
            raise ValidationError(
                {"is_published": _("Cannot publish show until date is set.")}
            )

    @admin.display(description="Day of Week")
    def day_of_week(self):
        return self.date.strftime("%a").upper() if self.date else None

    @admin.display(description="Date", ordering="date")
    def formatted_date(self, fmt="%m/%d"):
        return self.date.strftime(fmt) if self.date else None

    @admin.display(description="Time", ordering="time")
    def formatted_time(self, fmt="%-I:%M %p"):
        return self.time.strftime(fmt) if self.time else None

    @admin.display(description="Times", ordering="time")
    def show_times(self):
        if self.rounds.count() == 0:
            return None
        return " · ".join([r.time.strftime("%-I:%M %p") for r in self.rounds.all()])

    @admin.display(description="Performers")
    def performer_count(self):
        return self.performers.count()

    @admin.display(description="Slack", boolean=True)
    def has_slack_channel(self):
        return hasattr(self, "channel")


class Round(models.Model):
    """Model for a round of a show.

    Each Round belongs to a show and stores the performance time of that
    round. Each Show may have one or more Rounds (or none, if TBD).
    """

    show = models.ForeignKey(
        "Show",
        related_name="rounds",
        related_query_name="round",
        on_delete=models.CASCADE,
    )
    time = models.TimeField(null=True, blank=True)

    class Meta:
        unique_together = [["show", "time"]]

    def __str__(self):
        return f"{self.show} at {self.time}"


class Role(models.Model):
    """Model for a performer's role at a show.

    Each Role contains information about what role a performer played at a
    show, e.g., lion, drum, cymbal, gong, etc.
    """

    ROLES = Choices(
        (0, "lion", _("Lion")),
        (1, "drum", _("Drum")),
        (2, "cymbal", _("Cymbal")),
        (3, "gong", _("Gong")),
        (4, "monk", _("Monk")),
        (5, "other", _("Other")),
    )

    show = models.ForeignKey("Show", on_delete=models.CASCADE)
    performer = models.ForeignKey("Member", on_delete=models.CASCADE)
    role = models.PositiveSmallIntegerField(
        choices=ROLES, null=True, blank=True, default=None, verbose_name="role type"
    )

    class Meta:
        unique_together = [["show", "performer"]]

    def __str__(self):
        return f"{self.show.name} ({self.performer.user.get_full_name()})"  # noqa


class Contact(models.Model):
    """Model for a client contact.

    Each Contact contains information about the client's name, phone, email, etc.
    """

    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    email = models.EmailField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
