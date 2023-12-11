from datetime import datetime, timedelta

import pandas as pd
from .models import Stock


def getStockTickers():
    out = pd.Series(Stock.objects.values("name").distinct()).apply(lambda x: x["name"])
    return out


def getStockData(stock_ticker):
    stock_data = Stock.objects.filter(name=stock_ticker).values()
    df = pd.DataFrame(list(stock_data))
    return df


# API to calculate Daily Returns in a given time period.


def getDailyReturns(stock_ticker, time="all_time"):
    stock_data = getStockData(stock_ticker).set_index("date")
    stock_data["Daily_Returns"] = stock_data["close"].pct_change()

    # SEND stock_data['Daily_Returns'] back to the database as well

    time_values = {
        "all_time": len(stock_data),
        "1_week": 5,
        "2_weeks": 10,
        "1_month": 22,
        "1_quarter": 66,
        "6_months": 132,
        "1_year": 253,
    }

    if time.startswith("custom"):
        time_value = int(time[7:])
        time = "custom"
        time_values["custom"] = time_value

    if len(stock_data) < time_values[time]:
        return "Data is not available. Please reduce your time window!"

    if time == "all_time":
        result_df = stock_data["Daily_Returns"]
    else:
        result_df = stock_data["Daily_Returns"][-time_values[time] :]

    result_df.dropna(inplace=True)
    max_result = result_df.max()
    min_result = result_df.min()
    max_date = result_df.idxmax()
    min_date = result_df.idxmin()
    avg_result = result_df.mean()

    return result_df, max_result, max_date, min_result, min_date, avg_result


# API to get Daily Price Change in a given time period.


def getDailyPriceChange(stock_ticker, time="all_time"):
    stock_data = getStockData(stock_ticker).set_index("date")
    stock_data["Daily_Price_Change"] = stock_data["close"] - stock_data["open"]

    # SEND stock_data['Daily_Price_Change'] back to the database as well

    time_values = {
        "all_time": len(stock_data),
        "1_week": 5,
        "2_weeks": 10,
        "1_month": 22,
        "1_quarter": 66,
        "6_months": 132,
        "1_year": 253,
    }

    if time.startswith("custom"):
        time_value = int(time[7:])
        time = "custom"
        time_values["custom"] = time_value

    if len(stock_data) < time_values[time]:
        return "Data is not available. Please reduce your time window!"

    if time == "all_time":
        result_df = stock_data["Daily_Price_Change"]
    else:
        result_df = stock_data["Daily_Price_Change"][-time_values[time] :]

    result_df.dropna(inplace=True)
    max_result = result_df.max()
    min_result = result_df.min()
    max_date = result_df.idxmax()
    min_date = result_df.idxmin()
    avg_result = result_df.mean()

    return result_df, max_result, max_date, min_result, min_date, avg_result


# API to get Daily Price Range in a given time period.


def getDailyPriceRange(stock_ticker, time="all_time"):
    stock_data = getStockData(stock_ticker).set_index("date")
    stock_data["Daily_Price_Range"] = stock_data["high"] - stock_data["low"]

    # SEND stock_data['Daily_Price_Range'] back to the database as well

    time_values = {
        "all_time": len(stock_data),
        "1_week": 5,
        "2_weeks": 10,
        "1_month": 22,
        "1_quarter": 66,
        "6_months": 132,
        "1_year": 253,
    }

    if time.startswith("custom"):
        time_value = int(time[7:])
        time = "custom"
        time_values["custom"] = time_value

    if len(stock_data) < time_values[time]:
        return "Data is not available. Please reduce your time window!"

    if time == "all_time":
        result_df = stock_data["Daily_Price_Range"]
    else:
        result_df = stock_data["Daily_Price_Range"][-time_values[time] :]

    result_df.dropna(inplace=True)
    max_result = result_df.max()
    min_result = result_df.min()
    max_date = result_df.idxmax()
    min_date = result_df.idxmin()
    avg_result = result_df.mean()

    return result_df, max_result, max_date, min_result, min_date, avg_result


# API to get Daily Price Gap in a given time period.


def getDailyPriceGap(stock_ticker, time="all_time"):
    stock_data = getStockData(stock_ticker).set_index("date")
    stock_data["Daily_Price_Gap"] = stock_data["open"] - stock_data["close"].shift(1)

    # SEND stock_data['Daily_Price_Gap'] back to the database as well

    time_values = {
        "all_time": len(stock_data),
        "1_week": 5,
        "2_weeks": 10,
        "1_month": 22,
        "1_quarter": 66,
        "6_months": 132,
        "1_year": 253,
    }

    if time.startswith("custom"):
        time_value = int(time[7:])
        time = "custom"
        time_values["custom"] = time_value

    if len(stock_data) < time_values[time]:
        return "Data is not available. Please reduce your time window!"

    if time == "all_time":
        result_df = stock_data["Daily_Price_Gap"]
    else:
        result_df = stock_data["Daily_Price_Gap"][-time_values[time] :]

    result_df.dropna(inplace=True)
    max_result = result_df.max()
    min_result = result_df.min()
    max_date = result_df.idxmax()
    min_date = result_df.idxmin()
    avg_result = result_df.mean()

    return result_df, max_result, max_date, min_result, min_date, avg_result


def getYearlyPerformance(stock_ticker):
    stock_data = getStockData(stock_ticker)

    if len(stock_data) < 253:
        return "Not enough data to calculate yearly performance. Please wait while we update our APIs. Thank you :)"

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

    max_result = result_df.max()
    min_result = result_df.min()
    max_date = result_df.idxmax()
    min_date = result_df.idxmin()
    avg_result = result_df.mean()

    return result_df, max_result, max_date, min_result, min_date, avg_result


def getRawAnalyticData(stock_ticker, raw_analytic, time="all_time"):
    stock_data = getStockData(stock_ticker).set_index("date")

    time_values = {
        "all_time": len(stock_data),
        "1_week": 5,
        "2_weeks": 10,
        "1_month": 22,
        "1_quarter": 66,
        "6_months": 132,
        "1_year": 253,
    }

    if time.startswith("custom"):
        time_value = int(time[7:])
        time = "custom"
        time_values["custom"] = time_value

    if len(stock_data) < time_values[time]:
        return "Data is not available. Please reduce your time window!"

    if time == "all_time":
        result_df = stock_data[raw_analytic]
    else:
        result_df = stock_data[raw_analytic][-time_values[time] :]

    max_result = result_df.max()
    min_result = result_df.min()
    max_date = result_df.idxmax()
    min_date = result_df.idxmin()
    avg_result = result_df.mean()

    return result_df, max_result, max_date, min_result, min_date, avg_result


def getAnalyticData(
    analytic, stock_ticker, time="all_time", ma_analytic="NA", ma_window="NA"
):
    res = None
    if analytic == "yearly_performance":
        res = getYearlyPerformance(stock_ticker)

    elif analytic == "daily_price_gap":
        res = getDailyPriceGap(stock_ticker, time)

    elif analytic == "daily_price_range":
        res = getDailyPriceRange(stock_ticker, time)

    elif analytic == "daily_price_change":
        res = getDailyPriceChange(stock_ticker, time)

    elif analytic == "daily_returns":
        res = getDailyReturns(stock_ticker, time)

    elif analytic == "moving_averages":
        res = getMovingAverages(stock_ticker, ma_analytic, ma_window, time)

    return res


def getMovingAverages(stock_ticker, analytic, ma_window="3_day", time="all_time"):
    stock_data = getStockData(stock_ticker).set_index("date")

    if analytic not in stock_data.columns:
        analytic_data = getAnalyticData(analytic, stock_ticker)[0]

    else:
        analytic_data = stock_data[analytic]

    ma_window_values = {
        "3_day": 3,
        "5_day": 5,
        "10_day": 10,
        "30_day": 30,
        "60_day": 60,
    }

    if ma_window.startswith("custom"):
        ma_window_value = int(ma_window[7:])
        ma_window = "custom"
        ma_window_values["custom"] = ma_window_value

    if len(analytic_data) < ma_window_values[ma_window]:
        return "Data is not available. Please reduce your Moving Average Time Window!"

    MA_analytic = analytic_data.rolling(window=ma_window_values[ma_window]).mean()

    time_values = {
        "all_time": len(MA_analytic),
        "1_week": 5,
        "2_weeks": 10,
        "1_month": 22,
        "1_quarter": 66,
        "6_months": 132,
        "1_year": 253,
    }

    if time.startswith("custom"):
        time_value = int(time[7:])
        time = "custom"
        time_values["custom"] = time_value

    if len(MA_analytic) < time_values[time]:
        return "Data is not available. Please reduce your time window!"

    if time == "all_time":
        result_df = MA_analytic

    else:
        result_df = MA_analytic[-time_values[time] :]

    result_df.dropna(inplace=True)
    max_result = result_df.max()
    min_result = result_df.min()
    max_date = result_df.idxmax()
    min_date = result_df.idxmin()
    avg_result = result_df.mean()

    return result_df, max_result, max_date, min_result, min_date, avg_result


def getRankings(analytic, time="all_time", ma_analytic="NA", ma_window="NA"):
    stock_tickers = getStockTickers()

    rankings = []

    for stock_ticker in stock_tickers:
        stock_data = getStockData(stock_ticker).set_index("date")

        if analytic not in stock_data.columns:
            analytic_data = getAnalyticData(
                analytic, stock_ticker, time, ma_analytic, ma_window
            )

        else:
            analytic_data = getRawAnalyticData(stock_ticker, analytic, time)

        if not isinstance(analytic_data, str):
            rankings.append([stock_ticker, analytic_data[5]])

    rankings.sort(key=lambda x: x[1], reverse=True)

    return rankings


def getDuration(start_date, end_date):
    if not isinstance(start_date, str) and not isinstance(end_date, str):
        x = end_date - start_date
        return x.days if isinstance(x, pd.Timedelta) or isinstance(x, timedelta) else int(x)

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    time_difference = end_date - start_date
    duration = time_difference.days

    return duration


def getLongestContinuousTrends(
    stock_ticker, analytic, time="all_time", ma_window="NA", ma_analytic="NA"
):
    stock_data = getStockData(stock_ticker).set_index("date")

    if analytic not in stock_data.columns:
        analytic_data = getAnalyticData(
            analytic, stock_ticker, time, ma_analytic, ma_window
        )[0].dropna()

    else:
        analytic_data = getRawAnalyticData(stock_ticker, analytic, time)[0].dropna()

    uptrend = [-1, "", ""]  # [duration, uptrend_start_date, uptrend_end_date]
    uptrend_start_date = analytic_data.index[0]

    prev = 0

    for i in range(1, len(analytic_data)):
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


def getCorrelationAnalytics(
    target_stock_ticker, analytic, time="all_time", ma_analytic="NA", ma_window="NA"
):
    stock_tickers = getStockTickers()
    combined_df = pd.DataFrame(columns=stock_tickers)

    for stock_ticker in stock_tickers:
        stock_data = getStockData(stock_ticker)

        if len(stock_data) <= 60:
            continue

        if analytic not in stock_data.columns:
            analytic_data = getAnalyticData(
                analytic, stock_ticker, time, ma_analytic, ma_window
            )

        else:
            analytic_data = getRawAnalyticData(stock_ticker, analytic, time)

        if not isinstance(analytic_data, str):
            combined_df[f"{stock_ticker}"] = analytic_data[0]

    combined_df.fillna(method="ffill", inplace=True)
    combined_df.fillna(method="bfill", inplace=True)

    # Choose the target column for which you want MIC scores
    target_column = target_stock_ticker

    # Create a DataFrame to store MIC scores
    mic_scores = pd.Series(
        index=combined_df.columns.difference([target_column]), dtype=float
    )

    # Calculate MIC scores for the chosen target column
    for col in combined_df.columns.difference([target_column]):
        mine = MINE()
        mine.compute_score(combined_df[col], combined_df[target_column])
        mic_scores[col] = mine.mic()

    mic_scores = mic_scores.sort_values(ascending=False)

    return mic_scores.to_dict()
