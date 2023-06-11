from django.contrib import admin
from financeapp_tel.models import Transactions
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _
from django.urls import path
from django.urls import reverse
from django.utils.html import format_html

import csv
import datetime


class YearFilter(admin.SimpleListFilter):
    title = _('Year')
    parameter_name = 'year'

    def lookups(self, request, model_admin):
        years = Transactions.objects.dates('date', 'year')
        return [(year.year, year.year) for year in years]

    def queryset(self, request, queryset):
        if self.value():
            year = int(self.value())
            return queryset.filter(date__year=year)


class MonthFilter(admin.SimpleListFilter):
    title = _('Month')
    parameter_name = 'month'

    def lookups(self, request, model_admin):
        months = Transactions.objects.dates('date', 'month')
        return [(month.month, datetime.date(1900, month.month, 1).strftime('%B')) for month in months]

    def queryset(self, request, queryset):
        if self.value():
            month = int(self.value())
            return queryset.filter(date__month=month)


class TransactionsAdmin(admin.ModelAdmin):
    # your other admin configuration
    list_display = ('name', 'user', 'account', 'budget', 'date', 'type', 'amount', 'is_from_budget', 'delete_button')
    list_filter = (YearFilter, MonthFilter, 'user', 'account', 'budget', 'type')
    search_fields = ('name', 'user__username', 'account__name')
    ordering = ('-date',)
    actions = ['custom_action_1']

    change_list_template = "admin/change_list.html"

    def delete_button(self, obj):
        delete_url = reverse('admin:financeapp_tel_transactions_delete', args=[obj.pk])
        return format_html('<a class="deletion btn btn-danger" href="{}">Delete</a>', delete_url)
    delete_button.short_description = 'Delete'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('custom-action-1/', self.custom_action_1, name='custom_action_1'),
            # path('custom-action-2/', self.custom_action_2, name='custom_action_2'),
        ]
        return custom_urls + urls

    @admin.action(description="Export to CSV")
    def custom_action_1(self, request, queryset=None):
        if not queryset:
            # If no queryset is provided, get all objects of the model
            queryset = self.model.objects.all()

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    def save_model(self, request, obj, form, change):
        if not change:
            # New transaction, update the account balance accordingly
            if obj.type == 'income':
                obj.account.amount += obj.amount
            elif obj.type == 'expense':
                obj.account.amount -= obj.amount
        else:
            # Existing transaction, calculate the difference in the amount and update the account balance
            old_transaction = Transactions.objects.get(pk=obj.pk)
            amount_difference = obj.amount - old_transaction.amount
            if obj.type == 'income':
                obj.account.amount += amount_difference
            elif obj.type == 'expense' or obj.type == 'loan':
                obj.account.amount -= amount_difference

        obj.account.save()  # Save the updated account balance
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        if obj.type == 'income':
            obj.account.amount -= obj.amount
        elif obj.type == 'expense' or obj.type == 'loan':
            obj.account.amount += obj.amount

        obj.account.save()  # Save the updated account balance
        super().delete_model(request, obj)
