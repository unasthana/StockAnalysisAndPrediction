from django.contrib import admin
from django.urls import path
from .views import stock_detail, stock_name_list

urlpatterns = [
   path('admin/', admin.site.urls),
   path('stocks/', stock_name_list, name='stock-name-list'),
   path('stocks/<str:ticker>/', stock_detail, name='stock-detail'),
]