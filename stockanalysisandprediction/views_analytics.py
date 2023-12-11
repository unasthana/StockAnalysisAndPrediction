from rest_framework.decorators import api_view
from rest_framework.response import Response
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
)


@api_view(["GET"])
def getDailyReturnsApi(request, stock_ticker):
    stock_ticker = request.GET.get("stock_ticker")
    time = request.GET.get("time", "all_time")
    return Response(getDailyReturns(stock_ticker, time))


def getDailyPriceChangeApi(request, stock_ticker):
    time = request.GET.get('time', 'all_time')
    data = getDailyPriceChange(stock_ticker, time)
    return Response(data)


def getDailyPriceRangeApi(request, stock_ticker):
    time = request.GET.get('time', 'all_time')
    data = getDailyPriceRange(stock_ticker, time)
    return Response(data)


def getDailyPriceGapApi(request, stock_ticker):
    time = request.GET.get('time', 'all_time')
    data = getDailyPriceGap(stock_ticker, time)
    return Response(data)


def getYearlyPerformanceApi(request, stock_ticker):
    data = getYearlyPerformance(stock_ticker)
    return Response(data)
