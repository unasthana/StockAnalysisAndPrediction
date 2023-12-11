from django.contrib import admin
from .models import Stock, CompanyInfo


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'open', 'high', 'low', 'close', 'volume')
    list_filter = ('name', 'date')
    search_fields = ('name',)


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'sector')
    search_fields = ('ticker', 'sector')