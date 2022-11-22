from typing import Optional, List, Union
from unittest.mock import patch, MagicMock

from django.conf import settings
from django.test import SimpleTestCase, override_settings
from faker import Faker
from slack_sdk.errors import SlackApiError

from common.exceptions import WrongUsage
from shows.models import Member, Show
from shows.tests.utils import fake_show_name, fake_show_data
from slack.exceptions import SlackTokenException, SlackBossException
from slack.models import SlackChannel, SlackUser
from slack.service import SlackBoss
from slack.tests.utils import fake_slack_token, fake_slack_id, fake_slack_timestamp
from users.models import User
from users.tests.utils import fake_user_data


# logging.disable(logging.WARNING)


class TestSlackBossArgs(SimpleTestCase):
    def setUp(self):
        self.faker = Faker()
        Faker.seed(421)

    def test_get_email_arg(self):
        with self.assertRaises(WrongUsage):
            SlackBoss._get_email_arg()

        email_arg = self.faker.email()
        user_data = fake_user_data(self.faker)
        user_arg = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"],
            password=user_data["password"],
        )
        member_arg = Member(user=user_arg)

        email, label = SlackBoss._get_email_arg(email=email_arg, user=user_arg)
        self.assertEqual(email, email_arg)
        self.assertEqual(label, email_arg)

        email, label = SlackBoss._get_email_arg(user=user_arg)
        self.assertEqual(email, user_arg.email)
        self.assertEqual(label, str(user_arg))

        email, label = SlackBoss._get_email_arg(member=member_arg)
        self.assertEqual(email, user_arg.email)
        self.assertEqual(label, str(member_arg))

        with self.assertRaises(SlackBossException):
            SlackBoss._get_email_arg(member=Member())

    def test_get_channel_name_arg(self):
        with self.assertRaises(WrongUsage):
            SlackBoss._get_channel_name_arg()

        name_arg = fake_show_name(self.faker)
        show_data = fake_show_data(self.faker)
        show_arg = Show(
            name=show_data["name"],
            date=show_data["date"],
        )

        name, label = SlackBoss._get_channel_name_arg(name=name_arg, show=show_arg)
        self.assertEqual(name, name_arg)
        self.assertEqual(label, name_arg)

        name, label = SlackBoss._get_channel_name_arg(show=show_arg)
        self.assertEqual(name, show_arg.default_channel_name())
        self.assertEqual(label, str(show_arg))

    def test_get_channel_id_arg(self):
        with self.assertRaises(WrongUsage):
            SlackBoss._get_slack_channel_id_arg()

        channel_id_arg = fake_slack_id(self.faker)
        show_data = fake_show_data(self.faker)
        show_arg = Show(
            name=show_data["name"],
            date=show_data["date"],
        )

        with self.assertRaises(SlackBossException):
            SlackBoss._get_slack_channel_id_arg(show=show_arg)

        channel_arg = SlackChannel(id=fake_slack_id(self.faker), show=show_arg)

        channel_id, label = SlackBoss._get_slack_channel_id_arg(
            channel_id=channel_id_arg, channel=channel_arg
        )
        self.assertEqual(channel_id, channel_id_arg)
        self.assertEqual(label, channel_id_arg)

        channel_id, label = SlackBoss._get_slack_channel_id_arg(channel=channel_arg)
        self.assertEqual(channel_id, channel_arg.id)
        self.assertEqual(label, show_arg.default_channel_name())

        channel_id, label = SlackBoss._get_slack_channel_id_arg(show=show_arg)
        self.assertEqual(channel_id, channel_arg.id)
        self.assertEqual(label, show_arg.default_channel_name())

    def test_get_slack_user_ids_arg(self):
        with self.assertRaises(WrongUsage):
            SlackBoss._get_slack_user_ids_arg()

        user_ids_arg = fake_slack_id(self.faker, count=3)
        user_data = fake_user_data(self.faker, count=3)
        users = [
            User(
                first_name=user["first_name"],
                last_name=user["last_name"],
                email=user["email"],
                password=user["password"],
            )
            for user in user_data
        ]
        members = [Member(user=user) for user in users]
        users_arg = [
            SlackUser(id=user_id, member=member)
            for user_id, member in zip(user_ids_arg, members)
        ]

        user_ids, label = SlackBoss._get_slack_user_ids_arg(user_ids=user_ids_arg)
        self.assertEqual(user_ids, user_ids_arg)
        self.assertEqual(label, str(user_ids_arg))

        user_ids, label = SlackBoss._get_slack_user_ids_arg(users=users_arg)
        self.assertEqual(user_ids, user_ids_arg)
        self.assertEqual(label, str(members))

        user_ids, label = SlackBoss._get_slack_user_ids_arg(users=users_arg[0])
        self.assertEqual(user_ids, user_ids_arg[0])
        self.assertEqual(label, str(users_arg[0]))

    def test_get_show_arg(self):
        with self.assertRaises(WrongUsage):
            SlackBoss._get_show_arg()

        show_data = fake_show_data(self.faker)
        show_arg = Show(
            name=show_data["name"],
            date=show_data["date"],
        )
        channel_arg = SlackChannel(id=fake_slack_id(self.faker), show=show_arg)

        show, label = SlackBoss._get_show_arg(show=show_arg)
        self.assertEqual(show, show_arg)
        self.assertEqual(label, str(show))

        show, label = SlackBoss._get_show_arg(channel=channel_arg)
        self.assertEqual(show, show_arg)
        self.assertEqual(label, str(show))

    def test_get_message_timestamp_arg(self):
        ts, label = SlackBoss._get_message_timestamp_arg()
        self.assertIsNone(ts)
        self.assertEqual(label, "")

        ts, label = SlackBoss._get_message_timestamp_arg(ts="")
        self.assertIsNone(ts)
        self.assertEqual(label, "")

        ts_arg = fake_slack_timestamp(self.faker)
        ts, label = SlackBoss._get_message_timestamp_arg(ts=ts_arg)
        self.assertEqual(ts, ts_arg)
        self.assertEqual(label, ts_arg)


class TestSlackBoss(SimpleTestCase):
    @patch("slack.service.WebClient")
    def setUp(self, mock_web_client):
        self.faker = Faker()
        Faker.seed(26)

        self.mock_client = MagicMock()
        mock_web_client.return_value = self.mock_client
        self.slack_boss = SlackBoss()

        self.generic_slack_api_error = SlackApiError(message="", response={"error": ""})

    @override_settings()
    def test_init_with_no_slack_token_error(self):
        delattr(settings, "SLACK_TOKEN")
        with self.assertRaises(SlackTokenException):
            SlackBoss()

    @patch("slack.service.WebClient")
    def test_init_with_override_slack_token(self, mock_web_client):
        token = fake_slack_token(self.faker)
        slack_boss = SlackBoss(token=token)
        self.assertEqual(slack_boss.token, token)
        mock_web_client.assert_called_with(token=token)
        self.assertEqual(slack_boss.client, mock_web_client.return_value)

    def test_fetch_user(self):
        user_ids = {self.faker.email(): fake_slack_id(self.faker) for _ in range(3)}

        def mock_users_lookupByEmail(email: str):
            if email in user_ids:
                return {
                    "ok": True,
                    "user": {"id": user_ids[email]},
                }
            raise SlackApiError(message="", response={"error": "users_not_found"})

        self.mock_client.users_lookupByEmail.side_effect = mock_users_lookupByEmail

        for user_email, user_id in user_ids.items():
            fetched_user_id = self.slack_boss.fetch_user(email=user_email)
            self.mock_client.users_lookupByEmail.assert_called_with(email=user_email)
            self.assertEqual(fetched_user_id, user_id)

        nonexistent_email = self.faker.email()
        fetched_user_id = self.slack_boss.fetch_user(email=nonexistent_email)
        self.mock_client.users_lookupByEmail.assert_called_with(email=nonexistent_email)
        self.assertIsNone(fetched_user_id)

        self.mock_client.users_lookupByEmail.side_effect = self.generic_slack_api_error
        with self.assertRaises(SlackBossException):
            self.slack_boss.fetch_user(email="")

    def test_create_channel(self):
        show_name = fake_show_name(self.faker)
        channel_id = fake_slack_id(self.faker)

        def mock_conversations_create(name: str, is_private: Optional[bool] = False):
            return {"ok": True, "channel": {"id": channel_id}}

        self.mock_client.conversations_create.side_effect = mock_conversations_create

        fetched_channel_id = self.slack_boss.create_channel(name=show_name)
        self.mock_client.conversations_create.assert_called_with(
            name=show_name, is_private=False
        )
        self.assertEqual(fetched_channel_id, channel_id)

        self.mock_client.conversations_create.side_effect = self.generic_slack_api_error
        with self.assertRaises(SlackBossException):
            self.slack_boss.create_channel(name=show_name)

    def test_archive_channel(self):
        channel_id = fake_slack_id(self.faker)

        def mock_conversations_archive(channel: str):
            if channel == channel_id:
                return {"ok": True}
            raise self.generic_slack_api_error

        self.mock_client.conversations_archive.side_effect = mock_conversations_archive

        archive_success = self.slack_boss.archive_channel(channel_id=channel_id)
        self.mock_client.conversations_archive.assert_called_with(channel=channel_id)
        self.assertTrue(archive_success)

        with self.assertRaises(SlackBossException):
            self.slack_boss.archive_channel(channel_id=fake_slack_id(self.faker))

    def test_rename_channel(self):
        show_name = fake_show_name(self.faker)
        channel_id = fake_slack_id(self.faker)

        def mock_conversations_rename(channel: str, name: str):
            if channel == channel_id:
                return {"ok": True, "channel": {"id": channel_id}}
            raise self.generic_slack_api_error

        self.mock_client.conversations_rename.side_effect = mock_conversations_rename

        name_updated = self.slack_boss.rename_channel(
            name=show_name, channel_id=channel_id
        )
        self.mock_client.conversations_rename.assert_called_with(
            channel=channel_id, name=show_name
        )
        self.assertTrue(name_updated)

        with self.assertRaises(SlackBossException):
            self.slack_boss.rename_channel(
                name=show_name, channel_id=fake_slack_id(self.faker)
            )

    def test_invite_users_to_channel(self):
        channel_id = fake_slack_id(self.faker)
        user_ids = fake_slack_id(self.faker, count=2)

        def mock_conversations_invite(channel: str, users=Union[str, List[str]]):
            for user in users if isinstance(users, list) else [users]:
                if user == user_ids[0]:
                    raise SlackApiError(
                        message="", response={"error": "already_in_channel"}
                    )
            return {"ok": True}

        self.mock_client.conversations_invite.side_effect = mock_conversations_invite

        invite_success = self.slack_boss.invite_users_to_channel(
            channel_id=channel_id, user_ids=user_ids[1:]
        )
        self.mock_client.conversations_invite.assert_called_with(
            channel=channel_id, users=user_ids[1:]
        )
        self.assertTrue(invite_success)

        invite_success = self.slack_boss.invite_users_to_channel(
            channel_id=channel_id, user_ids=user_ids
        )
        self.mock_client.conversations_invite.assert_called_with(
            channel=channel_id, users=user_ids
        )
        self.assertTrue(invite_success)

        self.mock_client.conversations_invite.side_effect = self.generic_slack_api_error
        with self.assertRaises(SlackBossException):
            self.slack_boss.invite_users_to_channel(
                channel_id=channel_id, user_ids=user_ids
            )

    def test_remove_users_from_channel(self):
        channel_id = fake_slack_id(self.faker)
        user_ids = fake_slack_id(self.faker, count=2)

        def mock_conversations_kick(channel: str, user: str):
            if user == user_ids[-1]:
                raise SlackApiError(message="", response={"error": "not_in_channel"})
            return {"ok": True}

        self.mock_client.conversations_kick.side_effect = mock_conversations_kick

        kick_success = self.slack_boss.remove_users_from_channel(
            channel_id=channel_id, user_ids=user_ids[0]
        )
        self.mock_client.conversations_kick.assert_called_once_with(
            channel=channel_id, user=user_ids[0]
        )
        self.assertTrue(kick_success)

        kick_success = self.slack_boss.remove_users_from_channel(
            channel_id=channel_id, user_ids=user_ids
        )
        self.assertEqual(self.mock_client.conversations_kick.call_count, 3)
        self.assertTrue(kick_success)

        self.mock_client.conversations_kick.side_effect = self.generic_slack_api_error
        with self.assertRaises(SlackBossException):
            self.slack_boss.remove_users_from_channel(
                channel_id=channel_id, user_ids=user_ids
            )

    def test_send_message_in_channel(self):
        channel_id = fake_slack_id(self.faker)
        message_ts = fake_slack_timestamp(self.faker)
        message_blocks, message_text = [{"blocks"}], "text"

        def mock_chat_postMessage(channel: str, blocks: List, text: str):
            if channel == channel_id:
                return {"ok": True, "ts": message_ts}
            raise self.generic_slack_api_error

        def mock_chat_update(channel: str, ts: str, blocks: List, text: str):
            if channel == channel_id:
                return {"ok": True, "ts": message_ts}
            raise self.generic_slack_api_error

        self.mock_client.chat_postMessage.side_effect = mock_chat_postMessage
        self.mock_client.chat_update.side_effect = mock_chat_update

        with self.assertRaises(WrongUsage):
            self.slack_boss.send_message_in_channel(channel_id=channel_id)

        sent_ts, is_new_message = self.slack_boss.send_message_in_channel(
            channel_id=channel_id, blocks=message_blocks, text=message_text
        )
        self.mock_client.chat_postMessage.assert_called_with(
            channel=channel_id, blocks=message_blocks, text=message_text
        )
        self.mock_client.chat_update.assert_not_called()
        self.assertTrue(is_new_message)
        self.assertEqual(sent_ts, message_ts)

        sent_ts, is_new_message = self.slack_boss.send_message_in_channel(
            channel_id=channel_id,
            ts=message_ts,
            blocks=message_blocks,
        )
        self.mock_client.chat_update.assert_called_with(
            channel=channel_id, ts=message_ts, blocks=message_blocks, text=None
        )
        self.assertFalse(is_new_message)
        self.assertEqual(sent_ts, message_ts)

        with self.assertRaises(SlackBossException):
            self.slack_boss.send_message_in_channel(
                channel_id=fake_slack_id(self.faker), blocks=message_blocks
            )

    def test_pin_message_in_channel(self):
        channel_id = fake_slack_id(self.faker)

        with self.assertRaises(WrongUsage):
            self.slack_boss.pin_message_in_channel(channel_id=channel_id)

        message_ts = fake_slack_timestamp(self.faker)
        self.mock_client.pins_add.return_value = {"ok": True}
        pin_success = self.slack_boss.pin_message_in_channel(
            channel_id=channel_id, ts=message_ts
        )
        self.mock_client.pins_add.assert_called_with(
            channel=channel_id, timestamp=message_ts
        )
        self.assertTrue(pin_success)

        message_ts = fake_slack_timestamp(self.faker)
        self.mock_client.pins_add.side_effect = SlackApiError(
            message="", response={"error": "already_pinned"}
        )
        self.assertFalse(
            self.slack_boss.pin_message_in_channel(channel_id=channel_id, ts=message_ts)
        )

        message_ts = fake_slack_timestamp(self.faker)
        self.mock_client.pins_add.side_effect = SlackApiError(
            message="", response={"error": "not_pinnable"}
        )
        self.assertFalse(
            self.slack_boss.pin_message_in_channel(channel_id=channel_id, ts=message_ts)
        )

        message_ts = fake_slack_timestamp(self.faker)
        self.mock_client.pins_add.side_effect = self.generic_slack_api_error
        with self.assertRaises(SlackBossException):
            self.slack_boss.pin_message_in_channel(channel_id=channel_id, ts=message_ts)
