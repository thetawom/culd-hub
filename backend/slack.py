import os
from slack_sdk import WebClient
from dotenv import load_dotenv

load_dotenv()

class SlackBoss(object):
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SlackBoss, cls).__new__(cls)
            cls.instance.client = WebClient(token=os.getenv("SLACK_TOKEN"))
        return cls.instance
    def create_channel(self, name):
        return self.client.conversations_create(
            name=name,
            is_private=False
        )
