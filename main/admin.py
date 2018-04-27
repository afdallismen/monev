import nested_admin

from django.contrib import admin

from main.models import (
    Diklat, Questionnaire, Topic, Question, Parameter, Aspect, Response,
    Recommendation
)


class DiklatAdmin(admin.ModelAdmin):
    autocomplete_fields = ('province', 'regency')
    list_display = ('title_display', 'province', 'location', 'date')
    list_filter = ('date', 'province')
    search_fields = ['title', 'province__name']
    date_hierarchy = 'date'

    def title_display(self, obj):
        return str(obj.title).title()
    title_display.short_description = "title"
    title_display.admin_order_field = 'title'


class ParameterInline(nested_admin.NestedTabularInline):
    model = Parameter
    extra = 0


class AspectInline(nested_admin.NestedTabularInline):
    model = Aspect
    extra = 0


class QuestionInline(nested_admin.NestedTabularInline):
    model = Question
    inlines = [ParameterInline, AspectInline]
    extra = 0


class TopicInline(nested_admin.NestedStackedInline):
    model = Topic
    inlines = [QuestionInline]
    extra = 0


class QuestionnaireAdmin(nested_admin.NestedModelAdmin):
    inlines = [TopicInline]


class TopicAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline]


class QuestionAdmin(nested_admin.NestedModelAdmin):
    inlines = [ParameterInline, AspectInline]


class BasicAdmin(admin.ModelAdmin):
    pass


admin.site.register(Diklat, DiklatAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Question, QuestionAdmin)

models = [Parameter, Aspect, Response, Recommendation]

for model in models:
    admin.site.register(model, BasicAdmin)
