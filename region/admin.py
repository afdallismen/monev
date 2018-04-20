from django.contrib import admin

from region.models import Province, Regency


class ProvinceAdmin(admin.ModelAdmin):
    search_fields = ('name', )


class RegencyAdmin(admin.ModelAdmin):
    search_fields = ('name', )


admin.site.register(Province, ProvinceAdmin)
admin.site.register(Regency, RegencyAdmin)
