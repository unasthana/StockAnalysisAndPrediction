# urls.py
from django.contrib import admin
from django.urls import path
from .views import (
    stock_detail,
    stock_name_list,
)
from .views_analytics import getDailyReturnsApi, getDailyPriceChangeApi, getDailyPriceRangeApi, getDailyPriceGapApi, \
    getYearlyPerformanceApi

urlpatterns = [
    path("admin/", admin.site.urls),
    path("stocks/", stock_name_list, name="stock-name-list"),
    path("stocks/<str:ticker>/", stock_detail, name="stock-detail"),
    path("api/getDailyReturns/<str:stock_ticker>/", getDailyReturnsApi, name="get-daily-returns"),
    path("api/getDailyPriceChange/<str:stock_ticker>/", getDailyPriceChangeApi, name="get-daily-price-change-api"),
    path("api/getDailyPriceRange/<str:stock_ticker>/", getDailyPriceRangeApi, name="get-daily-price-range-api"),
    path("api/getDailyPriceGap/<str:stock_ticker>/", getDailyPriceGapApi, name="get-daily-price-gap-api"),
    path("api/getYearlyPerformance/<str:stock_ticker>/", getYearlyPerformanceApi, name="get-yearly-performance-api"),
]
