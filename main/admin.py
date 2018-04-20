import nested_admin

from django.contrib import admin

from easy_select2 import select2_modelform

from main.forms import QuestionForm
from main.models import Diklat, Questionnaire, Topic, Question


DiklatForm = select2_modelform(Diklat, attrs={'width': '300px'})


class DiklatAdmin(admin.ModelAdmin):
    form = DiklatForm
    list_display = ('title_display', 'province', 'location', 'date')
    list_filter = ('province', 'date')

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
    list_display = ('diklat', 'instrument')
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
