from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from .models import Account
from services.utils import delete_account_cache


@receiver(post_save, sender=Account)
def delete_account_cache_after_save(sender, instance, **kwargs):
    delete_account_cache(instance.id, instance.owner.id)


@receiver(post_delete, sender=Account)
def delete_account_cache_after_delete(sender, instance, **kwargs):
    delete_account_cache(instance.id, instance.owner.id)
