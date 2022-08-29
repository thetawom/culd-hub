from django.conf import settings
from slack_sdk import WebClient


class SlackBoss(object):
    def __init__(self):
        self.client = WebClient(token=settings.SLACK_TOKEN)

    @staticmethod
    def _get_channel_name(show):
        return f"{show.date.strftime('%m-%d')}-{show.name.replace(' ', '-').lower()}"

    def create_channel(self, show):
        response = self.client.conversations_create(
            name=self._get_channel_name(show), is_private=False
        )
        print(response)
        show.channel_id = response["channel"]["id"]
        show.save()
        return response

    @staticmethod
    def _create_briefing(show):
        time = show.time.strftime("%I:%M %p") if show.time else "TBD"
        briefing = [
            {
                "type": "section",
                "text": {
                    "text": "*Show Information*",
                    "type": "mrkdwn",
                },
                "fields": [
                    {"type": "mrkdwn", "text": "*Date:* " + str(show.date)},
                    {"type": "mrkdwn", "text": "*Time:* " + time},
                    {
                        "type": "mrkdwn",
                        "text": "*Point Person:* " + str(show.point),
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Lions:* " + str(show.lions),
                    },
                ],
            }
        ]
        return briefing

    def send_briefing(self, show):
        briefing = self._create_briefing(show)
        response = self.client.chat_postMessage(
            channel=show.channel_id, blocks=briefing
        )
        print(response)
        return response

    def update_briefing(self, show, message):
        block = self._create_briefing(show)
        response = self.client.chat_update(
            channel=show.channel_id, ts=message.ts, blocks=block
        )
        print(response)
        return response


slack_boss = SlackBoss()
