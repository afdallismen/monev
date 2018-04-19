from django.contrib import admin

from easy_select2 import select2_modelform

from main.models import Diklat, Questionnaire, Topic, Question


DiklatForm = select2_modelform(Diklat, attrs={'width': '300px'})


class DiklatAdmin(admin.ModelAdmin):
    form = DiklatForm
    list_display = ('title', 'province')


class QuestionnaireAdmin(admin.ModelAdmin):
    list_display = ('diklat', 'instrument')


class TopicAdmin(admin.ModelAdmin):
    list_display = ('questionnaire', 'title')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('topic', 'text')


admin.site.register(Diklat, DiklatAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Question, QuestionAdmin)
