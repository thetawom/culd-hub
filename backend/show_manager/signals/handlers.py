import logging

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from django.dispatch import receiver

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


@receiver(pre_save, sender=Show)
@disable_for_loaddata
def create_or_update_channel_for_show(sender, instance, **kwargs):
    prev_instance = Show.objects.filter(pk=instance.pk).first()
    if instance.is_published:
        if not hasattr(instance, "channel"):
            slack_boss.create_channel(instance)
        if hasattr(instance, "channel"):
            if prev_instance and (
                instance.name != prev_instance.name
                or instance.date != prev_instance.date
            ):
                slack_boss.rename_channel(instance)
            update_fields = [
                field
                for field in ["date", "time", "address", "lions"]
                if getattr(instance, field) != getattr(prev_instance, field)
            ]
            slack_boss.send_or_update_briefing(instance, update_fields)
    else:
        if hasattr(instance, "channel"):
            slack_boss.archive_channel(instance)


@receiver(pre_delete, sender=Show)
@disable_for_loaddata
def delete_channel_for_show(sender, instance, **kwargs):
    if hasattr(instance, "channel"):
        slack_boss.archive_channel(instance)
