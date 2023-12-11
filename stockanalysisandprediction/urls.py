# urls.py
from django.contrib import admin
from django.urls import path
from django.views.decorators.cache import cache_page

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
    path("stocks/", cache_page(60 * 15)(stock_name_list), name="stock-name-list"),
    path("stocks/<str:ticker>/", cache_page(60 * 15)(stock_detail), name="stock-detail"),
    path(
        "api/getDailyReturns/<str:stock_ticker>/",
        cache_page(60 * 15)(getDailyReturnsApi),
        name="get-daily-returns-api",
    ),
    path(
        "api/getDailyPriceChange/<str:stock_ticker>/",
        cache_page(60 * 15)(getDailyPriceChangeApi),
        name="get-daily-price-change-api",
    ),
    path(
        "api/getDailyPriceRange/<str:stock_ticker>/",
        cache_page(60 * 15)(getDailyPriceRangeApi),
        name="get-daily-price-range-api",
    ),
    path(
        "api/getDailyPriceGap/<str:stock_ticker>/",
        cache_page(60 * 15)(getDailyPriceGapApi),
        name="get-daily-price-gap-api",
    ),
    path(
        "api/getYearlyPerformance/<str:stock_ticker>/",
        cache_page(60 * 15)(getYearlyPerformanceApi),
        name="get-yearly-performance-api",
    ),
    path(
        "api/getRawAnalyticData/<str:stock_ticker>/<str:raw_analytic>/",
        cache_page(60 * 15)(getRawAnalyticDataApi),
        name="get-raw-analytic-data-api",
    ),
    path(
        "api/getAnalyticData/<str:stock_ticker>/<str:analytic>/",
        cache_page(60 * 15)(getAnalyticDataApi),
        name="get-analytic-data-api",
    ),
    path(
        "api/getMovingAverages/<str:stock_ticker>/<str:analytic>/",
        cache_page(60 * 15)(getMovingAveragesApi),
        name="get-moving-averages-api",
    ),
    path("api/getRankings/<str:analytic>/",
         cache_page(60 * 15)(getRankingsApi),
         name="get-rankings-api"),
    path(
        "api/getLongestContinuousTrends/<str:stock_ticker>/<str:analytic>/",
        cache_page(60 * 15)(getLongestContinuousTrendsApi),
        name="get-longest-continuous-trends-api",
    ),
    path(
        "api/getCorrelationAnalytics/<str:stock_ticker>/<str:analytic>/",
        cache_page(60 * 15)(getCorrelationAnalyticsApi),
        name="get-correlation-analytics-api",
    ),
    path(
        "api/getPrediction/<str:stock_ticker>",
        cache_page(60 * 15)(makePrediction),
        name="make-prediction"
    ),
]
