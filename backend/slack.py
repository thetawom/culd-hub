from django.conf import settings
from slack_sdk import WebClient


class SlackBoss(object):
    instance = None

    def __new__(cls):
        if not cls.instance:
            cls.instance = super(SlackBoss, cls).__new__(cls)
            cls.instance.client = WebClient(token=settings.SLACK_TOKEN)
        return cls.instance

    def create_channel(self, name):
        return self.client.conversations_create(name=name, is_private=False)

    def post_message(self, channel, blocks):
        return self.client.chat_postMessage(channel=channel, blocks=blocks)
