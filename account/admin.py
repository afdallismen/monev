from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from account.models import Participant, RegionalAdmin
from account.forms import (
    ParticipantCreationForm, ParticipantChangeForm, RegionalAdminCreationForm,
    RegionalAdminChangeForm
)


User = get_user_model()


class BaseAccountAdmin(admin.ModelAdmin):
    empty_value_display = "-"
    list_display = ('name', 'is_active')

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def name(self, acc):
        name = False
        if acc.user.first_name or acc.user.last_name:
            name = (str(acc.user.first_name), str(acc.user.last_name))
            name = ((word.lower()).capitalize() for word in name)
            name = " ".join(name)
        return name if name else "-username: {}-".format(acc.user.username)
    name.admin_order_field = 'user__first_name'

    def is_active(self, acc):
        return acc.user.is_active
    is_active.boolean = True
    is_active.admin_order_field = 'user__is_active'


class ParticipantAdmin(BaseAccountAdmin):
    form = ParticipantChangeForm
    add_form = ParticipantCreationForm


class RegionalAdminAdmin(BaseAccountAdmin):
    form = RegionalAdminChangeForm
    add_form = RegionalAdminCreationForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_display = self.list_display + ('region_display', )

    def region_display(self, acc):
        # Convert all caps to title case
        region = (str(acc.get_region_display()).lower()).split()
        region = (word.capitalize() for word in region)
        region = " ".join(region)

        return region
    region_display.short_description = "region"


admin.site.register(RegionalAdmin, RegionalAdminAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.unregister(Group)
