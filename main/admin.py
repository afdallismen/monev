import nested_admin

from django.contrib import admin

from main.forms import QuestionForm
from main.models import Diklat, Questionnaire, Topic, Question


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
    list_display = ('__str__', 'diklat', 'instrument')
    list_filter = ('diklat', )
    inlines = [TopicInline]


class TopicAdmin(admin.ModelAdmin):
    list_display = ('questionnaire', 'title')
    list_filter = ('questionnaire', )


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('topic', 'text')
    list_filter = ('topic', )


admin.site.register(Diklat, DiklatAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Question, QuestionAdmin)
