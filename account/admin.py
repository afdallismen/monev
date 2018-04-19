# TODO:
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.models import Group

# This dependency copied from django.contrib.auth.admin
from django.contrib import messages
from django.contrib.admin.options import IS_POPUP_VAR
from django.contrib.admin.utils import unquote
from django.contrib.auth import update_session_auth_hash
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import escape
from django.utils.translation import gettext, gettext_lazy as _
# end of copied dependency

from account.models import Participant, RegionalAdmin
from account.forms import (
    ParticipantCreationForm, ParticipantChangeForm, RegionalAdminCreationForm,
    RegionalAdminChangeForm
)


User = get_user_model()


class BaseAccountAdmin(admin.ModelAdmin):
    empty_value_display = "-"
    list_display = ('name', 'is_active')
    change_user_password_template = None
    change_password_form = AdminPasswordChangeForm

    # This method is copied from django.contrib.auth.admin
    def get_urls(self):
        return [
            path(
                '<id>/password/',
                self.admin_site.admin_view(self.user_change_password),
                name='auth_user_password_change',
            ),
        ] + super().get_urls()

    # This method is copied from django.contrib.auth.admin
    def user_change_password(self, request, id, form_url=''):
        if not self.has_change_permission(request):
            raise PermissionDenied
        acc = self.get_object(request, unquote(id))
        user = acc.user
        if user is None:
            raise Http404(_("%(name)s object with primary key %(key)r does not exist.").format({  # noqa
                'name': user._meta.verbose_name,
                'key': escape(id),
            }))
        if request.method == 'POST':
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                change_message = self.construct_change_message(
                    request,
                    form,
                    None
                )
                self.log_change(request, user, change_message)
                msg = gettext("Password changed successfully.")
                messages.success(request, msg)
                update_session_auth_hash(request, form.user)
                # Redirect to account changelist
                return HttpResponseRedirect(
                    reverse(
                        '%s:%s_%s_change' % (
                            self.admin_site.name,
                            acc._meta.app_label,
                            acc._meta.model_name,
                        ),
                        args=(acc.pk,),
                    )
                )
        else:
            form = self.change_password_form(user)

        fieldsets = [(None, {'fields': list(form.base_fields)})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        context = {
            'title': _("Change password: %s") % escape(user.get_username()),
            'adminForm': adminForm,
            'form_url': form_url,
            'form': form,
            'is_popup': (IS_POPUP_VAR in request.POST or
                         IS_POPUP_VAR in request.GET),
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True,
        }
        context.update(self.admin_site.each_context(request))

        request.current_app = self.admin_site.name

        return TemplateResponse(
            request,
            self.change_user_password_template or
            'admin/auth/user/change_password.html',
            context,
        )

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = self.add_form
        defaults.update(kwargs)
        return super().get_form(request, obj, **defaults)

    def name(self, acc):
        name = False
        if acc.user.first_name or acc.user.last_name:
            name = (acc.user.first_name, acc.user.last_name)
            name = ((str(word).lower()).capitalize() for word in name)
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
