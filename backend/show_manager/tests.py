import datetime

from django.db.utils import IntegrityError
from django.test import TestCase

from users.models import User
from .models import Member, Show, Round, Role, Contact


class TestMemberModel(TestCase):
    def setUp(self):
        self.email = "frankiev@gmail.com"
        self.password = "OhWhatANight"
        self.first_name = "Frankie"
        self.last_name = "Valli"

    def test_create_member_from_user(self):
        pre_member_count = Member.objects.count()
        user = User.objects.create(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
        )
        self.assertEqual(Member.objects.count(), pre_member_count + 1)
        member = Member.objects.get(user__email=self.email)
        self.assertEqual(user, member.user)
        self.assertEqual(str(member), user.get_full_name())

    def test_create_duplicate_member_error(self):
        user = User.objects.create(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
        )
        with self.assertRaises(IntegrityError):
            Member.objects.create(user=user)

    def test_delete_user_from_member(self):
        user = User.objects.create(
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
        )
        pre_user_count = User.objects.count()
        Member.objects.get(user=user).delete()
        self.assertEqual(User.objects.count(), pre_user_count - 1)


class TestShowModel(TestCase):
    def setUp(self):
        self.users = [
            User.objects.create(
                email="frankiev@gmail.com",
                password="OhWhatANight",
                first_name="Frankie",
                last_name="Valli",
            ),
            User.objects.create(
                email="bobg@gmail.com",
                password="OhWhatANight",
                first_name="Bob",
                last_name="Gaudio",
            ),
            User.objects.create(
                email="tommyd@gmail.com",
                password="OhWhatANight",
                first_name="Tommy",
                last_name="Devito",
            ),
        ]
        self.members = [user.member for user in self.users]

        self.show_name = "National Hot Dog Day"
        self.date = datetime.date(2022, 7, 20)
        self.times = [
            datetime.time(12, 30, 15),
            datetime.time(7, 45, 0),
            datetime.time(19, 15, 0),
        ]
        self.address = "1310 Surf Ave, Brooklyn, NY 11224"
        self.lions = 2

    def test_create_show(self):
        show = Show.objects.create(
            name=self.show_name,
            date=self.date,
            address=self.address,
            lions=self.lions,
            point=self.members[0],
        )
        for time in self.times:
            new_round = Round.objects.create(show=show, time=time)
            self.assertEqual(str(new_round), f"{self.show_name} at {time}")

        for performer in self.members:
            new_role = Role.objects.create(show=show, performer=performer)
            self.assertEqual(str(new_role), f"{self.show_name} ({str(performer.user)})")

        self.assertEqual(str(show), self.show_name)
        self.assertEqual(show.day_of_week(), "WED")
        self.assertEqual(show.format_date(), "07/20")
        self.assertEqual(show.show_times(), "7:45 AM · 12:30 PM · 7:15 PM")
        self.assertEqual(show.num_performers(), len(self.members))
        self.assertEqual(show.time, min(self.times))

    def test_create_empty_show(self):
        show = Show.objects.create(name=self.show_name)
        self.assertIsNone(show.day_of_week())
        self.assertIsNone(show.format_date())
        self.assertIsNone(show.format_time())
        self.assertIsNone(show.show_times())
        self.assertEqual(show.num_performers(), 0)

    def test_add_duplicate_performer_error(self):
        show = Show.objects.create(name=self.show_name)
        Role.objects.create(show=show, performer=self.members[0])
        with self.assertRaises(IntegrityError):
            Role.objects.create(show=show, performer=self.members[0])

    def test_update_time_after_round_added(self):
        show = Show.objects.create(name=self.show_name)
        self.assertIsNone(show.time)
        for i, time in enumerate(self.times):
            Round.objects.create(show=show, time=time)
            self.assertEqual(show.time, min(self.times[: i + 1]))
        self.assertEqual(show.rounds.count(), len(self.times))


class TestContactModel(TestCase):
    def setUp(self):
        pass

    def test_create_contact(self):
        contact = Contact.objects.create(first_name="Tom", last_name="Hanks")
        self.assertEqual(str(contact), "Tom Hanks")
