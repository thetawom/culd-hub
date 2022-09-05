from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver

from common.decorators import disable_for_loaddata
from shows.models import Show, Member
from shows.slack import slack_boss


@receiver(pre_save, sender=Show)
@disable_for_loaddata
def get_updated_fields(sender, instance, **kwargs):
    original = Show.objects.filter(pk=instance.pk).first()
    instance._updated_fields = [
        field
        for field in ["name", "date", "time", "address", "lions"]
        if getattr(instance, field) != getattr(original, field, None)
    ]


@receiver(post_save, sender=Show)
@disable_for_loaddata
def create_or_update_channel_for_show(sender, instance, created, **kwargs):
    if instance.is_published:
        if not hasattr(instance, "channel"):
            slack_boss.create_channel(show=instance)
        updated_fields = getattr(instance, "_updated_fields", [])
        delattr(instance, "_updated_fields")
        if not created and ("name" in updated_fields or "date" in updated_fields):
            slack_boss.rename_channel(show=instance)
        if updated_fields:
            slack_boss.send_or_update_briefing(
                show=instance, update_fields=updated_fields
            )
    else:
        if hasattr(instance, "channel"):
            slack_boss.archive_channel(show=instance)


@receiver(post_save, sender=Member)
@disable_for_loaddata
def fetch_slack_user_for_new_member(sender, instance, created, **kwargs):
    if created:
        slack_boss.fetch_user(member=instance)


@receiver(pre_delete, sender=Show)
@disable_for_loaddata
def delete_channel_for_show(sender, instance, **kwargs):
    if hasattr(instance, "channel"):
        slack_boss.archive_channel(show=instance)
