import nested_admin

from django.contrib import admin

from main.forms import QuestionForm
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


class QuestionInline(nested_admin.NestedTabularInline):
    model = Question
    form = QuestionForm
    extra = 1


class TopicInline(nested_admin.NestedStackedInline):
    model = Topic
    inlines = [QuestionInline]
    extra = 0


class QuestionnaireAdmin(nested_admin.NestedModelAdmin):
    # list_display = ('__str__', 'diklat', 'instrument')
    # list_filter = ('diklat', )
    # inlines = [TopicInline]
    pass


class BasicAdmin(admin.ModelAdmin):
    pass


testModels = [Questionnaire, Topic, Question, Parameter, Aspect, Response,
              Recommendation]

admin.site.register(Diklat, DiklatAdmin)

for model in testModels:
    admin.site.register(model, BasicAdmin)
