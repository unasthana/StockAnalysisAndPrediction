# urls.py
from django.contrib import admin
from django.urls import path
from .views import (
    stock_detail,
    stock_name_list,
    # get_stock_tickers,
    # get_stock_data,
    daily_returns,
    daily_price_change,
    daily_price_range,
    daily_price_gap,
    yearly_performance,
    get_longest_continuous_trends,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("stocks/", stock_name_list, name="stock-name-list"),
    path("stocks/<str:ticker>/", stock_detail, name="stock-detail"),
    # path('api/tickers/', get_stock_tickers, name='get-stock-tickers'),
    # path('api/stocks/<str:stock_ticker>/', get_stock_data, name='get-stock-data'),
    path(
        "api/returns/<str:stock_ticker>/<str:time>/",
        daily_returns,
        name="daily-returns",
    ),
    path(
        "api/price-change/<str:stock_ticker>/<str:time>/",
        daily_price_change,
        name="daily-price-change",
    ),
    path(
        "api/price-range/<str:stock_ticker>/<str:time>/",
        daily_price_range,
        name="daily-price-range",
    ),
    path(
        "api/price-gap/<str:stock_ticker>/<str:time>/",
        daily_price_gap,
        name="daily-price-gap",
    ),
    path(
        "api/yearly-performance/<str:stock_ticker>/",
        yearly_performance,
        name="yearly-performance",
    ),
    path(
        "api/longest-continuous-trends/",
        get_longest_continuous_trends,
        name="longest-continuous-trends",
    ),
]
