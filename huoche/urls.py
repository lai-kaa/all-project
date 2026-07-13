"""
项目主路由配置。
根路径 '/' 为首页，用户与票务功能分别由 my / ticket 应用提供。
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('search/', views.global_search, name='search'),
    path('support/', include('support.urls')),
    path('', include('my.urls')),
    path('ticket/', include('ticket.urls')),
]
