# urls.py
from django.contrib import admin
from django.urls import path

from .prediction import makePrediction
from .views import (
    stock_detail,
    stock_name_list,
)
from .views_analytics import (
    getDailyReturnsApi,
    getDailyPriceChangeApi,
    getDailyPriceRangeApi,
    getDailyPriceGapApi,
    getYearlyPerformanceApi,
    getRawAnalyticDataApi,
    getAnalyticDataApi,
    getMovingAveragesApi,
    getRankingsApi,
    getLongestContinuousTrendsApi,
    getCorrelationAnalyticsApi,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("stocks/", stock_name_list, name="stock-name-list"),
    path("stocks/<str:ticker>/", stock_detail, name="stock-detail"),
    path(
        "api/getDailyReturns/<str:stock_ticker>/",
        getDailyReturnsApi,
        name="get-daily-returns-api",
    ),
    path(
        "api/getDailyPriceChange/<str:stock_ticker>/",
        getDailyPriceChangeApi,
        name="get-daily-price-change-api",
    ),
    path(
        "api/getDailyPriceRange/<str:stock_ticker>/",
        getDailyPriceRangeApi,
        name="get-daily-price-range-api",
    ),
    path(
        "api/getDailyPriceGap/<str:stock_ticker>/",
        getDailyPriceGapApi,
        name="get-daily-price-gap-api",
    ),
    path(
        "api/getYearlyPerformance/<str:stock_ticker>/",
        getYearlyPerformanceApi,
        name="get-yearly-performance-api",
    ),
    path(
        "api/getRawAnalyticData/<str:stock_ticker>/<str:raw_analytic>/",
        getRawAnalyticDataApi,
        name="get-raw-analytic-data-api",
    ),
    path(
        "api/getAnalyticData/<str:stock_ticker>/<str:analytic>/",
        getAnalyticDataApi,
        name="get-analytic-data-api",
    ),
    path(
        "api/getMovingAverages/<str:stock_ticker>/<str:analytic>/",
        getMovingAveragesApi,
        name="get-moving-averages-api",
    ),
    path("api/getRankings/<str:analytic>/", getRankingsApi, name="get-rankings-api"),
    path(
        "api/getLongestContinuousTrends/<str:stock_ticker>/<str:analytic>/",
        getLongestContinuousTrendsApi,
        name="get-longest-continuous-trends-api",
    ),
    path(
        "api/getCorrelationAnalytics/<str:stock_ticker>/<str:analytic>/",
        getCorrelationAnalyticsApi,
        name="get-correlation-analytics-api",
    ),
    path(
        "api/getPrediction/<str:stock_ticker>", makePrediction, name="make-prediction"
    ),
]
