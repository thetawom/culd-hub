from django.conf import settings
from slack_sdk import WebClient


class SlackBoss(object):
    instance = None

    def __new__(cls):
        if not cls.instance:
            cls.instance = super(SlackBoss, cls).__new__(cls)
            cls.instance.client = WebClient(token=settings.SLACK_TOKEN)
        return cls.instance

    def create_channel(self, info):
        response = self.client.conversations_create(name=info.name.replace(" ", "-").lower(), is_private=False)
        info.channel_id = response["channel"]["id"]
        info.save()

    def create_show_info(self, info):
        d = "TBD"
        if info.time:
            d = info.time.strftime("%I:%M %p")
        block = [
            {
                "type": "section",
                "text": {
                    "text": "*Show Information*",
                    "type": "mrkdwn",
                },
                "fields": [
                    {"type": "mrkdwn", "text": "*Date:* " + str(info.date)},
                    {"type": "mrkdwn", "text": "*Time:* " + d},
                    {
                        "type": "mrkdwn",
                        "text": "*Point Person:* " + str(info.point),
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Lions:* " + str(info.lions),
                    },
                ],
            }
        ]
        return block
        # return self.client.chat_postMessage(channel=info.channel_id, blocks=block)

    def post_show_info(self, info):
        block = self.create_show_info(info)
        response = self.client.chat_postMessage(channel=info.channel_id, blocks=block)
        print(response)
        return response

    def update_show_info(self, info, message):
        block = self.create_show_info(info)
        print(block)
        print(info.channel_id)
        return self.client.chat_update(channel=info.channel_id, ts=message.ts, blocks=block)
