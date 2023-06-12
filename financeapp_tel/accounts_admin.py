from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html


class AccountsAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'bank', 'amount', 'delete_button')  # Fields to display in the table
    list_filter = ('bank',)  # Add filters for the 'bank' field if desired
    search_fields = ('user__username', 'name')  # Add search functionality for 'user' and 'name' fields

    def delete_button(self, obj):
        delete_url = reverse('admin:financeapp_tel_accounts_delete', args=[obj.pk])
        return format_html('<a class="deletion btn btn-danger" href="{}">Delete</a>', delete_url)

    delete_button.short_description = 'Actions'
