from django.contrib import admin
from django.template.defaultfilters import truncatewords
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from dynamic_preferences.admin import GlobalPreferenceAdmin, PerInstancePreferenceAdmin
from dynamic_preferences.models import GlobalPreferenceModel

from . import models


class OrganizationMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'member', 'organization', 'status', 'is_active', 'datetime')
    list_filter = ('member', 'organization', 'status', 'is_active')
    search_fields = ('member__first_name', 'member__last_name')


class OrganizationMemberOrgAdmin(admin.ModelAdmin):
    list_display = ('id', 'member_org', 'organization', 'status', 'is_active', 'datetime')
    list_filter = ('member_org', 'organization', 'status', 'is_active')


class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'phone', 'user', 'draft')
    search_fields = ('first_name', 'last_name')
    list_filter = ('email_verified', 'phone_verified')


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'website',)
    search_fields = ('name', 'website', 'email', 'phone')
    list_filter = ('type',)


class RaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'event', 'start_datetime',)
    search_fields = ('name', 'event__name')
    list_filter = ('event',)


class RaceResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'rider', 'race', 'place',)
    search_fields = ('race__name', 'rider__first_name', 'rider__last_name')
    list_filter = ('race',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'organization', 'create_by')
    search_fields = ('title',)
    list_filter = ('organization',)
    exclude = ('create_by',)

    def save_model(self, request, obj, form, change):
        if not change:
            obj.create_by = request.user
        super().save_model(request, obj, form, change)


class RaceSeriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'organization')
    search_fields = ('name',)
    list_filter = ('organization',)


class RaceSeriesResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'race_series', 'category', 'place',)
    search_fields = ('race_series__name',)
    list_filter = ('race_series',)


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start_date', 'end_date', 'country', 'city', 'state')
    search_fields = ('name',)


class FinancialTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'user', 'type', 'create_datetime')
    list_filter = ('type',)


class FieldsTrackingAdmin(admin.ModelAdmin):
    list_display = ('id', 'object_id', 'content_type', 'object_repr', 'datetime', 'user')
    search_fields = ('object_repr',)
    list_filter = ('content_type',)


class MyGlobalPreferenceAdmin(GlobalPreferenceAdmin):
    class Media:
        css = {
            'all': ('dj/admin/css/global_preferences.css',)
        }

    list_display = ('verbose_name', 'name', 'section_name', 'ellipsis_raw_value')

    def has_add_permission(self, request, obj=None):
        return False

    def ellipsis_raw_value(self, obj):
        return truncatewords(mark_safe(strip_tags(obj.raw_value or '')), 20)

    ellipsis_raw_value.short_description = "Raw Value"


admin.site.register(models.Member, MemberAdmin)
admin.site.register(models.Organization, OrganizationAdmin)
admin.site.register(models.OrganizationMember, OrganizationMemberAdmin)
admin.site.register(models.OrganizationMemberOrg, OrganizationMemberOrgAdmin)
admin.site.register(models.Race, RaceAdmin)
admin.site.register(models.RaceResult, RaceResultAdmin)
admin.site.register(models.RaceSeriesResult, RaceSeriesResultAdmin)
admin.site.register(models.FieldsTracking, FieldsTrackingAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.RaceSeries, RaceSeriesAdmin)
admin.site.register(models.Event, EventAdmin)
admin.site.register(models.FinancialTransaction, FinancialTransactionAdmin)

admin.site.unregister(GlobalPreferenceModel)
admin.site.register(GlobalPreferenceModel, MyGlobalPreferenceAdmin)
