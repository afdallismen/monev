from django.contrib import admin

from easy_select2 import select2_modelform

from main.models import Diklat, Questionnaire, Topic, Question


DiklatForm = select2_modelform(Diklat, attrs={'width': '300px'})


class DiklatAdmin(admin.ModelAdmin):
    form = DiklatForm


class QuestionnaireAdmin(admin.ModelAdmin):
    pass


class TopicAdmin(admin.ModelAdmin):
    pass


class QuestionAdmin(admin.ModelAdmin):
    pass


admin.site.register(Diklat, DiklatAdmin)
admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Question, QuestionAdmin)
