from django.db import models
from django.contrib import admin
from django.contrib.auth import get_user_model
from phonenumber_field.modelfields import PhoneNumberField

User = get_user_model()

MEMBERSHIP_CHOICES = (
    ("G", "General Member"),
    ("B", "Executive Board Member"),
)

SHOW_PRIORITY_CHOICES = (
    (1, "Full"),
    (2, "Regular"),
    (3, "Urgent"),
)

PERFORMANCE_ROLE_CHOICES = (
    ("L", "Lion"),
    ("D", "Drum"),
    ("C", "Cymbal"),
    ("G", "Gong"),
    ("M", "Monk"),
    ("O", "Other"),
)


class Member(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, related_name="member"
    )
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default="G")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Show(models.Model):
    name = models.CharField(max_length=60)
    date = models.DateField(null=True, blank=True)
    time = models.TimeField(null=True, blank=True, editable=False)
    address = models.CharField(max_length=80, blank=True)
    lions = models.PositiveSmallIntegerField(null=True, blank=True)

    point = models.ForeignKey(
        "Member",
        on_delete=models.PROTECT,
        related_name="pointed_shows",
        null=True,
        blank=True,
    )
    contact = models.ForeignKey(
        "Contact", on_delete=models.PROTECT, related_name="shows", null=True, blank=True
    )
    performers = models.ManyToManyField(
        "Member", through="Role", related_name="performed_shows"
    )

    is_campus = models.BooleanField(verbose_name="On Campus", default=False)
    is_published = models.BooleanField(
        verbose_name="Published",
        help_text="Whether or not show is visible to users",
        default=False,
    )
    is_open = models.BooleanField(
        verbose_name="Open",
        help_text="Whether or not show is open for sign-ups",
        default=True,
    )
    priority = models.PositiveSmallIntegerField(
        choices=SHOW_PRIORITY_CHOICES, default=2
    )

    class Meta:
        ordering = ["date", "time"]

    @admin.display(description="Day of Week")
    def day_of_week(self):
        return self.date.strftime("%a").upper() if self.date else None

    @admin.display(description="Date", ordering="date")
    def format_date(self):
        return self.date.strftime("%m/%d") if self.date else None

    @admin.display(description="Time", ordering="time")
    def format_time(self):
        return self.time.strftime("%-I:%M %p") if self.time else None

    @admin.display(description="Times", ordering="time")
    def show_times(self):
        if self.rounds.count() == 0:
            return None
        return " · ".join(
            [round.time.strftime("%-I:%M %p") for round in self.rounds.all()]
        )

    @admin.display(description="Performers")
    def num_performers(self):
        return self.performers.count()

    def __str__(self):
        return self.name


class Round(models.Model):
    show = models.ForeignKey("Show", on_delete=models.CASCADE, related_name="rounds")
    time = models.TimeField(null=True, blank=True)

    class Meta:
        unique_together = [["show", "time"]]

    def __str__(self):
        return f"{self.show} at {self.time}"


class Role(models.Model):
    show = models.ForeignKey("Show", on_delete=models.CASCADE)
    performer = models.ForeignKey("Member", on_delete=models.CASCADE)
    role = models.CharField(
        max_length=1,
        choices=PERFORMANCE_ROLE_CHOICES,
        blank=True,
    )

    class Meta:
        unique_together = [["show", "performer"]]

    def __str__(self):
        return f"{self.show.name} ({self.performer.user.first_name} {self.performer.user.last_name})"


class Contact(models.Model):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    email = models.EmailField(max_length=30, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
