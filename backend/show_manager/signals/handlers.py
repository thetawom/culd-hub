import logging

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from slack_sdk.errors import SlackApiError

from ..decorators import disable_for_loaddata
from ..models import Member, Round, Show
from ..slack import slack_boss

logger = logging.getLogger(__name__)

User = get_user_model()


@receiver(post_save, sender=User)
def create_member_for_user(sender, instance, created, **kwargs):
    del sender, kwargs
    if created:
        Member.objects.create(user=instance)


@receiver(post_save, sender=Round)
@receiver(post_delete, sender=Round)
def update_show_time(sender, instance, **kwargs):
    del sender, kwargs
    rounds = instance.show.rounds.all()
    instance.show.time = min(r.time for r in rounds) if rounds else None
    instance.show.save()


@receiver(post_delete, sender=Member)
def delete_user_for_member(sender, instance, **kwargs):
    del sender, kwargs
    User.objects.filter(id=instance.user.id).delete()


@receiver(pre_save, sender=Show)
@disable_for_loaddata
def clean_show(sender, instance, **kwargs):
    instance.full_clean()


# Should be for modifying channel info?
@receiver(pre_save, sender=Show)
@disable_for_loaddata
def check_channel(sender, instance, **kwargs):
    if not kwargs.get("created", True):
        prev = Show.objects.get(id=instance.id)
        if not prev.channel.id != instance.channel.id:
            pass


# Should be for initially creating a channel
@receiver(post_save, sender=Show)
@disable_for_loaddata
def create_channel_for_show(sender, instance, **kwargs):
    if instance.is_published and instance.channel is None:
        logger.info(f"Creating channel for {instance} ...")
        try:
            slack_boss.create_channel(instance)
            slack_boss.send_briefing(instance)
        except SlackApiError as error:
            logger.info(f"Failed to create channel: {error}")


# @disable_for_loaddata
# @receiver(post_save, sender=Show)
# def create_channel_for_show(sender, instance, **kwargs):
#     print("KWARGS: ", kwargs.get("raw"))
#     print("KWARGS: ", kwargs.get("created"))
#     # Still doesn't work, need to figure out disable for loaddata
#     # if (kwargs.get("created", True)) and not kwargs.get("raw", False):
#     slack = instance.slack_boss
#     print("NAME: ", instance.name)
#     print("CHANNEL ID: ", instance.channel_id)
#     if instance.is_published and instance.channel_id == "":
#         slack.create_channel(instance)
#         message = slack.post_show_info(instance)
#     elif instance.channel_id != "":
#         print("THIS RUNS")
# slack.update_show_info(instance, message)
# slack.update_show_info(instance)
# elif instance.is_published and instance.channel_id != "":
#     print(instance.channel_id)
#     # slack.update_show_info(instance)
# @receiver(post_save, sender=Show)
# @disable_for_loaddata
# def create_channel_for_show(sender, instance, **kwargs):
#     if instance.is_published and instance.channel_id == "" and instance.time:
#         d = instance.time.strftime("%I:%M %p")
#         response = instance.slack_boss.create_channel(
#             instance.name.replace(" ", "-").lower()
#         )
#         instance.channel_id = response["channel"]["id"]
#         instance.save()
#         instance.slack_boss.post_message(
#             instance.channel_id,
#             [
#                 {
#                     "type": "section",
#                     "text": {
#                         "text": "A message *with some bold text* and _some italicized text_.",
#                         "type": "mrkdwn",
#                     },
#                     "fields": [
#                         {"type": "mrkdwn", "text": "*Date:* " + str(instance.date)},
#                         {"type": "mrkdwn", "text": "*Time:* " + d},
#                         {
#                             "type": "mrkdwn",
#                             "text": "*Point Person:* " + str(instance.point),
#                         },
#                         {
#                             "type": "mrkdwn",
#                             "text": "*Lions:* " + str(instance.lions),
#                         },
#                     ],
#                 }
#             ],
#         )
