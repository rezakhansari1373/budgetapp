from django.contrib import admin

from .models import Category, Transaction


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'type', 'icon']


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['date', 'type', 'category', 'amount', 'note', 'user']
    list_filter = ['type', 'category', 'date']
    search_fields = ['note']
