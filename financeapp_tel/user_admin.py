from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html


class CustomUserAdmin(UserAdmin):
    list_display = ('custom_profile_pic', 'username', 'email', 'first_name', 'last_name', 'custom_actions')
    list_filter = ('is_staff', 'is_superuser', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    actions = ['edit_selected', 'delete_selected']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.extra(
            select={'custom_actions': "''"},
            select_params=[],
            where=[],
            params=[],
            tables=[],
            order_by=[]
        )
        return queryset

    @staticmethod
    def custom_profile_pic(obj):
        if obj.profilePic:
            return format_html(
                '<div style="width: 60px; height: 29px; border-radius: 50%; overflow: hidden;"><img  class="img-circle elevation-2" src="{}" '
                'alt="Profile Pic" style="width: 100%; height: 100%; object-fit: cover;"></div>',
                obj.profilePic.url
            )
        else:
            return mark_safe(
                '<div style="width: 60px; height: 60px; border-radius: 50%; background-color: lightgray;"></div>'
            )

    def custom_actions(self, obj):
        return format_html(
            '<a class="btn btn-primary" href="{}">Edit</a> '
            '<a class="btn btn-danger" href="{}">Delete</a>',
            reverse('admin:financeapp_tel_user_change', args=[obj.pk]),  # Edit URL
            reverse('admin:financeapp_tel_user_delete', args=[obj.pk]),  # Delete URL
        )

    custom_profile_pic.short_description = 'Profile Pic'
    custom_actions.short_description = 'Actions'
    custom_actions.allow_tags = True
    custom_actions.admin_order_field = 'custom_actions'
