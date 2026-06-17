from django.urls import path
from . import views

urlpatterns = [
    path('', views.my_orders, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('my/', views.my_orders, name='my_orders'),
    path('refund/<int:order_id>/', views.refund_ticket, name='refund_ticket'),
]