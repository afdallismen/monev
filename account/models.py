from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import (
    ObjectDoesNotExist, MultipleObjectsReturned, ValidationError
)
from django.db import models
from django.utils.translation import gettext_lazy as _

from region.models import Province, Regency


class User(AbstractUser):
    def get_account(self):
        if self.is_regionaladmin and self.is_respondent:
            raise MultipleObjectsReturned(
                _("User can't be both a RegionalAdmin and a Respondent."))
        elif self.is_regionaladmin:
            return self.regionaladmin
        elif self.is_respondent:
            return self.respondent
        else:
            raise ObjectDoesNotExist(
                _("User is neither a RegionalAdmin nor a Respondent."))

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
        return self.user.get_full_name().title()


class RegionalAdmin(BaseAccount):
    region = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        verbose_name=_("region"),
    )

    def clean(self):
        if hasattr(self, 'user') and self.user.is_respondent:
            raise ValidationError({
                'user': _("User already registered as a Repondent.")
            })

    class Meta:
        verbose_name = _("regional admin")
        verbose_name_plural = _("regional admins")


class Respondent(BaseAccount):
    GENDER_CHOICES = (
        ('m', _("Male")),
        ('f', _("Female")),
    )

    gender = models.CharField(
        _("gender"),
        max_length=1,
        choices=GENDER_CHOICES,
    )
    age = models.PositiveSmallIntegerField(_("age"))
    workplace = models.CharField(
        _("workplace"),
        max_length=100,
        blank=True,
        null=True,
    )
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        verbose_name=_("province"),
    )
    regency = models.ForeignKey(
        Regency,
        on_delete=models.CASCADE,
        verbose_name=_("regency"),
        blank=True,
        null=True,
    )
    position = models.CharField(
        _("position"),
        max_length=100,
        blank=True,
        null=True,
    )
    year_of_service = models.PositiveSmallIntegerField(
        _("year of service"),
        blank=True,
        null=True,
    )
    last_education = models.CharField(
        _("last education"),
        max_length=50,
        blank=True,
        null=True,
    )

    def clean(self):
        if hasattr(self, 'user') and self.user.is_regionaladmin:
            raise ValidationError({
                'user': _("User already registered as a RegionalAdmin.")
            })

    class Meta:
        verbose_name = _("respondent")
        verbose_name_plural = _("respondents")
