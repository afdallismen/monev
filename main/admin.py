import nested_admin

from django.contrib import admin

from main.models import (
    Diklat, Questionnaire, Topic, Question, Option, Measure, Response,
    Recommendation
)


class DiklatAdmin(admin.ModelAdmin):
    autocomplete_fields = ['province', 'regencies']
    search_fields = ['title']
    list_display = ('__str__', 'date', 'duration_display',
                    'num_of_participant', 'supervisor', 'location')
    # regencies need custom list filter
    list_filter = ['province', 'regencies']
    date_hierarchy = 'date'

    def duration_display(self, obj):
        return "{!s} days".format(obj.duration)
    duration_display.short_description = "duration"
    duration_display.admin_order_field = "duration"


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
    list_display = ('__str__', 'instrument')
    list_filter = ['diklat']
    date_hierarchy = 'diklat__date'


def question_display(obj):
    if len(str(obj.question)) > 40:
        return "{}...".format(str(obj.question)[:40])
    return str(obj.title)
question_display.short_description = "question"  # noqa


class RecommendationAdmin(admin.ModelAdmin):
    search_fields = [
        'respondent__user__first_name',
        'respondent__user__last_name',
    ]
    list_display = ('title_display', question_display, 'respondent')
    # add questionnaire list filter

    def title_display(self, obj):
        if len(str(obj.text)) > 15:
            return "{}...".format(str(obj.text)[:15])
        return str(obj.title)
    title_display.short_description = "recommendation"
    title_display.admin_order_field = "pk"


class ResponseAdmin(admin.ModelAdmin):
    search_fields = [
        'respondent__user__first_name',
        'respondent__user__last_name',
    ]
    # create a response with text
    list_display = ('response_display', 'respondent', question_display,
                    'measure', 'selected', 'text')

    def response_display(self, obj):
        return "!icon here"  # change this with link icon


admin.site.register(Diklat, DiklatAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Recommendation, RecommendationAdmin)
admin.site.register(Response, ResponseAdmin)
