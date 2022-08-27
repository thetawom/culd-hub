from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from ..decorators import disable_for_loaddata
from ..models import Member, Round, Show

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


@receiver(post_save, sender=Show)
@disable_for_loaddata
def create_channel_for_show(sender, instance, **kwargs):
    if instance.is_published and instance.channel_id == "" and instance.time:
        d = instance.time.strftime("%I:%M %p")
        response = instance.slack_boss.create_channel(
            instance.name.replace(" ", "-").lower()
        )
        instance.channel_id = response["channel"]["id"]
        instance.save()
        instance.slack_boss.post_message(
            instance.channel_id,
            [
                {
                    "type": "section",
                    "text": {
                        "text": "A message *with some bold text* and _some italicized text_.",
                        "type": "mrkdwn",
                    },
                    "fields": [
                        {"type": "mrkdwn", "text": "*Date:* " + str(instance.date)},
                        {"type": "mrkdwn", "text": "*Time:* " + d},
                        {
                            "type": "mrkdwn",
                            "text": "*Point Person:* " + str(instance.point),
                        },
                        {
                            "type": "mrkdwn",
                            "text": "*Lions:* " + str(instance.lions),
                        },
                    ],
                }
            ],
        )
