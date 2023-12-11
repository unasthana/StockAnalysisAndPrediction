import json

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
from .models import APICache


@api_view(["GET"])
def getDailyReturnsApi(request, stock_ticker):
    time = request.GET.get("time", "all_time")
    response = prepare_response(getDailyReturns(stock_ticker, time))
    keys = [
        "result_df",
        "max_result",
        "max_date",
        "min_result",
        "min_date",
        "avg_result",
    ]
    return JsonResponse(dict(zip(keys, response)), safe=False)


def getDailyPriceChangeApi(request, stock_ticker):
    time = request.GET.get("time", "all_time")
    response = prepare_response(getDailyPriceChange(stock_ticker, time))
    keys = [
        "result_df",
        "max_result",
        "max_date",
        "min_result",
        "min_date",
        "avg_result",
    ]
    return JsonResponse(dict(zip(keys, response)), safe=False)


def getDailyPriceRangeApi(request, stock_ticker):
    time = request.GET.get("time", "all_time")
    response = prepare_response(getDailyPriceRange(stock_ticker, time))
    keys = [
        "result_df",
        "max_result",
        "max_date",
        "min_result",
        "min_date",
        "avg_result",
    ]
    return JsonResponse(dict(zip(keys, response)), safe=False)


def getDailyPriceGapApi(request, stock_ticker):
    time = request.GET.get("time", "all_time")
    response = prepare_response(getDailyPriceGap(stock_ticker, time))
    keys = [
        "result_df",
        "max_result",
        "max_date",
        "min_result",
        "min_date",
        "avg_result",
    ]
    return JsonResponse(dict(zip(keys, response)), safe=False)


def getYearlyPerformanceApi(request, stock_ticker):
    data = getYearlyPerformance(stock_ticker)
    response = prepare_response(getYearlyPerformance(stock_ticker))
    keys = [
        "result_df",
        "max_result",
        "max_date",
        "min_result",
        "min_date",
        "avg_result",
    ]
    return JsonResponse(dict(zip(keys, response)), safe=False)


def getRawAnalyticDataApi(request, stock_ticker, raw_analytic):
    time = request.GET.get("time", "all_time")
    response = prepare_response(getRawAnalyticData(stock_ticker, raw_analytic, time))
    keys = [
        "result_df",
        "max_result",
        "max_date",
        "min_result",
        "min_date",
        "avg_result",
    ]
    return JsonResponse(dict(zip(keys, response)), safe=False)


def getAnalyticDataApi(request, stock_ticker, analytic):
    time = request.GET.get("time", "all_time")
    ma_analytic = request.GET.get("ma_analytic", "NA")
    ma_window = request.GET.get("ma_window", "NA")
    response = prepare_response(
        getAnalyticData(analytic, stock_ticker, time, ma_analytic, ma_window)
    )
    keys = [
        "result_df",
        "max_result",
        "max_date",
        "min_result",
        "min_date",
        "avg_result",
    ]
    return JsonResponse(dict(zip(keys, response)), safe=False)


def getMovingAveragesApi(request, stock_ticker, analytic):
    ma_window = request.GET.get("ma_window", "3_day")
    time = request.GET.get("time", "all_time")
    response = prepare_response(
        getMovingAverages(stock_ticker, analytic, ma_window, time)
    )
    keys = [
        "result_df",
        "max_result",
        "max_date",
        "min_result",
        "min_date",
        "avg_result",
    ]
    return JsonResponse(dict(zip(keys, response)), safe=False)


def getLongestContinuousTrendsApi(request, stock_ticker, analytic):
    time = request.GET.get("time", "all_time")
    ma_window = request.GET.get("ma_window", "NA")
    ma_analytic = request.GET.get("ma_analytic", "NA")
    data = getLongestContinuousTrends(
        stock_ticker, analytic, time, ma_window, ma_analytic
    )
    return JsonResponse(
        list([[str(x) for x in sublist] for sublist in data]), safe=False
    )


def getRankingsApi(request, analytic):
    time = request.GET.get("time", "all_time")
    ma_analytic = request.GET.get("ma_analytic", "NA")
    ma_window = request.GET.get("ma_window", "NA")

    params = {
        "analytic": analytic,
        "time": time,
        "ma_analytic": ma_analytic,
        "ma_window": ma_window,
    }

    cached_response = get_cached_response("getRankingsApi", params)
    if cached_response is not None:
        return JsonResponse(cached_response, safe=False)

    data = getRankings(analytic, time, ma_analytic, ma_window)
    APICache.objects.create(
        api_name="getRankingsApi",
        params=json.dumps(params, sort_keys=True),
        response=data,
    )

    return JsonResponse(data, safe=False)


def getCorrelationAnalyticsApi(request, stock_ticker, analytic):
    time = request.GET.get("time", "all_time")
    ma_analytic = request.GET.get("ma_analytic", "NA")
    ma_window = request.GET.get("ma_window", "NA")

    params = {
        "stock_ticker": stock_ticker,
        "analytic": analytic,
        "time": time,
        "ma_analytic": ma_analytic,
        "ma_window": ma_window,
    }

    cached_response = get_cached_response("getCorrelationAnalyticsApi", params)
    if cached_response is not None:
        return JsonResponse(cached_response, safe=False)

    data = getCorrelationAnalytics(stock_ticker, analytic, time, ma_analytic, ma_window)
    APICache.objects.create(
        api_name="getCorrelationAnalyticsApi",
        params=json.dumps(params, sort_keys=True),
        response=data,
    )

    return JsonResponse(data, safe=False)


def prepare_response(response):
    response = list(response)
    response[0].index = response[0].index.astype(str)
    response[0] = response[0].to_dict()

    response = [str(x) if not isinstance(x, dict) else x for x in response]
    return response


def get_cached_response(api_name, params):
    params_json = json.dumps(params, sort_keys=True)
    cache_entry = APICache.objects.filter(api_name=api_name, params=params_json).first()

    if cache_entry:
        return cache_entry.response

    return None
