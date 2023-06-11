from django.contrib import admin
from financeapp_tel.models import Accounts, Transactions, Loan, User
from financeapp_tel.transactions_admin import TransactionsAdmin
from financeapp_tel.user_admin import CustomUserAdmin
from django.contrib.auth.models import Group
from tabulate import tabulate


class LoanAdmin(admin.ModelAdmin):
    # your other admin configuration

    def save_model(self, request, obj, form, change):
        if not change:
            # New loan record, subtract the loan amount from the selected account
            account = Accounts.objects.get(user=obj.user)
            account.amount -= obj.installment_amount
            account.save()
        else:
            # Existing loan record, calculate the difference in the loan amount and update the account balance
            old_loan = Loan.objects.get(pk=obj.pk)
            amount_difference = obj.installment_amount - old_loan.installment_amount
            account = Accounts.objects.get(user=obj.user)
            if obj.installment_amount > old_loan.installment_amount:
                account.amount -= amount_difference
            else:
                account.amount -= amount_difference
            account.save()

        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        account = Accounts.objects.get(user=obj.user)
        account.amount += obj.installment_amount
        account.save()

        super().delete_model(request, obj)


class GroupAdmin(admin.ModelAdmin):
    def has_module_permission(self, request):
        return False


admin.site.register(User, CustomUserAdmin)
admin.site.unregister(Group)
admin.site.register(Group, GroupAdmin)
# admin.site.register(Category)
admin.site.register(Accounts)
admin.site.register(Transactions, TransactionsAdmin)
# admin.site.register(Budget)
admin.site.register(Loan, LoanAdmin)
# Register your models here.
