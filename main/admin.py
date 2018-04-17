from django.contrib import admin

from main.models import Diklat, Questionnaire, Topic, Question


class DiklatAdmin(admin.ModelAdmin):
    pass


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
