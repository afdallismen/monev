import nested_admin

from django.contrib.admin import AdminSite
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


from main.models import (
    Diklat, Questionnaire, Topic, Question, Option, Measure, Response,
    Recommendation, EssayResponse, ObjectiveResponse, GroupOfObjectiveResponse
)


class MainAdminSite(AdminSite):
    site_header = _("Evaluasi Dan Monitoring Diklat")


class DiklatAdmin(admin.ModelAdmin):
    autocomplete_fields = ['province', 'regencies']
    search_fields = ['title', 'province__name', 'regencies__name']
    list_display = ('__str__', 'date', 'duration_display', 'province',
                    'regencies_display', 'participants')
    list_filter = [
        ('province', admin.RelatedOnlyFieldListFilter),
        ('regencies', admin.RelatedOnlyFieldListFilter),
    ]
    date_hierarchy = 'date'

    def duration_display(self, obj):
        return _("{!s} days").format(obj.duration)
    duration_display.short_description = _("duration")
    duration_display.admin_order_field = 'duration'

    def regencies_display(self, obj):
        return ", ".join(obj.regencies.values_list('name', flat=True))
    regencies_display.short_description = _("regencies")

    def participants(self, obj):
        regencies = obj.regencies.values_list('name', flat=True)
        q = ",".join(regencies)
        url = reverse('admin:account_respondent_changelist')
        return format_html(
            '<a href="{}">Participants</a>',
            url + "?q={!s}".format(q),
        )
    participants.short_description = _("participants")

    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return (request.user.is_superuser or
                obj.province == request.user.regionaladmin.region)

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser


class MeasureInline(nested_admin.NestedTabularInline):
    model = Measure
    extra = 0


class OptionInline(nested_admin.NestedTabularInline):
    model = Option
    extra = 0


class QuestionInline(nested_admin.NestedTabularInline):
    model = Question
    extra = 0
    inlines = [MeasureInline, OptionInline]


class TopicInline(nested_admin.NestedStackedInline):
    model = Topic
    extra = 0
    inlines = [QuestionInline]


class QuestionnaireAdmin(nested_admin.NestedModelAdmin):
    inlines = [TopicInline]
    search_fields = ['diklat__title']
    list_display = ('__str__', 'instrument', 'diklat', 'respondents',
                    'responses', 'chart')
    list_filter = ['diklat']
    date_hierarchy = 'diklat__date'

    def has_change_permission(self, request, obj=None):
        return (request.user.is_superuser or
                obj.diklat.province == request.user.regionaladmin.region)

    def respondents(self, obj):
        regencies = obj.diklat.regencies.values_list('name', flat=True)
        q = ",".join(regencies)
        url = reverse('admin:account_respondent_changelist')
        return format_html(
            '<a href="{}">Respondents</a>',
            url + "?q={!s}".format(q),
        )
    respondents.short_description = _("respondents")

    def responses(self, obj):
        return format_html(
            "<a href='{}' target='blank'>Responses</a>",
            reverse('main:questionnaire_responses', kwargs={'pk': obj.pk})
        )
    responses.short_description = _("user responses")

    def chart(self, obj):
        return format_html(
            "<a href='{}' target='blank'>Chart</a>",
            reverse(
                'main:questionnaire_responses_chart', kwargs={'pk': obj.pk})
        )
    chart.short_description = _("user responses in chart")


def question_display(obj):
    if len(str(obj.question)) > 40:
        return "{}...".format(str(obj.question)[:40])
    else:
        return str(obj.question)
question_display.short_description = _("question")  # noqa


def topic_display(obj):
    return str(obj.question.topic).title()
topic_display.short_description = _("topic")  # noqa


class RecommendationAdmin(admin.ModelAdmin):
    search_fields = [
        'respondent__user__first_name',
        'respondent__user__last_name',
    ]
    list_display = (question_display, topic_display, 'respondent')
    list_filter = [
        ('question__topic__questionnaire', admin.RelatedOnlyFieldListFilter),
    ]

    # these permission return true for easy testing purpose
    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True


class ResponseAdmin(admin.ModelAdmin):
    search_fields = [
        'respondent__user__first_name',
        'respondent__user__last_name',
    ]
    # create a response with text
    list_display = ('__str__', 'respondent', 'type',
                    topic_display)

    # these permission return true for easy testing purpose
    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True


class BasicAdmin(admin.ModelAdmin):
    pass


admin.site.site_header = _("Administration")
admin.site.site_url = None

admin.site.register(Diklat, DiklatAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Recommendation, RecommendationAdmin)
# admin.site.register(Response, ResponseAdmin)

# models = [EssayResponse, ObjectiveResponse, GroupOfObjectiveResponse]
#
# for model in models:
#     admin.site.register(model, BasicAdmin)
