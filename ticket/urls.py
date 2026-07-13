from django.urls import path
from . import views

# 票务相关路由：查询页 / 购票
urlpatterns = [
    path('', views.ticket, name='ticket'),
    path('buy/', views.buy_ticket, name='buy_ticket'),
]
