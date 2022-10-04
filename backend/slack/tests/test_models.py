from unittest.mock import Mock, MagicMock

from django.test import TestCase
from faker import Faker

from common.exceptions import WrongUsage
from shows.models import Member, Show
from slack.models import SlackUser, SlackChannel
from slack.tests.utils import fake_slack_id, PatchSlackBossMixin, fake_slack_timestamp


# logging.disable(logging.WARNING)


class TestSlackUser(TestCase):
    def setUp(self):
        faker = Faker()
        Faker.seed(382)

        self.user_id = fake_slack_id(faker)
        self.member = Mock(spec=Member)
        self.member._state = MagicMock()

        self.slack_user = SlackUser(id=self.user_id, member=self.member)

    def test_mention(self):
        mention_tag = self.slack_user.mention()
        self.assertEqual(mention_tag, f"<@{self.user_id}>")


class TestSlackChannel(PatchSlackBossMixin, TestCase):
    def setUp(self):
        super().setUp()

        faker = Faker()
        Faker.seed(231)

        self.channel_id = fake_slack_id(faker)
        self.channel_name = "-".join(faker.words(nb=3))
        self.show = Mock(spec=Show)
        self.show._state = MagicMock()
        self.show.default_channel_name.return_value = self.channel_name
        self.slack_user = Mock(spec=SlackUser)
        self.slack_user._state = MagicMock()
        self.message_ts = fake_slack_timestamp(faker)

        self.slack_channel = SlackChannel(
            id=self.channel_id, show=self.show, briefing_ts=self.message_ts
        )

        self.field_names = faker.words(nb=3)

    def test_slack_channel_to_string(self):
        self.assertEqual(str(self.slack_channel), self.channel_name)

    def test_slack_channel_update_name(self):
        self.slack_channel.update_name(name=self.channel_name)
        self.mock_rename_channel.assert_called_with(
            channel_id=self.channel_id, name=self.channel_name, show=self.show
        )

    def test_slack_channel_archive(self):
        self.slack_channel.archive()
        self.mock_rename_channel.assert_called_once()
        self.mock_archive_channel.assert_called_once_with(channel_id=self.channel_id)

    def test_slack_channel_archive_without_rename(self):
        self.slack_channel.archive(rename=False)
        self.mock_rename_channel.assert_not_called()
        self.mock_archive_channel.assert_called_once_with(channel_id=self.channel_id)

    def test_slack_channel_invite_users(self):
        self.slack_channel.invite_users(users=self.slack_user)
        self.mock_invite_users_to_channel.assert_called_with(
            channel_id=self.channel_id, users=self.slack_user
        )

    def test_slack_channel_invite_performers(self):
        member = Mock(spec=Member)
        member._state = MagicMock()
        member.fetch_slack_user.return_value = self.slack_user

        self.show.performers.count.return_value = 1
        self.show.performers.all.return_value = [member]
        self.slack_channel.invite_performers()
        self.mock_invite_users_to_channel.assert_called_once_with(
            channel_id=self.channel_id, users=[self.slack_user]
        )

    def test_slack_channel_invite_performers_none(self):
        self.show.performers.count.return_value = 0
        self.slack_channel.invite_performers()
        self.mock_invite_users_to_channel.assert_not_called()

    def test_slack_channel_remove_users(self):
        self.slack_channel.remove_users(users=self.slack_user)
        self.mock_remove_users_from_channel.assert_called_with(
            channel_id=self.channel_id, users=self.slack_user
        )

    def test_send_update_message(self):
        self.slack_channel.send_update_message(updated_fields=self.field_names)
        _, kwargs = self.mock_send_message_in_channel.call_args_list[0]
        self.assertEqual(kwargs["channel_id"], self.channel_id)
        for field_name in self.field_names:
            self.assertTrue(field_name in str(kwargs["blocks"]))

    def test_send_update_message_with_no_updated_fields(self):
        with self.assertRaises(ValueError):
            self.slack_channel.send_update_message(updated_fields=[])

    def test_send_update_message_with_no_message(self):
        self.slack_channel.briefing_ts = ""
        with self.assertRaises(WrongUsage):
            self.slack_channel.send_update_message(updated_fields=[])
