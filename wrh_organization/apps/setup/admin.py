from django.contrib import admin, messages
from apps.setup.models import FormsModel, Criteria, CustomView


class FormsModelAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name', )
    search_fields = ('name', )


admin.site.register(FormsModel, FormsModelAdmin)
admin.site.register(Criteria)
admin.site.register(CustomView)

