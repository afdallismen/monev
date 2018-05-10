from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountConfig(AppConfig):
    name = 'account'
    verbose_name = _("account")

    def ready(self):
        import account.signals  # noqa
