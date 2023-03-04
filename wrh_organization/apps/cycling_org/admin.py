import traceback

from django.conf import settings
from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.template.defaultfilters import truncatewords
from django.urls import path
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from dynamic_preferences.admin import GlobalPreferenceAdmin
from dynamic_preferences.models import GlobalPreferenceModel

from wrh_organization.helpers.utils import admin_url_wrap, USACApi
from . import models


class OrganizationMemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'member', 'organization', 'status', 'is_active', 'is_admin')
    list_filter = ('member', 'organization', 'status', 'is_active', 'is_admin', 'is_master_admin')
    search_fields = ('member__first_name', 'member__last_name', 'organization')


class OrganizationMemberOrgAdmin(admin.ModelAdmin):
    list_display = ('id', 'member_org', 'organization', 'status', 'is_active', 'datetime')
    list_filter = ('member_org', 'organization', 'status', 'is_active')


class MemberAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email', 'usac_license_number', 'user', 'draft')
    search_fields = ('first_name', 'last_name', 'usac_license_number', 'email')
    list_filter = ('email_verified', 'phone_verified')
    change_form_template = "admin/cycling_org/member_changeform.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('<int:object_id>/validate-usac-license/', admin_url_wrap(self.validate_usac_license, self.admin_site, self),
                 name="cycling_org_member_validate_usac_license"),
        ]
        return my_urls + urls

    def validate_usac_license(self, request, *args, **kwargs):
        object_id = kwargs.get('object_id')
        obj = self.get_object(request, object_id)
        if obj is None:
            return self._get_obj_does_not_exist_redirect(
                request, models.Member._meta, str(object_id)
            )
        if not obj.usac_license_number:
            self.message_user(request, '"usac_license_number" is not set for this member!', messages.WARNING)
            return redirect("..")
        if obj.usac_license_number_verified:
            self.message_user(request, '"usac_license_number" is already verified for this member!', messages.WARNING)
            return redirect("..")

        if request.method == "POST":
            obj.usac_license_number_verified = True
            obj.save(update_fields=['usac_license_number_verified'])
            self.message_user(request, f'"usac_license_number" verified for "{obj}" successfully.')
            return redirect("..")

        error = None
        usac_object = None
        usac_api = USACApi({'user_id': settings.USAC_API_USERNAME, 'user_password': settings.USAC_API_PASSWORD})
        try:
            usac_object = usac_api.lookup(license=obj.usac_license_number)
            usac_object = usac_object[0] if usac_object else None
        except Exception as e:
            traceback.print_exc()
            error = str(e)
        if not usac_object:
            error = f'No record matched with this usac_license_number "{obj.usac_license_number}"!'
            matched = {}
        else:
            matched = {
                'name': (usac_object.get('profile_first_name') or '').lower() == f'{obj.first_name} {obj.last_name}'.lower(),
                'age': usac_object.get('profile_birthdate') == obj.age,
                'gender': (usac_object.get('profile_race_gender') or '').lower() == obj.get_gender_display().lower(),
            }
        context = {
            'object': obj,
            'usac_object': usac_object,
            'matched': matched,
            'error': error,
            **self.admin_site.each_context(request),
        }
        return render(
            request, "admin/cycling_org/member_validate_usac_license.html", context
        )


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'website',)
    search_fields = ('name', 'website', 'email', 'phone')
    list_filter = ('type',)


class RaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'event', 'start_datetime',)
    search_fields = ('name', 'event__name',)
    list_filter = ('event',)


class RaceResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'rider', 'race', 'place' )
    search_fields = ('race__name', 'rider__first_name', 'rider__last_name',)
    list_filter = ('race',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'organization', 'create_by',)
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
    list_display = ('id', 'name', 'start_date', 'is_usac_permitted', 'city', 'organization', 'shared_org_perms')
    search_fields = ('name', )
    list_filter = ('is_usac_permitted',)


class FinancialTransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'user', 'type', 'create_datetime')
    list_filter = ('type',)


class ExportHistoryAdmin(admin.ModelAdmin):
    list_display = ('type','user', 'exported_time')
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

    list_display = ('verbose_name', 'name', 'section_name', 'ellipsis_raw_value',)

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
admin.site.register(models.ExportHistory, ExportHistoryAdmin)

admin.site.unregister(GlobalPreferenceModel)
admin.site.register(GlobalPreferenceModel, MyGlobalPreferenceAdmin)
