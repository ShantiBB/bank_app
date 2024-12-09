from django.contrib import admin

from accounts.models import Account


@admin.register(Account)
class TransactionAdmin(admin.ModelAdmin):
    pass
