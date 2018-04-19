# TODO:
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import (
    ObjectDoesNotExist, MultipleObjectsReturned, ValidationError
)
from django.db import models


class User(AbstractUser):
    def get_account(self):
        if self.is_regionaladmin and self.is_participant:
            raise MultipleObjectsReturned("User can't be both a RegionalAdmin "
                                          "and a Participant")
        elif self.is_regionaladmin:
            return self.regionaladmin
        elif self.is_participant:
            return self.participant
        else:
            raise ObjectDoesNotExist("User is neither a RegionalAdmin nor a "
                                     "Participant")

    @property
    def is_regionaladmin(self):
        return (hasattr(self, 'regionaladmin')
                and self.regionaladmin is not None)

    @property
    def is_participant(self):
        return (hasattr(self, 'participant')
                and self.participant is not None)


class BaseAccount(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return str(self.user)


class RegionalAdmin(BaseAccount):
    region = models.ForeignKey('main.Province', on_delete=models.CASCADE)

    def clean(self):
        if self.user.id and self.user.is_participant:
            raise ValidationError({
                'user': "User already registered as a Participant."
            })

    class Meta:
        verbose_name = "regional admin"
        verbose_name_plural = "regional admins"


class Participant(BaseAccount):
    def clean(self):
        if self.user.id and self.user.is_regionaladmin:
            raise ValidationError({
                'user': "User already registered as a RegionalAdmin."
            })

    class Meta:
        verbose_name = "participant"
        verbose_name_plural = "participants"
