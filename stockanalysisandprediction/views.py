from datetime import datetime

import pandas as pd
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Stock, CompanyInfo
from .serializers import StockSerializer, StockNameSerializer


@api_view(["GET"])
def stock_detail(request, ticker):
    stocks = Stock.objects.filter(name=ticker)
    try:
        sector = CompanyInfo.objects.get(ticker=ticker).sector
    except CompanyInfo.DoesNotExist:
        sector = None
    serializer = StockSerializer(stocks, many=True)
    response_data = serializer.data
    return Response({"sector": sector, "data": response_data})


@api_view(["GET"])
def stock_name_list(request):
    stock_names = Stock.objects.values("name").distinct()
    serializer = StockNameSerializer(stock_names, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def daily_returns(request, stock_ticker, time="all_time"):
    response = calculate_stats(
        get_daily_returns_df(stock_ticker, time), "Daily_Returns"
    )
    return JsonResponse(response)


def get_daily_returns_df(ticker, time):
    stock_data = (
        Stock.objects.filter(name=ticker).order_by("date").values("date", "close")
    )
    df = pd.DataFrame(list(stock_data))
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    df["Daily_Returns"] = df["close"].pct_change()
    df = df["Daily_Returns"]

    # Time period handling
    time_values = get_time_values()
    handle_custom_time(time, time_values, df)

    df.dropna(inplace=True)
    return df


@api_view(["GET"])
def daily_price_change(request, stock_ticker, time="all_time"):
    response = calculate_stats(
        get_daily_returns_df(stock_ticker, time), "Daily_Price_Change"
    )
    return JsonResponse(response)


def get_daily_price_change_df(ticker, time):
    stock_data = (
        Stock.objects.filter(name=ticker)
        .order_by("date")
        .values("date", "open", "close")
    )
    df = pd.DataFrame(list(stock_data))
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    df["Daily_Price_Change"] = df["close"] - df["open"]
    df = df["Daily_Price_Change"]

    # Time period handling
    time_values = get_time_values()
    handle_custom_time(time, time_values, df)

    # Calculation
    df.dropna(inplace=True)
    df = df["Daily_Price_Change"]
    return df


@api_view(["GET"])
def daily_price_range(request, stock_ticker, time="all_time"):
    response = calculate_stats(
        get_daily_price_range_df(stock_ticker, time), "Daily_Price_Range"
    )
    return JsonResponse(response)


def get_daily_price_range_df(ticker, time):
    stock_data = (
        Stock.objects.filter(name=ticker).order_by("date").values("date", "high", "low")
    )
    df = pd.DataFrame(list(stock_data))
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    df["Daily_Price_Range"] = df["high"] - df["low"]
    df = df["Daily_Price_Range"]

    # Time period handling
    time_values = get_time_values()
    handle_custom_time(time, time_values, df)

    # Calculation
    df.dropna(inplace=True)
    return df


@api_view(["GET"])
def daily_price_gap(request, stock_ticker, time="all_time"):
    response = calculate_stats(
        get_daily_price_gap_df(stock_ticker, time), "Daily_Price_Gap"
    )
    return JsonResponse(response)


def get_daily_price_gap_df(ticker, time):
    stock_data = (
        Stock.objects.filter(name=ticker)
        .order_by("date")
        .values("date", "open", "close")
    )
    df = pd.DataFrame(list(stock_data))
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)
    df["Daily_Price_Gap"] = df["open"] - df["close"].shift(1)
    df = df["Daily_Price_Gap"]

    # Time period handling
    time_values = get_time_values()
    handle_custom_time(time, time_values, df)

    # Calculation
    df.dropna(inplace=True)
    return df


@api_view(["GET"])
def yearly_performance(request, stock_ticker):
    yearly_performance = get_yearly_performance_df(stock_ticker)
    if isinstance(yearly_performance, JsonResponse):
        return yearly_performance

    # Calculation
    response = {
        "yearly_performance": yearly_performance.tolist(),
        "max": yearly_performance.max(),
        "min": yearly_performance.min(),
        "average": yearly_performance.mean(),
    }
    return JsonResponse(response)


def get_yearly_performance_df(ticker):
    stock_data = (
        Stock.objects.filter(name=ticker).order_by("date").values("date", "close")
    )
    if len(stock_data) < 253:
        return JsonResponse(
            "Not enough data to calculate yearly performance.", safe=False
        )

    df = pd.DataFrame(list(stock_data))
    # Convert 'date' column to datetime type
    stock_data["date"] = pd.to_datetime(stock_data["date"])

    stock_data["year"] = stock_data["date"].dt.year
    stock_data["Yearly_Performance"] = (
                                               (
                                                       stock_data.groupby("year")["close"].transform("last")
                                                       / stock_data.groupby("year")["close"].transform("first")
                                               )
                                               - 1
                                       ) * 100

    result_df = pd.DataFrame(
        {"Yearly_Performance": stock_data["Yearly_Performance"].unique()},
        index=stock_data["year"].unique(),
    )

    result_df = result_df["Yearly_Performance"]
    return result_df


def get_time_values():
    return {
        "all_time": 0,
        "1_week": 5,
        "2_weeks": 10,
        "1_month": 22,
        "1_quarter": 66,
        "6_months": 132,
        "1_year": 253,
    }


def handle_custom_time(time, time_values, df):
    if time.startswith("custom"):
        time_value = int(time[7:])
        time = "custom"
        time_values["custom"] = time_value

    if time != "all_time":
        df = df[-time_values[time] :]


def calculate_stats(df, column):
    max_result = df[column].max()
    min_result = df[column].min()
    max_date = df[column].idxmax()
    min_date = df[column].idxmin()
    avg_result = df[column].mean()

    return {
        "data": df[column].tolist(),
        "max": max_result,
        "max_date": max_date.strftime("%Y-%m-%d") if max_date else None,
        "min": min_result,
        "min_date": min_date.strftime("%Y-%m-%d") if min_date else None,
        "average": avg_result,
    }


def getAnalyticData(
    analytic, stock_ticker, time="all_time", ma_analytic="NA", ma_window="NA"
):
    if analytic == "yearly_performance":
        res = get_yearly_performance_df(stock_ticker)

    elif analytic == "daily_price_gap":
        res = get_daily_price_gap_df(stock_ticker, time)

    elif analytic == "daily_price_range":
        res = get_daily_price_range_df(stock_ticker, time)

    elif analytic == "daily_price_change":
        res = get_daily_price_range_df(stock_ticker, time)

    elif analytic == "daily_returns":
        res = get_daily_returns_df(stock_ticker, time)

    # elif analytic == 'moving_averages':
    #   res = (stock_ticker, ma_analytic, ma_window, time)

    return res


@api_view(["GET"])
def get_longest_continuous_trends(request):
    stock_ticker = request.query_params.get("stock_ticker")
    analytic = request.query_params.get("analytic")
    time = request.query_params.get(
        "time", "all_time"
    )  # default to 'all_time' if not provided
    ma_window = request.query_params.get(
        "ma_window", "NA"
    )  # default to 'NA' if not provided
    ma_analytic = request.query_params.get(
        "ma_analytic", "NA"
    )  # default to 'NA' if not provided

    stock_data = Stock.objects.filter(name=stock_ticker).values()
    df = pd.DataFrame(list(stock_data))
    df["date"] = pd.to_datetime(df["date"])
    df.set_index("date", inplace=True)

    analytic_data = getAnalyticData(
        analytic, stock_ticker, time, ma_analytic, ma_window
    ).dropna()

    uptrend = [-1, "", ""]  # [duration, uptrend_start_date, uptrend_end_date]
    uptrend_start_date = analytic_data.index[0]

    prev = 0

    for i in range(1, len(analytic_data)):
        print(analytic_data.iloc[i])
        if analytic_data.iloc[i] < analytic_data.iloc[prev]:
            uptrend_end_date = analytic_data.index[prev]
            duration = getDuration(uptrend_start_date, uptrend_end_date)

            if duration >= uptrend[0]:
                uptrend[0] = duration
                uptrend[1] = uptrend_start_date
                uptrend[2] = uptrend_end_date

            uptrend_start_date = analytic_data.index[i]

        prev = i

    downtrend = [-1, "", ""]  # [duration, downtrend_start_date, downtrend_end_date]
    downtrend_start_date = analytic_data.index[0]

    prev = 0

    for i in range(1, len(analytic_data)):
        if analytic_data.iloc[i] > analytic_data.iloc[prev]:
            downtrend_end_date = analytic_data.index[prev]
            duration = getDuration(downtrend_start_date, downtrend_end_date)

            if duration >= downtrend[0]:
                downtrend[0] = duration
                downtrend[1] = downtrend_start_date
                downtrend[2] = downtrend_end_date

            downtrend_start_date = analytic_data.index[i]

        prev = i

    return uptrend, downtrend


def getDuration(start_date, end_date):
    if not isinstance(start_date, str) and not isinstance(end_date, str):
        return end_date - start_date

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    time_difference = end_date - start_date
    duration = time_difference.days

    return duration
