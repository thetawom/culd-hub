from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver

from common.decorators import disable_for_loaddata
from shows.models import Show, Member, Role
from shows.slackboss import slack_boss


@receiver(pre_save, sender=Show)
@disable_for_loaddata
def get_updated_fields(sender, instance, **kwargs):
    original = Show.objects.filter(pk=instance.pk).first()
    updated_fields = [
        field
        for field in ["name", "date", "time", "address", "lions", "point"]
        if getattr(instance, field) != getattr(original, field, None)
    ]
    if "point" in updated_fields:
        instance._original_point = getattr(original, "point", None)
    instance._updated_fields = updated_fields


@receiver(post_save, sender=Show)
@disable_for_loaddata
def create_or_update_channel_for_show(sender, instance, **kwargs):
    if instance.is_published:
        created_channel = False
        if not hasattr(instance, "channel"):
            slack_boss.create_channel(show=instance)
            created_channel = True
        updated_fields = getattr(instance, "_updated_fields", [])
        if not created_channel and (
            "name" in updated_fields or "date" in updated_fields
        ):
            slack_boss.rename_channel(show=instance)
        if created_channel or updated_fields:
            slack_boss.send_or_update_briefing(
                show=instance, update_fields=updated_fields
            )
        if created_channel or "point" in updated_fields:
            original_point = getattr(instance, "_original_point", None)
            if original_point and original_point not in instance.performers.all():
                slack_boss.remove_member_from_channel(
                    show=instance, member=original_point
                )
            if hasattr(instance, "point"):
                slack_boss.invite_member_to_channel(
                    show=instance, member=instance.point
                )
    else:
        if hasattr(instance, "channel"):
            slack_boss.archive_channel(show=instance)
    for attr_name in ["_original_point", "_updated_fields"]:
        if hasattr(instance, attr_name):
            delattr(instance, attr_name)


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


@receiver(post_save, sender=Role)
@disable_for_loaddata
def invite_performer_to_show_channel(sender, instance, created, **kwargs):
    if created and hasattr(instance, "channel"):
        slack_boss.invite_member_to_channel(
            show=instance.show, member=instance.performer
        )


@receiver(pre_delete, sender=Role)
@disable_for_loaddata
def remove_performer_from_show_channel(sender, instance, **kwargs):
    slack_boss.remove_member_from_channel(show=instance.show, member=instance.performer)
