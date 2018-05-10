from django.db.models.signals import post_delete
from django.dispatch import receiver

from account.models import Respondent, RegionalAdmin

@receiver(post_delete, sender=Respondent)  # noqa
@receiver(post_delete, sender=RegionalAdmin)
def delete_user(sender, instance, *arg, **kwargs):
    if instance.user:
        instance.user.delete()
