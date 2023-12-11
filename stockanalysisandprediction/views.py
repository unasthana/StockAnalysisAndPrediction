import pandas as pd
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Stock, CompanyInfo
from .serializers import StockSerializer, StockNameSerializer


@api_view(['GET'])
def stock_detail(request, ticker):
    stocks = Stock.objects.filter(name=ticker)
    try:
        sector = CompanyInfo.objects.get(ticker=ticker).sector
    except CompanyInfo.DoesNotExist:
        sector = None
    serializer = StockSerializer(stocks, many=True)
    response_data = serializer.data
    return Response({"sector": sector, "data": response_data})


@api_view(['GET'])
def stock_name_list(request):
    stock_names = Stock.objects.values('name').distinct()
    serializer = StockNameSerializer(stock_names, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def daily_returns(request, stock_ticker, time='all_time'):
    stock_data = Stock.objects.filter(name=stock_ticker).order_by('date').values('date', 'close')
    df = pd.DataFrame(list(stock_data))
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df['Daily_Returns'] = df['close'].pct_change()

    # Time period handling
    time_values = get_time_values()
    handle_custom_time(time, time_values, df)

    df.dropna(inplace=True)
    max_result = df['Daily_Returns'].max()
    min_result = df['Daily_Returns'].min()
    max_date = df['Daily_Returns'].idxmax()
    min_date = df['Daily_Returns'].idxmin()
    avg_result = df['Daily_Returns'].mean()

    response = {
        'data': df['Daily_Returns'].tolist(),
        'max': max_result,
        'max_date': max_date,
        'min': min_result,
        'min_date': min_date,
        'average': avg_result
    }
    return JsonResponse(response)


@api_view(['GET'])
def daily_price_change(request, stock_ticker, time='all_time'):
    stock_data = Stock.objects.filter(name=stock_ticker).order_by('date').values('date', 'open', 'close')
    df = pd.DataFrame(list(stock_data))
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df['Daily_Price_Change'] = df['close'] - df['open']

    # Time period handling
    time_values = get_time_values()
    handle_custom_time(time, time_values, df)

    # Calculation
    df.dropna(inplace=True)
    response = calculate_stats(df, 'Daily_Price_Change')
    return JsonResponse(response)


@api_view(['GET'])
def daily_price_range(request, stock_ticker, time='all_time'):
    stock_data = Stock.objects.filter(name=stock_ticker).order_by('date').values('date', 'high', 'low')
    df = pd.DataFrame(list(stock_data))
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df['Daily_Price_Range'] = df['high'] - df['low']

    # Time period handling
    time_values = get_time_values()
    handle_custom_time(time, time_values, df)

    # Calculation
    df.dropna(inplace=True)
    response = calculate_stats(df, 'Daily_Price_Range')
    return JsonResponse(response)


@api_view(['GET'])
def daily_price_gap(request, stock_ticker, time='all_time'):
    stock_data = Stock.objects.filter(name=stock_ticker).order_by('date').values('date', 'open', 'close')
    df = pd.DataFrame(list(stock_data))
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    df['Daily_Price_Gap'] = df['open'] - df['close'].shift(1)

    # Time period handling
    time_values = get_time_values()
    handle_custom_time(time, time_values, df)

    # Calculation
    df.dropna(inplace=True)
    response = calculate_stats(df, 'Daily_Price_Gap')
    return JsonResponse(response)


@api_view(['GET'])
def yearly_performance(request, stock_ticker):
    stock_data = Stock.objects.filter(name=stock_ticker).order_by('date').values('date', 'close')
    if len(stock_data) < 253:
        return JsonResponse("Not enough data to calculate yearly performance.", safe=False)

    df = pd.DataFrame(list(stock_data))
    df['date'] = pd.to_datetime(df['date'])
    df['year'] = df['date'].dt.year
    df.set_index('date', inplace=True)

    yearly_performance = df.groupby('year')['close'].apply(lambda x: (x.iloc[-1] / x.iloc[0] - 1) * 100)

    # Calculation
    response = {
        'yearly_performance': yearly_performance.tolist(),
        'max': yearly_performance.max(),
        'min': yearly_performance.min(),
        'average': yearly_performance.mean()
    }
    return JsonResponse(response)


def get_time_values():
    return {"all_time": 0, "1_week": 5, "2_weeks": 10, "1_month": 22, "1_quarter": 66, "6_months": 132, "1_year": 253}


def handle_custom_time(time, time_values, df):
    if time.startswith('custom'):
        time_value = int(time[7:])
        time = 'custom'
        time_values["custom"] = time_value

    if time != 'all_time':
        df = df[-time_values[time]:]


def calculate_stats(df, column):
    max_result = df[column].max()
    min_result = df[column].min()
    max_date = df[column].idxmax()
    min_date = df[column].idxmin()
    avg_result = df[column].mean()

    return {
        'data': df[column].tolist(),
        'max': max_result,
        'max_date': max_date.strftime('%Y-%m-%d') if max_date else None,
        'min': min_result,
        'min_date': min_date.strftime('%Y-%m-%d') if min_date else None,
        'average': avg_result
    }
