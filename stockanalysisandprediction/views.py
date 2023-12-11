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
