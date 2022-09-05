from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver

from common.decorators import disable_for_loaddata
from shows.models import Member, Round, Show

User = get_user_model()


@receiver(post_save, sender=User)
def create_member_for_user(sender, instance, created, **kwargs):
    if created:
        Member.objects.create(user=instance)


@receiver(post_save, sender=Round)
@receiver(post_delete, sender=Round)
def update_show_time(sender, instance, **kwargs):
    rounds = instance.show.rounds.all()
    instance.show.time = min(r.time for r in rounds) if rounds else None
    instance.show.save()


@receiver(post_delete, sender=Member)
def delete_user_for_member(sender, instance, **kwargs):
    try:
        User.objects.filter(id=instance.user.id).delete()
    except ObjectDoesNotExist:
        pass


@receiver(pre_save, sender=Show)
@disable_for_loaddata
def clean_show(sender, instance, **kwargs):
    instance.full_clean()
