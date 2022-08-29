import datetime
from unittest.mock import patch

from django.contrib.admin.sites import AdminSite
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase

from users.models import User
from .admin import ShowAdmin
from .models import Member, Show, Round, Role, Contact
from .slack import slack_boss

USER = {
    "email": "frankiev@gmail.com",
    "password": "OhWhatANight",
    "first_name": "Frankie",
    "last_name": "Valli",
}

USERS = [
    USER,
    {
        "email": "bobg@gmail.com",
        "password": "OhWhatANight",
        "first_name": "Bob",
        "last_name": "Gaudio",
    },
    {
        "email": "tommyd@gmail.com",
        "password": "OhWhatANight",
        "first_name": "Tommy",
        "last_name": "Devito",
    },
]

SHOW_NAME = "National Hot Dog Day"
SHOW_DATE = datetime.date(2022, 7, 20)
SHOW_TIMES = [
    datetime.time(12, 30, 15),
    datetime.time(7, 45, 0),
    datetime.time(19, 15, 0),
]
ADDRESS = "1310 Surf Ave, Brooklyn, NY 11224"
LIONS = 2


class TestMemberModel(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            email=USER["email"],
            password=USER["password"],
            first_name=USER["first_name"],
            last_name=USER["last_name"],
        )

    def test_create_member_from_user(self):
        self.assertEqual(Member.objects.count(), 1)
        member = Member.objects.get(user__email=USER["email"])
        self.assertEqual(self.user, member.user)
        self.assertEqual(str(member), self.user.get_full_name())

    def test_create_duplicate_member_error(self):
        with self.assertRaises(IntegrityError):
            Member.objects.create(user=self.user)

    def test_delete_user_from_member(self):
        pre_user_count = User.objects.count()
        Member.objects.get(user=self.user).delete()
        self.assertEqual(User.objects.count(), pre_user_count - 1)


class TestShowModel(TestCase):
    def setUp(self):
        with patch("show_manager.slack.slack_boss") as mock_slack_boss:
            mock_slack_boss.create_channel.return_value = {
                "ok": True,
                "channel": {"id": 1},
            }
            mock_slack_boss.post_message.return_value = {
                "ok": True,
                "channel": {"id": 1},
            }

        self.users = [
            User.objects.create(
                email=user["email"],
                password=user["password"],
                first_name=user["first_name"],
                last_name=user["last_name"],
            )
            for user in USERS
        ]
        self.members = [user.member for user in self.users]

        self.show = Show.objects.create(
            name=SHOW_NAME,
            date=SHOW_DATE,
            address=ADDRESS,
            lions=LIONS,
            point=self.members[0],
        )

        for time in SHOW_TIMES:
            Round.objects.create(show=self.show, time=time)

        for performer in self.members:
            Role.objects.create(show=self.show, performer=performer)

    def test_show_rounds_and_performers(self):
        for show_round in self.show.rounds.all():
            self.assertEqual(str(show_round), f"{SHOW_NAME} at {show_round.time}")
        for role in Role.objects.filter(show=self.show):
            self.assertEqual(str(role), f"{SHOW_NAME} ({str(role.performer.user)})")

    def test_show_displays(self):
        self.assertEqual(str(self.show), SHOW_NAME)
        self.assertEqual(self.show.day_of_week(), "WED")
        self.assertEqual(self.show.format_date(), "07/20")
        self.assertEqual(self.show.show_times(), "7:45 AM · 12:30 PM · 7:15 PM")
        self.assertEqual(self.show.num_performers(), len(self.members))
        self.assertEqual(self.show.time, min(SHOW_TIMES))

    def test_create_empty_show(self):
        show = Show.objects.create(name=SHOW_NAME)
        self.assertIsNone(show.day_of_week())
        self.assertIsNone(show.format_date())
        self.assertIsNone(show.format_time())
        self.assertIsNone(show.show_times())
        self.assertEqual(show.num_performers(), 0)

    def test_create_show_without_name(self):
        with self.assertRaises(ValidationError):
            Show.objects.create()
        with self.assertRaises(ValidationError):
            Show.objects.create(name="")

    def test_add_duplicate_performer_error(self):
        show = Show.objects.create(name=SHOW_NAME)
        Role.objects.create(show=show, performer=self.members[0])
        with self.assertRaises(IntegrityError):
            Role.objects.create(show=show, performer=self.members[0])

    def test_update_time_after_round_added(self):
        show = Show.objects.create(name=SHOW_NAME)
        self.assertIsNone(show.time)
        for i, time in enumerate(SHOW_TIMES):
            Round.objects.create(show=show, time=time)
            self.assertEqual(show.time, min(SHOW_TIMES[: i + 1]))
        self.assertEqual(show.rounds.count(), len(SHOW_TIMES))

    def test_publish_show_without_date(self):
        show = Show.objects.create(name=SHOW_NAME)
        with self.assertRaises(ValidationError):
            show.is_published = True
            show.save()


class TestContactModel(TestCase):
    def setUp(self):
        pass

    def test_create_contact(self):
        contact = Contact.objects.create(first_name="Tom", last_name="Hanks")
        self.assertEqual(str(contact), "Tom Hanks")


class TestShowAdmin(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.show = Show.objects.create(name=SHOW_NAME)

    def test_admin_board(self):
        show_admin = ShowAdmin(Show, self.site)
        self.assertIsNone(show_admin.rounds(self.show))
        for time in SHOW_TIMES:
            Round.objects.create(show=self.show, time=time)
        self.assertEqual(show_admin.rounds(self.show), len(SHOW_TIMES))


class TestSlackBoss(TestCase):
    def setUp(self):
        testShowModel = TestShowModel()
        testShowModel.setUp()
        self.show = testShowModel.show

    def test_slack_boss_channel_name(self):
        channel_name = slack_boss._get_channel_name(self.show)
        self.assertEqual(channel_name, "07-20-national-hot-dog-day")
