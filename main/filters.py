from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class RegenciesListFilter(admin.SimpleListFilter):
    title = _("regencies")
    parameter_name = "regency"

    def lookups(self, request, model_admin):
        qs = model_admin.get_queryset(request)
        qs = qs.filter()
