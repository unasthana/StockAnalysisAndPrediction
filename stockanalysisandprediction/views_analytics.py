from django.http import JsonResponse
from rest_framework.decorators import api_view
from .analytics import (
    getDailyReturns,
    getDailyPriceGap,
    getDailyPriceChange,
    getDailyPriceRange,
    getCorrelationAnalytics,
    getRankings,
    getMovingAverages,
    getYearlyPerformance,
    getLongestContinuousTrends,
    getAnalyticData,
    getRawAnalyticData,
)


@api_view(["GET"])
def getDailyReturnsApi(request, stock_ticker):
    time = request.GET.get("time", "all_time")
    return JsonResponse(str(getDailyReturns(stock_ticker, time)), safe=False)


def getDailyPriceChangeApi(request, stock_ticker):
    time = request.GET.get('time', 'all_time')
    return JsonResponse(str(getDailyPriceChange(stock_ticker, time)), safe=False)


def getDailyPriceRangeApi(request, stock_ticker):
    time = request.GET.get('time', 'all_time')
    return JsonResponse(str(getDailyPriceRange(stock_ticker, time)), safe=False)


def getDailyPriceGapApi(request, stock_ticker):
    time = request.GET.get('time', 'all_time')
    data = getDailyPriceGap(stock_ticker, time)
    return JsonResponse(str(data), safe=False)


def getYearlyPerformanceApi(request, stock_ticker):
    data = getYearlyPerformance(stock_ticker)
    return JsonResponse(str(data), safe=False)


def getRawAnalyticDataApi(request, stock_ticker, raw_analytic):
    time = request.GET.get('time', 'all_time')
    data = getRawAnalyticData(stock_ticker, raw_analytic, time)
    return JsonResponse(str(data), safe=False)


def getAnalyticDataApi(request, stock_ticker, analytic):
    time = request.GET.get('time', 'all_time')
    ma_analytic = request.GET.get('ma_analytic', 'NA')
    ma_window = request.GET.get('ma_window', 'NA')
    data = getAnalyticData(analytic, stock_ticker, time, ma_analytic, ma_window)
    return JsonResponse(str(data), safe=False)


def getMovingAveragesApi(request, stock_ticker, analytic):
    ma_window = request.GET.get('ma_window', '3_day')
    time = request.GET.get('time', 'all_time')
    data = getMovingAverages(stock_ticker, analytic, ma_window, time)
    return JsonResponse(str(data), safe=False)


def getRankingsApi(request, analytic):
    top_n = request.GET.get('top_n', 'top_10')
    time = request.GET.get('time', 'all_time')
    ma_analytic = request.GET.get('ma_analytic', 'NA')
    ma_window = request.GET.get('ma_window', 'NA')
    data = getRankings(analytic, top_n, time, ma_analytic, ma_window)
    return JsonResponse(str(data), safe=False)


def getLongestContinuousTrendsApi(request, stock_ticker, analytic):
    time = request.GET.get('time', 'all_time')
    ma_window = request.GET.get('ma_window', 'NA')
    ma_analytic = request.GET.get('ma_analytic', 'NA')
    data = getLongestContinuousTrends(stock_ticker, analytic, time, ma_window, ma_analytic)
    return JsonResponse(str(data), safe=False)


def getCorrelationAnalyticsApi(request, stock_ticker, analytic):
    time = request.GET.get('time', 'all_time')
    ma_analytic = request.GET.get('ma_analytic', 'NA')
    ma_window = request.GET.get('ma_window', 'NA')
    data = getCorrelationAnalytics(stock_ticker, analytic, time, ma_analytic, ma_window)
    return JsonResponse(str(data), safe=False)