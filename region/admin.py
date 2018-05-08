from django.contrib import admin

from region.models import Province, Regency


class ProvinceAdmin(admin.ModelAdmin):
    search_fields = ('name', )

    def has_module_permission(self, request):
        return False


class RegencyAdmin(admin.ModelAdmin):
    search_fields = ('name', )

    def has_module_permission(self, request):
        return False


admin.site.register(Province, ProvinceAdmin)
admin.site.register(Regency, RegencyAdmin)
