import logging

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.test import TestCase
from faker import Faker

from shows.models import Member, Show, Round, Role, Contact
from shows.tests.utils import fake_show_data, fake_round_data
from slack.models import SlackChannel
from slack.tests.utils import PatchSlackBossMixin, fake_slack_id
from users.tests.utils import fake_user_data

logging.disable(logging.WARNING)

User = get_user_model()


class TestMemberModel(PatchSlackBossMixin, TestCase):
    def setUp(self):
        super().setUp()

        faker = Faker()
        Faker.seed(0)

        self.user_data = fake_user_data(faker)
        self.user = User.objects.create(
            email=self.user_data["email"],
            password=self.user_data["password"],
            first_name=self.user_data["first_name"],
            last_name=self.user_data["last_name"],
        )

    def test_create_member_from_user(self):
        self.assertEqual(Member.objects.count(), 1)
        member = Member.objects.get(user__email=self.user_data["email"])
        self.assertEqual(self.user, member.user)
        self.assertEqual(str(member), self.user.get_full_name())

    def test_create_duplicate_member_error(self):
        with self.assertRaises(IntegrityError):
            Member.objects.create(user=self.user)

    def test_delete_user_from_member(self):
        pre_user_count = User.objects.count()
        Member.objects.get(user=self.user).delete()
        self.assertEqual(User.objects.count(), pre_user_count - 1)


class TestShowModel(PatchSlackBossMixin, TestCase):
    def setUp(self):
        super().setUp()

        faker = Faker()
        Faker.seed(0)

        self.user_data = fake_user_data(faker, count=3)
        self.users = [
            User.objects.create(
                email=user["email"],
                password=user["password"],
                first_name=user["first_name"],
                last_name=user["last_name"],
            )
            for user in self.user_data
        ]
        self.members = [user.member for user in self.users]

        self.show_data = fake_show_data(faker, count=1)
        self.show = Show.objects.create(
            name=self.show_data["name"],
            date=self.show_data["date"],
            address=self.show_data["address"],
            lions=self.show_data["lions"],
            point=self.members[0],
        )

        self.round_data = fake_round_data(faker, count=3)
        for show_round in self.round_data:
            Round.objects.create(show=self.show, time=show_round["time"])

        for performer in self.members:
            Role.objects.create(show=self.show, performer=performer)

        self.channel_id = fake_slack_id(faker)

    def test_show_rounds_and_performers(self):
        for show_round in self.show.rounds.all():
            self.assertEqual(
                str(show_round), f"{self.show_data['name']} at {show_round.time}"
            )
        for role in Role.objects.filter(show=self.show):
            self.assertEqual(
                str(role), f"{self.show_data['name']} ({str(role.performer.user)})"
            )

    def test_show_displays(self):
        show_date = self.show_data["date"]
        self.assertEqual(str(self.show), self.show_data["name"])
        self.assertEqual(self.show.day_of_week(), show_date.strftime("%a").upper())
        self.assertEqual(self.show.formatted_date(), show_date.strftime("%m/%d"))
        self.assertEqual(self.show.performer_count(), len(self.members))
        self.assertEqual(
            self.show.time, min([show_round["time"] for show_round in self.round_data])
        )

    def test_create_empty_show(self):
        show = Show.objects.create(name=self.show_data["name"])
        self.assertIsNone(show.day_of_week())
        self.assertIsNone(show.formatted_date())
        self.assertIsNone(show.formatted_time())
        self.assertEqual(show.performer_count(), 0)

    def test_create_show_without_name(self):
        with self.assertRaises(ValidationError):
            Show.objects.create()
        with self.assertRaises(ValidationError):
            Show.objects.create(name="")

    def test_add_duplicate_performer_error(self):
        show = Show.objects.create(name=self.show_data["name"])
        Role.objects.create(show=show, performer=self.members[0])
        with self.assertRaises(IntegrityError):
            Role.objects.create(show=show, performer=self.members[0])

    def test_update_time_after_round_added(self):
        show = Show.objects.create(name=self.show_data["name"])
        self.assertIsNone(show.time)
        for i, show_round in enumerate(self.round_data):
            Round.objects.create(show=show, time=show_round["time"])
            min_time = min([r["time"] for r in self.round_data[: i + 1]])
            self.assertEqual(show.time, min_time)
        self.assertEqual(show.rounds.count(), len(self.round_data))

    def test_publish_show_without_date(self):
        show = Show.objects.create(name=self.show_data["name"])
        with self.assertRaises(ValidationError):
            show.status = Show.STATUSES.published
            show.save()

    def test_default_channel_name(self):
        with self.assertRaises(ValueError):
            Show(name="", date=self.show_data["date"]).default_channel_name()
        with self.assertRaises(ValueError):
            Show(name=self.show_data["name"]).default_channel_name()
        name = self.show.default_channel_name()
        self.assertTrue(name.islower() and name.replace("-", "").isalnum())

    def test_has_slack_channel(self):
        self.assertFalse(self.show.has_slack_channel())
        SlackChannel(id=self.channel_id, show=self.show)
        self.assertTrue(self.show.has_slack_channel())
        self.assertEqual(self.show.channel.id, self.channel_id)

    def test_is_open(self):
        self.show.status = self.show.STATUSES.draft
        self.assertFalse(self.show.is_open())
        self.show.status = self.show.STATUSES.published
        self.assertTrue(self.show.is_open())
        self.show.status = self.show.STATUSES.closed
        self.assertFalse(self.show.is_open())


class TestContactModel(TestCase):
    def setUp(self):
        pass

    def test_create_contact(self):
        contact = Contact.objects.create(first_name="Tom", last_name="Hanks")
        self.assertEqual(str(contact), "Tom Hanks")
