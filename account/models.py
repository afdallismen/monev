# TODO:
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import (
    ObjectDoesNotExist, MultipleObjectsReturned, ValidationError
)
from django.db import models

from region.models import Province


class User(AbstractUser):
    def get_account(self):
        if self.is_regionaladmin and self.is_respondent:
            raise MultipleObjectsReturned("User can't be both a RegionalAdmin "
                                          "and a Respondent.")
        elif self.is_regionaladmin:
            return self.regionaladmin
        elif self.is_respondent:
            return self.respondent
        else:
            raise ObjectDoesNotExist("User is neither a RegionalAdmin nor a "
                                     "Respondent.")

    @property
    def is_regionaladmin(self):
        return (hasattr(self, 'regionaladmin')
                and self.regionaladmin is not None)

    @property
    def is_respondent(self):
        return (hasattr(self, 'respondent')
                and self.respondent is not None)


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
    region = models.ForeignKey(Province, on_delete=models.CASCADE)

    def clean(self):
        if hasattr(self, 'user') and self.user.is_respondent:
            raise ValidationError({
                'user': "User already registered as a Repondent."
            })

    class Meta:
        verbose_name = "regional admin"
        verbose_name_plural = "regional admins"


class Respondent(BaseAccount):
    def clean(self):
        if hasattr(self, 'user') and self.user.is_regionaladmin:
            raise ValidationError({
                'user': "User already registered as a RegionalAdmin."
            })

    class Meta:
        verbose_name = "respondent"
        verbose_name_plural = "respondents"
