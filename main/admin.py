import nested_admin

from django.contrib import admin

from main.models import (
    Diklat, Questionnaire, Topic, Question, Option, Measure, Response,
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


class BasicAdmin(admin.ModelAdmin):
    pass


admin.site.register(Diklat, DiklatAdmin)

models = [Questionnaire, Question, Option, Measure, Response, Recommendation,
          Topic]

for model in models:
    admin.site.register(model, BasicAdmin)
