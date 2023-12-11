from django.contrib import admin
from .models import Stock, CompanyInfo, APICache


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "open", "high", "low", "close", "volume")
    list_filter = ("name", "date")
    search_fields = ("name",)


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ("ticker", "sector")
    search_fields = ("ticker", "sector")


@admin.register(APICache)
class APICacheAdmin(admin.ModelAdmin):
    list_display = ("api_name", "params")
    search_fields = ("api_name", "params")
    readonly_fields = ("api_name", "params", "response")

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True
