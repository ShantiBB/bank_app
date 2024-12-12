from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from .models import Transaction
from services.utils import delete_transaction_cache, delete_account_cache


@receiver(post_save, sender=Transaction)
def delete_transaction_cache_after_save(sender, instance, **kwargs):
    user_id = instance.account.owner.id
    delete_transaction_cache(instance.id, user_id)
    delete_account_cache(instance.account.id, user_id)


@receiver(post_delete, sender=Transaction)
def delete_transaction_after_delete(sender, instance, **kwargs):
    user_id = instance.account.owner.id
    delete_transaction_cache(instance.id, user_id)
